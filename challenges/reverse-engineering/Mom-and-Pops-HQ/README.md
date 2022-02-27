# Mom & Pops HQ

### Category: Reverse Engineering
### Author: Joshua Cordeiro-Zebkowitz

## Description
An insider at Mom & Pops has smuggled your team a disc with the blueprint of their headquarters.
The Bad News: It's locked behind a key code.
The Good News: The key code must get verified somewhere on that disc! Surely your team of expert heist-ers can crack it!

## Hints
1. I heard Mom & Pops hired an ELF for these blueprints; use Cutter as your weapon and you'll see right through them.

## Solution

1. Download the ISO image and mount it into another folder. Then change directory into the folder into which you mounted the image.
```
mkdir re-easy
sudo mount mp_headquarters.iso re-easy
cd re-easy
```
2. The folder should contain a single binary file called "CONFIDENTIAL_BLUEPRINTS". It should be executable already, but if your system has changed the permissions, make it executable.
```
chmod +x CONFIDENTIAL_BLUEPRINTS
```
3. You can run the program now. It will display the following, requesting a key code:
```
 ***Confidential***

 Please enter your unique key code:
```
4. We don't know what this is yet. To find out, open "CONFIDENTIAL_BLUEPRINTS" in a program that will decompile it (my choice would be Cutter). There are a bunch of different tabs in Cutter (e.g. Disassembly, Graphs, Strings) and while Disassembly and Graphs could be used to solve the challenge, a more visually appealing method is to use the built-in decompiler, specifically Ghidra.

5. From here, click on the main function on the column on the lefthand side. This is always a good place to start as its where execution begins. The main function asks for the input and has some filler code in it that calculates the length of the input and ensures it is of proper length. You should see that the function has an if-else statement in the latter half checking the length, which prints invalid in the if-section, and calls a function in the else-section. This should clue you in that the 'else' occurs when the input given is valid.

6. You can either double-click on the function called in the 'else' or look for it in the column on the lefthand side, either way it should take you to a 'checker' function, which validates the key code and prints out the ASCII art of the flag.
There are 8 nested if-statements here, each of which checks whether an index of the input is correct, but it checks them out-of-order. It obtains the correct character for each index right before checking it in the if-statement by calling a function that returns a hex (which is the hexcode for that character in ASCII).

7. Now you have to translate from hex to ASCII for each of the 8 characters, and order them by their offsets in the if-statement.
Ex.
```
cVar1 = function that returns 'I' in hex
if (*(char *)(arg1 + 3) == cVar1)
```
The above excerpt is checking that 'I' is in index 3 of arg1 (the input) since the '+3' is an offset from the base address of arg1. Since indexing starts at 0, this is the 4th character in the input. The other if-statements work by the same logic. Repeat this until you obtain the key code 'OMNICORP'.

8. The function that prints the blueprints (containing the flag as ASCII art) would be a mess to decipher as the ASCII art has been split into many different chunks that then get printed out in order. So you can use the key code you determined in step 7 when you run the executable. The blueprints will then be printed to the terminal, with the flag inside.

## Flag
magpie{s#op_sm4rt_s#op_omni_m4rt}
