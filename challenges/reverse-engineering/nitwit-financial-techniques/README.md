# Nitwit Financial Techniques
### Category: Reverse Engineering
### Author: Jeremy Stuart (Mr.Wizard#3743)

## Description
Hello Flag Hunters.  I've been following your team's activities and I'm contacting you because we have a common
goal: bringing down Mom & Pop.  I'm sure you've noticed the damn fools have started selling NFTs...as
if having a monopoly on the flag market wasn't a stupid enough business plan!  I managed to hack into
their system and found that each image has a unique "fingerprint" that prevents others from producing
their own flags, but I couldn't find what the fingerprint actually IS! Luckily I also managed to
exfiltrate the program they're using to generate the flags, but I can't figure out what to do with this
generator file.  That's where you come in.

Reverse this generator, figure out how to get the fingerprint, and then send it to me.  I'll use it to
generate authentic fake NFTs and flood the market with them.  That should crash the price and kill this
idiotic cash cow.

Email the fingerprint as an attachment to vex31337@gmail.com.  I'll reply and let you know if it's the genuine
fingerprint.  I'm sure you're wondering what's in it for you.  I know what motivates you and am ready to
offer you one genuine Mom & Pop flag as payment.

Happy Heisting,
Vex

## Hints

## Solution
1. Try opening the `generator` in a decompiler
2. Find Py strings everywhere.  This is because this is a compiled python file.  It's been done using PyIstaller so that the file can run on it's own like an EXE
3. You can pull the EXE apart to get the bytecode files out of it.  I used  PyInstaller Extractor to do so.
4. This is where things can get really difficult.  This was compiled with Python 3.10, so `uncompyle6` won't be able to translate the byte code back to the source code.  You can go through the byte code by hand and figure it out, or you can add the instructions that are missing and uncompyle it yourself.  I found a way to slice in the missing byte code and have uncompyle6 do it (I have since lost the files I used to do it, sorry!).
5. Once you get the code back, find that fingerprint.png is a layer that's being used to build the flags (the base layer)
6. Examine the flags to find that the "white" base layer is actually random values of rgba between 251-255
7. You can get flags from the Mom and Pops NFT page and this will let you start stripping out those "white" background layers and putting them back together to make the fingerprint.  I just took a LOT of them and did an analysis to figure out which values were the fingerprint values.
8. Use that to reconstruct the "fingerprint"
9. Email it to Vex for your flag in return


## Flag
magpie{8uy_5tUp1d_t3CH_m4K3_5TuP1d_m0N3y}