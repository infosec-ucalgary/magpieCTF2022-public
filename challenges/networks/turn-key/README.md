# Turn Key
## Category: Networks
## AUTHOR: James Lowther (Articuler) & Jeremy Stuart (Mr.Wizard)
## Description
Mom & Pops most prized possession is their First Flag.  The OG flag.  The flag that started their entire business!  Mom wrote it herself!  Now that they are rich and powerful, they fear someone might try to steal it and so they had their programming team come up with a way to keep the First Flag safe.  They split it into three pieces and stored it in three different vaults around the world.  Only if you turn the key on all three vaults at the same time can you get the flag.  Obviously that's impossible...or is it?

Find the turn key protocol documentation here: momandpopsflags.ca/turn-key

## Hints
1. The flag is encrypted using AES, but you can get everything you need to decrypt it.  CyberChef has a nice tool for AES decryption if you need one!
2. Where are the "vaults" (servers) located?  

## Solution
1. The first problem is that you're given addresses but don't know which port to interact with.  The answer is to nmap the "vaults".  You would find a number of ports open - some of them were for infrastructure for the CTF - but if you did a service and script scan you should notice that port 5555 is returing `oh hai!` which is part of the protocol.  Finding this, you can find the protocol is running on port 5555 on all of the "vaults".

2. The turn key protocol is pretty simple.  You can run it by hand using netcat, but you're probably going to run the protocol too slow to have it work.  The solution to this problem is to script the protocol (we used pwntools) so that the time it takes from start to finish is fast enough to get the piece of the flag.  Run this solve script against the three "vaults" (servers).

3. Now you'll notice that the solve script should only work for one - possibly two - servers, the rest should say you were too slow.  Why?  The answer is that the servers you are interacting with are literally located in different places around the planet.  If you lookup the IP addresses for the vaults, you'll find that the servers are in San Fransisco, Amsterdam, and Bangalore.  If you run the script on your computer, the time it takes for the messages in  the protocol to go between the three servers will be different depending on how far away the vault is from you.  San Fransisco is likely the one you can get the most often if you're in North America.  Amsterdam and Bangalore are too far away, and so the transit time for all the messages in the protocol take too long getting to and from the server to finish the protocol in time.  *womp womp*

4. The only way to decrease the transit time of the messages is to be closer to those servers, and that's the intended solve.  You need to get machines that are running close enough to San Fransisco, Amsterdam, and Bangalore to complete the turn key protocol and get the encrypted flag and the decrpyt information.  We tested by starting cloud servers using Linode in Frankfurt and Mumbai.

5. The other problem is that the servers rotate the encryption key and IV every 2.3 seconds to make sure that all the keys need to be turned at - relatively - the same time.  So you need to make sure all three solve scripts are running at the same time, otherwise the encryption will be rotated and you won't get the same encryption for the three parts of the flag.  You need to run the protocol on all three machines within the same 2.3 second window.  We did this using cron jobs to try to make sure we used the system time on the computers.  System time on computers isn't *perfectly* in sync, but it's close enough that they should all run within the same 2.3 seconds.  When we tested the challenge, we aimed to have it be successful at least 85% of the time.  Accounting for differences in the system time, 2.3 seconds should be enough!

6. Once you have all the encrypted flags, the IVs, and the three pieces of the keys you can decrypt the flag!  (We used the AES feature in CyberChef)

## Flag
magpie{tH15_b3tT3R_f**k1n9_w0Rk_p0p...}
