# followme
### Category: Reverse Engineering
### Author: inga

## Description
You have gained access to a company employee's home directory. He was the target of a specialized spear-fishing campaign where we successfully stole his credentials. More specifically, this user was targeted because our recon intel indicated that they have permissions to run a program which contains information on top secret patents. Currently we have a different program running which changes their password, as well as the port on which ssh connects. This password will be given to you and will be valid for the next ten minutes until which time the connection will close. Your task is to figure out exactly what this program is doing. You have been given a copy of the binary which you will need to further reverse engineer in this user's home directory. 

## Hints
1. xxd
2. sudo -l

## Solution
The binary "locked-secret" is stuck in an if condition which will never be called. In order to force the binary to run the function, the "if" condition needs to be hex edited so that instead of always being false, it becomes always true. After editing the hex code, the reconstructed binary needs to be trace using sudo and strace in order to uncover the flag. The program being run at the root directory makes a call to setfattr for a file called "lock-box.txt". The attribute being set is the flag and will be visible because the system call will be shown by strace. 

1. Decompile locked-secret
2. Identify if statement at 1210
3. Reverse the binary into hex
	* \# xxd locked-secret > ls.re
4. Identify the "if" statement in the hex code
	* 0083 f801
5. Replace the byte "01" with "00"
	* 0083 f800
6. Reconstruct the hex code back into a binary
	* \# xxd -r ls.re > unlocked-secret
	* \# sudo -l
8. Trace the program the binary is calling
	* \# sudo trace -f ./unlocked-secret
9. The flag will be in the output of the trace 

## Flag
magpie{1\_gu3sz\_y()u\_c4ught\_m3}
