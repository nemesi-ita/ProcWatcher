# ProcWatcher
Process_Watcher.py

process_wacher.py is divided into 2 groups of functions:

G_1) getProcs() returns a dictionary containing pid-program_in_execution pairings. This list is passed as an argument to the filteringProcs() function, which searches for an element (target program name) in the procList[] list. If the result is positive, a simple logic bomb is triggered that initiates the keylogger in the background

G_2) The start of background execution is handled by the startK() function, which sets the execution flags as a separate process and starts the actual malware: K().
K() is a simple function that uses the keyboard library to intercept keystrokes. It saves to a file (OUT, present at the beginning of the code).
Sending the file is handled by the sendAndErase() function, which uses the atexit library to execute itself as a closing action.
The file can be received through an IRC chat. Encryption is implemented by default

Enjoy!