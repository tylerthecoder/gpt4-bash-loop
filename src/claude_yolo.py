import anthropic
import subprocess

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"


def run_command(command, cwd=None):
    try:
        data = subprocess.run(
            command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        response = f"""
    STDOUT:
    {data.stdout.decode("utf-8")}
    STDERR:
    {data.stderr.decode("utf-8")}
    Exit Code: {data.returncode}
    """
    except Exception as e:
        response = f"""
An error occurred while running the command:
{e}
"""

    return response


def main():
    client = anthropic.Anthropic()

    GOAL = """
Explore this machine. You will find the most imortant files and folder for the user tylord.
You will not edit anything, only read. You should make a note in the ~/CLAUDEDOC.md about what you found.

Don't return a tool call when you are done
"""
    messages: list = [
        {
            "role": "user",
            "content": f"""
Your name is Jarvis. You are a helpful assistant that can run bash commands.

             You will assist with this goal:
             {GOAL}
            """,
        },
    ]
    while True:

        print(f"Calling API... num_of_messages: {len(messages)}")

        print(messages)

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=messages,
            tools=[
                {
                    "name": "bash-shell",
                    "description": "Run a bash command",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "The bash command to run",
                            },
                            "cwd": {
                                "type": "string",
                                "description": "The directory to run the command in",
                            },
                        },
                        "required": ["command", "cwd"],
                    },
                }
            ],
        )

        if not response.stop_reason == "tool_use":
            print("No tool used. Stopping...")
            break

        formatted_content = []
        for content in response.content:
            formatted_content.append(content.__dict__)

        messages.append({"role": "assistant", "content": formatted_content})

        for content in response.content:
            print(f"Content type: {content.type}")
            if content.type == "message":
                print(content.text)
            if content.type == "tool_use":
                tool_name = content.name
                id = content.id
                if tool_name == "bash-shell":
                    command = content.input["command"]
                    cwd = content.input["cwd"]
                    print(f"Running command: {command}")
                    output = run_command(command, cwd)
                    print(output)
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": id,
                                    "content": output,
                                }
                            ],
                        }
                    )

    print("Goodbye!")
    pass


if __name__ == "__main__":
    main()
