#! /usr/bin/env python3

import os, sys, re
if len(sys.argv) > 1:
    shellMarker = sys.argv[1]

else:
    shellMarker = '$'
    
while 1:
    user_input = input(shellMarker + ": ") #need to swtich $ to the actual char user chooses

    print(shellMarker + ":", user_input)

    if user_input == 'exit':
        break
    
    pid = os.fork()

    if pid == 0:  # Child process
        # Split the command into arguments
        args = user_input.split()

        try:
            # Execute the command
            os.execve(args[0], args, os.environ)
        except FileNotFoundError:
            # If the command is not found, print an error message
            print("Command not found:", args[0])
            sys.exit(1)
    elif pid < 0:  # Error
        print("Fork failed")
        sys.exit(1)
    else:  # Parent process
        # Wait for the child process to finish
        _, status = os.waitpid(pid, 0)

        # Check if the child process exited normally
        if os.WIFEXITED(status):
            # Print the exit status of the child process
            print("Child process exited with status", os.WEXITSTATUS(status))
