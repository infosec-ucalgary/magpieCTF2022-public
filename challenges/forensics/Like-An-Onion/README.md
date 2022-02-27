# Like An Onion
### Category: Forensics
### Author: Daniel Sabourov (SteamBlizzard) & Jeremy Stuart (Mr.Wizard)

## Description
On behalf of Mom & Pop, thank you for accepting this contract!  Flags are somehow leaking out to the public, so we gave each employee a unique flag to see who was responsible for it.  We found the employee whose flag was leaked: Tanner Bratach.  Tanner isn't clever enough to hatch a scheme like this, so we took a snapshot of his work computer and  need you to analyze it.

We need you to figure out how the flag is being leaked and what flag is going to be leaked next.  Thank you again for assisting Mom & Pops Flag Shop I.T. department with this incident response!


## Hints
1. It's a capital I not a lower case l


## Solution
1. You are given a memory dump.  Your go to should be to load up volatility to start examining the dump.
2. There are no obviously supicious processes, so you need to look around for signs of suspicious processes.  Possible clues include:
    a. pstree plugin: there's one svchost.exe process - PID 2880 - without a running parent process.  It also started much later than the others.
    b. netscan plugin: find that there's an established connection to IP address `143.198.148.79` on a high numbered port.
    c. malfind plugin: several processes show signs of infection, including the PID 2880 svchost process.
    d. hivelist plugin: find a key called "vexillum-ferum" (latin for flag thief).  It runs `586657.dll`, which contains a string for "RattusOneratus" (latin for "rat loader")
    e. yarascan plugin: searching for IP address reveals it's coming from one of the svchost processes, the one with PID 2880.  Also noticed mention of a file called `vex.dat`
3. These are all signs that there's a remote access trojan (RAT) on this machine.  It also suggest that svchost.exe (PID 2880) isn't what it seems.  In fact, it's been the victim of process hollowing.  Malware has run svchost.exe and replaced it's memory space with the malware code, therfore the malware is running as svchost to try to hide itself.  Keep digging into this process:
    a. consoles plugin: someone ran `echo "VEX WAS HERE"` pointing to Vex being the one who might be taking the flags (Vex is mentioned in another challenge).
    c. procdump plugin: dump the executable for scvhost.exe (PID 2880).  There's a string in there for `C:\Users\TannerBratach\Downloads\vex.dat`
    d. filescan plugin: search for `vex.dat` finds it exists at memory address `0x000000007f98df20`
    e. dumpfiles plugin: allows you to dump the `vex.dat` file.
4. Fun file on `vex.dat` to find it's a jpg.  Open it to see a picture of an onion with Shrek's face on it.  Because we all know that ogres are like onions (also because the challenge is called "Like An Onion") is a strong clue that you are on the right track.
5. Binwalk the image to find a zip file attached to it.  Extract it with binwalk to get `pycnstrct.js`
6. Inside of the javascript file will be a very, very, very long string of unicode characters. This is a python file that has been encrypted using the functions inside of the file. You will have to refactor the functions and variables in order to figure out what's actually going on ([Here's a link to a John Hammond video where he does something like this.](https://www.youtube.com/watch?v=2wg4H9RMk3E)). These functions are used to encode strings into this "unicode" ciphertext, and also used to decode it using either a specified number or a range of numbers, and the way you can get the file is to comment or delete line 37 `fs.unlinkSync("./knwbabaomask.py");`, which is deleting a python file that was decoded from the large encoded string using the functions.
7. Inside of the python file, a Visual Basic Script file is being built via a lot of concatenations. In between each concatenation is a lot of pointless functions and lines that do effectively nothing. While the solution is (once again) to prevent the program from deleting the vbs file after it's done running by commenting or deleting line 20409 `paa0A23n("vnA3A2dmA.vbs")`, you will likely only realize this once you remove the pointless lines from the file using regex (which is also displayed in the John Hammond video mentioned above). You will also most likely have to refactor the functions and variables to understand what's going on in the file.
8. Once you have the Visual Basic Script file, you must figure out how to decode the flag that has been encoded using a variety of methods, all of which are provided as functions in the file. Again, refactor the functions and variables to be readable. At the bottom of the file is a bunch of string concatenations that are just a lot of bytes representing either 0 or 1. If these are decoded, you are given bytes that can be decoded again to show an English string with more binary. The binary may be decoded to get a Base64 string which, after being decoded, will finally give you the flag. A couple of solutions include:
    a. Manually concatenating the strings and decoding them using tools such as CyberChef.
    b. Refactoring and using the functions and variables inside of the file and displaying the decoded results using a message box.


## Flag
magpie{unR4VeLl3D_7h3_c0Re!_4h123vad3fbs}


## Notes
The memory dump for this challenge is 712mb and too large to host on Github.  If you would like a copy of it, please get in contact with The InfoSec Club to see if it's available.