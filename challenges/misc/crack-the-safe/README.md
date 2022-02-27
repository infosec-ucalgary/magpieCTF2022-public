# Crack the Safe

### Category: Misc

### Author: Ejaaz Lakhani (dmsday)

## Description

We found a portion of Mom and Pop's old website that was never taken down. Looks like a place thier customers could go to leave comments. Doesnt seem to be working too well.

## Hints

1. Try consulting a certain elephant
2. Firstname Smith can help unlock the ZIPper

## Solution

Navigating to the website, all we see is a boring web page with a text box. Lets try typing some random characters in. Hmmm, it looks like nothing shows up when we are typing.

1. Lets try doing an inspect element and see if we can ggather any information from there.
   - We see some HTML mixed with some javascript
   - The javascript isnt very helpful, lets try looking at different tabs
   - I wonder if there is any useful information in the headers
2. Go to the networks tab and click on the web app
   - Navigate to the the headers along top
   - We see X-Powered-By: PHP/7.2.34 this tells us PHP is running on the site
   - Now that we know PHP running lets see if we can gather any more info or see of wwe cna find the PHP source code
3. Lets navigate to the sources tab
   - Hmmm we see a image file but no image seems to be displayed on the webpage
   - Even more interesting ... its callled nothingHere.png
   - That name is very interesting, and I dont trust it. Let's download the image and see if it contains any hidden data
4. Lets first try a good ol binwalk on the image
   - Run the command binwalk -e nothingHere.png
   - Looks like it extracted a directory called (php) with a text file
   - run cat php/PHPSource.txt
   - AHA we found the PHP source code
5. Looking through this source code looks like the PHP is base64 encoding a zip file.
   - And that base64 encoding is the only thing the text box will accept
   - HMMM a forgotten comment tells the target base64 has length x, I wonder if that is useful
   - That could take a while to get the entire base64 I wonder if theres an easier way
   - AHA, looks like Mom and Pops were still n00bs when the programmed this site or forgot to remove a line that they used to test the site
   - They left an elseif in that will allow us to get the entire base64 if we copy and paste a string longer than the length of the base64
   - Time to scream at the program. Lets make a simple python script to get a long enough string.
     ```bash
     print("a"*length)
     ```
   - Run that python script, copy the output and paste it into the textbox of the website.
   - BOOM we have the base64 encoding of the zip file
6. Searching for base64 to zip file decode we find a site that will quickly do this.
   - Copy the base64 into the input and click decode
   - The webpage gives us an application.zip file to download
   - Downloading the file we see its called flag.zip ... we are so close ... all we have to do is unlock the zip ... and its password protected
   - There is a way to unlock ot of the password is common using John, lets try that
7. Run
   ```bash
   zip2john <zip file> > <output file>
   ```
   - Then run
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt <output file>
   ```
   - This will give us the passowrd for the zip file
   - We are so close run unzip flag.zip and enter the password when prompted
   - The password worked run ls /flag and we see a flag.txt file
   - Run cat flag.txt ... and ... no flag but a link to a Youtube video ...
   - Copy and paste the link, we see a vault opening and ... VIOLA OUR FLAG

## Flag

magpie{j0hN_0f_A11_7r@d35}
