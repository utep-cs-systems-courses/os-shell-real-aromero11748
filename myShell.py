#! /usr/bin/env python3

import os, sys, re
import fileinput

if len(sys.argv) > 1:
    shellMarker = sys.argv[1]

else:
    shellMarker = '$'
    
while 1:
    user_input = input(shellMarker + ": ") #need to swtich $ to the actual char user chooses

    print(shellMarker + ":", user_input)

    if user_input == 'exit':
        break

    #for pipes later
    pr,pw = os.pipe()
    for i in (pr, pw):
        os.set_inheritable(i, True)
    #-----------------------------
    
    pid = os.fork()

    if pid < 0:  # Error
        print("Fork failed")
        sys.exit(1)

    elif pid == 0:  # Child process
        # Split the command into arguments

        args1 = user_input.split()

        args = [args1[0], args1[1], args1[2]]
            # Execute the command

        if args[1] == '<' :
            print('another redirection')
        
        elif args[1] == '>' :
            print('in > ')
            os.close(1) #redirect childs stdout
            #here we are going to write the output into args[2]
            os.open(args[2], os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)
            args.pop(1)
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                print(program)
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            os.write(2, ("Child: Error: Could not exec %s\n" % args[0]).encode())
            sys.exit(1)

        elif args[1] == '|':
            print('in pipes')
            os.close(1)
            os.dup(pw)
            for fd in (pr, pw):
                os.close(fd)
            print('in child')
            
        else:
            args = user_input.split()
            
            try:
                # Execute the command
                os.execve(args[0], args, os.environ)
            except FileNotFoundError:
                # If the command is not found, print an error message
                print("Command not found:", args[0])
                sys.exit(1)


    else:  # Parent process
        # Wait for the child process to finish
        _, status = os.waitpid(pid, 0)

        args1 = user_input.split()
        
        if args1[1] == '|':
            os.close(0)
            os.dup(pr)
            for fd in (pw, pr):
                os.close(fd)
            for line in fileinput.input():
                print("from child: <%s>" % line)
        
        # Check if the child process exited normally
        if os.WIFEXITED(status):
            # Print the exit status of the child process
            print("Child process exited with status", os.WEXITSTATUS(status))
