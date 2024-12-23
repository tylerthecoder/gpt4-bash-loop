Jarvis will be able to help get things done on your computer.


Main features:

`jarvis`
- Prompt the user for natural language and jarvis will suggest a command to run.
- You can then either:
    - Run the command
    - Ask for a better command
    - Start a task instead
- Once the command is run, jarvis will summarize the output and ask the user for the next steps. The user can either
    - Exit
    - submit a new natural language command
And then the loop starts again.


`jarvis task`
- Start Task:
- You can ask jarvis to do a more complex task that will take multiple steps
- Jarvis is asked for code, then the code will be ran, and then jarvis will be fed the output. It then can:
    - Exit since the task is complete
    - Suggest a new command to run
    - Ask the human for clarification

`jarvis task list` will show all running tasks and which ones need human input.


Jarvis will save all conversations that have happened and can use these to learn.

Jarvis's state is saved to the state.json file. The file location is defaulted to ~/.local/share/jarvis/state.json.



