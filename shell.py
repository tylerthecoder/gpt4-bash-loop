import openai
import os
import json
from termcolor import colored

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = '''
You are a helpful assistant that runs on my locally computer.
You can run bash commands for me. Here is some useful information:
~/docs is where I store all of my documents
'''

TOOLS = [
	{
        "type": "function",
        "function": {
            "name": "run_bash_command",
            "description": "Run a bash command and read the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run",
                    },
                },
                "required": ["command"],
            },
        }
    }
]

def run_bash_command(command):
    print("Do you want to run this command? (y/n)")
    print(command)
    user_input = input()
    if user_input.lower() != 'y':
        return "Command not run"
    output = os.popen(command).read()
    print("Command output: ", output)
    return output


def add_user_message(prompt, messages):
    messages += [
        {"role": "user", "content": prompt},
    ]

    return messages


def chat(messages):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tool_choice='auto',
        tools=TOOLS
    )

    message = response.choices[0].message

    messages += [message]

    if message.content:
        print(colored(message.content, "green"))

    # Check if a tool was used
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        func = tool_call.function
        if func.name == "run_bash_command":
            data = json.loads(func.arguments)
            command = data.get('command')
            command_output = run_bash_command(command)

            messages += [
                {"role": "tool", "content": command_output, "tool_call_id": tool_call.id},
            ]

            chat(messages)

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    while True:
        user_input = input("Enter your prompt: ")
        if user_input.lower() == 'exit':
            break
        add_user_message(user_input, messages)
        chat(messages)
