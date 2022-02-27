# Tracking a CEO (Part I II III)

### Category: OSINT

### Author: Ejaaz Lakhani (dmsday)

## Description

Mae Jelsworth is supposedly the name for OmniFlags CEO. We have reason to believe this is a fake name. Can you find their real name, and perhaps some flags on the way? 

### Part 1

Your first step: we believe there is some hidden information on an information engine that anyone can easily edit. The problem is there is millions of possible things we can search for. However we do believe that it is something related to Mae. 
 
### Part 2

Great work you found a discord server. Too bad it is password protected. Hence your next step: Find the password. Dont be afraid to go back to the start sometimes these CEO's get careless. 

### Part 3

You did it! Nice work. Your final step is to find Mae's real name. Dont leave any stone unturned. 

## Hints

### Part 1

1. Wikipedia page for Mae's home city 

### Part 2

1. Look into DTMF Tones

### Part 3

1. PGP key directory can take names as well as keys 

## Solution

### Part 1

1. We have a name so let see if there is any social media accounts linked to it

    1. We find a instagram and twitter account

    2. Lets look at twitter first

    3. We find a bunch of weird looking tweets 

    4. Doing some googling we find tht the are encoded to have a secret message hidden withen them. 

    5. We can decode these tweets [here](https://holloway.nz/steg/)

    6. The tweets read:

    ```
    echo Hello Twitter

    I love being CEO

    Home for xmas
    ```

    7. We dont really know where home is lets switch to Instagram maybe something there will help
    
    ...

    8. Lets move on to Instagram

    9. We see a few posts the first of which reads 'echo "Hello Instagram"' along with #Omni. We seem to be in the right place

    10. Theres one more instagram post that catches our eye. One captioned Home - something we saw on twitter - but there is no location so we cant tell where exactly it is. Time for some GEO-OSINT.

    11. Looking at picture we can see a giant sign 2 things

        1. text that looks like 'OPEHAA'

        2. a number that looks like 0504303322

    Theres some text in the middle but we cant make it out.

    12. Googling OPEHAA doesnt seem to give us anything. Lets switch to the number

    13. We find a bunch of links with non english text. 

    14. One article tells us this is located in Lviv Ukraine.

    15. Taking a look at Lviv Wikipeia Page nothing seems out of the ordinary

    16. Lets take a look at edit histroy for christmas (December 25)

    17. Again we get nothing. Doing a little more research we see that Ukraine celebrates christmas on January 7th 

    18. Taking a look at edit history for this date we find a discord link and the first flag.

    ### Part 2

    19. Lets try joining the discord server.

    20. We can join but cant see anything as it is password protected. Lets go back to the instagram. 

    21. After looking at the posts we find a video that was posted captioned "Out to coffee with a CEO friend"

    22. We dont get a name for this CEO friend but a comment left by Mae tells us she was trying to listen to her favourite song but the beeping from her friends phone left her unable to enjoy it.

    23. Perhaps we can find what she was typing to get some information. 

    24. To do this we can make use of [DTMF tones](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) and can use [online tools](http://dialabc.com/sound/detect/) to find what keys were typed. 

    25. All we need is a .wav file to use this tool. So lets go and download the instagram video using [this](https://igram.io)

    26. And we can convert it to a .wav file using 

    ```cmd
    ffmpeg -i input.mp4 output.wav
    ```

    27. We can upload the .wav file and we get the following output

    ```
    9
    9
    5
    8
    6
    6
    4
    7
    ```

    28. At first this doesnt seem to be anything but then we remember that the friend was typing on a flip phone and they had to "type a single number mulitple times for a single letter"

    29. Using a phone keypad to decode this we get

    ```
    xjtngp
    ```

    30. We decoded some text from the instagram video, lets try that to see if it works. It does and we can now read messages on the server. 

    31. Looking at the channel description for #general we see the second flag 


### Part 3

2. We now have access to a private discord server full of "evil CEO's" 

    1. Scroll through message history and we find a post from Mae

    2. The post seems to be laughing at an OmniCorp employee - Myall Snowbird - whom she set up to take the fall for all her illegal work.

    3. We have a new name, lets see if we can find social media linked to this person. 

3. We find a twitter account for Myall

    1. At first it doesnt look like there is much here just two tweets and 1 response to himself. 

    2. Digging around some more we find that the account can hide replies to their tweets. 

    3. Looks like the post has a hidden reply from a user named fla6crea7or. Looks awfully close to flag creator - lets take a look at this account.

4. New Twitter account

    1. This account has some more tweets but none of them are in english. 

    2. Lucky twitter has a feature where you can translate tweets.

    3. The tweets after translating them read 

    ```

    Hello, this is Myall, you found my secret twitter

    I opened this account because I feel I am in danger

    I have a strong feeling that my company is trying to blame me for all its dirty work

    Our CEO is the real culprit. Using a false name so that nothing would be associated with her. Has Pretty Good Privacy.

    Revealing her real name here is too dangerous, but I'll leave you some tips on how to reveal her name. In case I get arrested.

    If you follow the directions, you will find her real name.

    You can use her name to find the flag I stole from her, which has evidence of all her crimes.
    Good luck.

    ```

    4. The last one cant be translated, but we can go to goole translate to find what it says 

    ```
    Your tip: 0xF4793FC7 
    ```

    Looks like a hex value but we dont really know what its for. 

    5. Smart Myall. Looks like he knew he was being set up so he left some clues as to find the real name for Omnicorps CEO. Looks like finding that name will also get us a flag so we seem to be close. 

    6. Looking through the tweets the 4th one in particukar stands out, specifically the last sentence. Why are Pretty Good Privacy capitalized. 

    7. Googling that phrase we see its related to PGP keys which can be assigned to a name/email. Perhaps that is what that hex value was. 


5. PGP Keys

    1. We have a pgp key for the CEO and we can enter it [here](http://keyserver2.pgp.com/vkd/GetWelcomeScreen.event) to find the user asscoaited with it

    2. Enter the key and complete the verification to find a username/email for that key. 

    ```
    Name: OmniCEO
    Email: ther3al0mnic30@gmail.com
    ```

    3. We dont get a real name but we get a email address.

    4. We can use a [reverse email lookup](https://tools.epieos.com/email.php) to see if we can get more information. 

    5. Enter the email address and fail the captcha few times before finally succeeding and we finally find the real name

    ```
    Madelina Saharan
    ```

    6. We have a real name but not a flag but we recall the PGP key directory can also accept names lets try that.

7. Getting the flag

    1. We enter the name - Madelina Saharan - into the PGP directory from earlier 

    2. Complete the verifiction and select Name contains, and enter the name we found

    3. Click enter and we have the flag!

## Flag

part1 flag: magpie{g30_O5in7_is_@w350mE}
part2 flag: magpie{w40_L3akeD_7h3_p@55w0Rd}
part3 flag: magpie{051nt_i5n'7_sT@lk1n6}
