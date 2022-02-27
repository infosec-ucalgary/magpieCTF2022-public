# Out of Mind
### Category: Forensics
### Author: e-seng (Petiole#4224)

## Description
This IP address was found on a napkin that fell out the pocket of a Mom and Pop's client.
We cannot seem to see anything interesting... Are you able to find anything that we can
possibly use?

## Hints
1. What is a good way to get server information?
2. How can a port be further enumerated? Look into arguments of note

## Solution
It's time to do scanning and enumeration

1. Scan the IP address, looking for more ports outside the general 1000.
  - this can be done with `nmap` and the `-p` flag.
  - to scan all ports, `-p-` can be used.
  - to run enumeration scripts, `-sC` should be used
  - as services are linked to non-standard ports, `-sV` should be used to determine which service is running
  - `nmap -p- <ip address>`
2. Wait for the scan to complete
3. Read the scan
```
$ nmap -sV -sC -Pn -p- 10.0.0.224
| Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
| Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-18 14:19 MST
| Nmap scan report for 10.0.0.224
| Host is up (0.0044s latency).
| Not shown: 65532 closed ports
| PORT      STATE SERVICE    VERSION
| 12321/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| | ssh-hostkey: 
| |   3072 1b:fd:c6:88:af:f0:65:58:8e:c5:fe:ac:cf:ee:bf:91 (RSA)
| |   256 a0:6d:55:2b:8d:30:4e:42:ae:d6:95:42:5c:7f:7a:73 (ECDSA)
| |_  256 fd:fa:ad:9d:dc:a1:55:cf:c3:96:77:00:fe:0b:a1:05 (ED25519)
| 59465/tcp open  finger     Linux fingerd
| | finger: Login    Name                    Tty      Idle  Login Time   Office     Office Phone\x0D
| |_myUser   magpie{0u7_0f_$1gh7;)}  pts/0          Jan 18 21:19 (172.17.0.1)\x0D
| Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
| 
| Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
| Nmap done: 1 IP address (1 host up) scanned in 19.09 seconds
```
	- flag is seen within the details of port 59465 in this case.

## Flag
magpie{0u7_0f_$1gh7;)}
