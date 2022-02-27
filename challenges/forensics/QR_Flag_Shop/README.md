# Broken QR

### Category: Misc

### Author: Ejaaz Lakhani (dmsday)

## Description

Mom and Pop are trying to connect more with these youngsters by modernizing the way they sell their flags. They are hoping to have all their flags available as QR codes. Being the old geezers they are they have done something wrong and the QR is broken. Can you help them?

## Hints

1. The QR code is version 3 with mask pattern 2. 
2. [Here is a link](https://www.robertxiao.ca/hacking/ctf-writeup/mma2015-qrcode/) to a writeup for a similar challenge

## Solution

This challenge will require reading up on how QR codes are structured. Theres a great QR code tutorial on how they are structred outling [7 key steps](https://www.thonky.com/qr-code-tutorial/introduction). 

1. Data Analysis
2. Data Encoding
3. Error Correction Coding
4. Structure Final Message
5. Module Placement in Matrix
6. Data Masking
7. Format and Version info 

Following these steps in reverse (7-1) can help you solve this challenge. 

---

### Version and Format Info 

The QR code version is a reference to the size (LxW) of the QR code in pixels. We have most of the left most column showing which we can count to have 29 pixels. Thus we can gather that this QR code is 29x29 pixels and therefore version 3. 


We can use a [pixel are tool](https://www.pixilart.com/draw/qr-code-c70c8f58df#') to help fill in the missing pixels of the QR code as we go along. Open up the link click file icon and then new. Fill in 29px for both column and rows and click create. Then fill in the pixels that are provided in the png file we are given. 


All QR codes also have the same "finder pattern"  in the top corners as well as the bottom left corner so we can go ahead and fill those pixels in. These finder patterns are surrounded bu white pixels called seperators, which we can also fill in. All QR codes also have an "Alignment" whose bottom right corener is the 4th pixel from right and 4th pixel from bottom. 


Doing some reading we discover all QR codes also share a "timing pattern" which connect the finder patterns. These can be found on 6th row from left and 6th column from top (coutning from 0). Moreover, these patterns alternate between white and black pixels for the enitre row so lets fill those in. 


Finally the last patterns we can fill in at this step are the "format pattern" and the "dark module".

The format patern is a pattern of 15 bits paced below and to the right of the top left finder pattern, as shown in image below. 

The first 7 correspond the the 7 bits to the right of bottom left finder pattern and the last 8 correspond to the 8 bits below the top right finder pattern. 


![alt text](https://www.thonky.com/qr-code-tutorial/format-layout.png "QR code structure")


Finally all QR codes also have a 'dark module", or black pixel at the coordinates (8, 4*version + 9). Since we have a version 3 QR our dark pixel will be at (8, 21) so we can fill that in. (Again remember to count from 0). 


![alt text](https://www.thonky.com/qr-code-tutorial/function-patterns.png "version and format info")
 

After the above steps we try scanning it with no luck, so lets keep going. 

---

### Data Masking 

Using the 15 bits from the format pattern we can use the following [table](https://www.thonky.com/qr-code-tutorial/format-version-tables) to find the mask pattern as well as the ECC Level (Error Correction Coding Level) which will be used later. 

Here the 15 bits are [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1] which corresponds to an ECC of Q and a mask pattern of 2. 

We look up mask patterns and find some useful info. Mask patterns refer to a formula which is used to determine wether or not you change the colour of the corresponding bit. 
We preform an XOR using the mask pattern along with our QR code. 

Note that you do not apply this to the finder patterns, timing patterns, separators, alignment patterns we did in the previous step.

There are 8 different mask patters (shown below), in our case we are using mask pattern 2 which means every 3rd column is masked. 

![alt text](https://imgs.developpaper.com/imgs/29896-20191016211239895-2078870481.png "mask types")

Thus we go to our QR code and starting from the very first column on left (column 0 as ) mod 3 = 0) we invert all bits excluding the finder pattern. We do this for every 3rd column where ColumnNumber mod 3 = 0. Once we are done we should have something that looks like this. 

---

### Module Placement in Matrix

The bits are placed within the QR code in a snake like pattern starting at the bottom right corner and moving through untill all squares are filled. The bits are packed in sizes of 8 bit units. The following 2 diagrams show the pattern of packing the bits as well as the boundary values for a version 3 QR code. 

![alt text](https://www.thonky.com/qr-code-tutorial/data-bit-progression.png "module placement")


![alt text](https://datagenetics.com/blog/november12013/zig.png "version 3")

While this image (above) does show the formatting for a version 3 QR code. The error correction level is H, while we have a level Q. So we must slightly alter what each box represents. 

From this [table](https://www.thonky.com/qr-code-tutorial/error-correction-table) we see a 3-H QR code has 26 data bytes and (22*2) or 44 error bytes giving a total of 70 bytes as is represented in the picture. Since we instead are using 3-Q we instead have 34 data bytes and (18*2) or 36 error bytes still giving us a total of 70 bytes. Since we still have the same number of bytes the only corrections we need to make are as follows. 

```
{
    D1-D13 stays the same

    E1-E4 becomes D14-D17

    D14-26 becomes D18-D30 

    E23-E26 becomes D31-D34

    E5-E22 becomes E1-18 and

    E27-E44 becomes E19-36 
}
```

Now that we have restructured the information, we can start reading all the bits we know, which gives us the follwing.

We have a TON of missing bits, no wonder we cant read the message. Lets work on filling those in. 

Here are the bits we can read off subbing in a ? for any missing bits

```
{
    [0 1 0 0 0 0 0 1] - D1

    [? ? ? ? ? ? ? ?] - D18

    [1 0 0 1 0 1 1 0] - D2

    [? ? ? ? ? ? ? ?] - D19

    [1 1 0 1 0 1 1 0] - D3

    [? ? ? ? ? ? ? ?] - D20

    [0 0 0 1 0 1 1 0] - D4

    [? ? ? ? ? ? ? ?] - D21

    [0 1 1 1 0 1 1 1] - D5

    [? ? ? ? ? ? ? ?] - D22

    [0 0 0 0 0 1 1 0] - D6

    [? ? ? ? ? ? ? ?] - D23

    [1 0 0 1 0 1 1 0] - D7

    [? ? ? ? ? ? ? ?] - D24

    [0 1 0 1 ? ? ? ?] - D8

    [? ? ? ? ? ? ? ?] - D25

    [? ? ? ? 0 1 1 0] - D9

    [0 0 1 0 ? ? ? ?] - D26

    [? ? ? ? ? ? ? ?] - D10

    [? ? ? ? ? ? ? ?] - D27

    [? ? ? ? ? ? ? ?] - D11

    [? ? ? ? ? ? ? ?] - D28

    [? ? ? ? ? ? ? ?] - D12

    [? ? ? ? ? ? ? ?] - D29

    [? ? ? ? ? ? ? ?] - D13

    [? ? ? ? ? ? ? ?] - D30

    [? ? ? ? ? ? ? ?] - D14

    [? ? ? ? ? ? ? ?] - D31

    [? ? ? ? ? ? ? ?] - D15

    [? ? ? ? ? ? ? ?] - D32

    [? ? ? ? ? ? ? ?] - D16

    [? ? ? ? ? ? ? ?] - D33

    [? ? ? ? ? ? ? ?] - D17

    [? ? ? ? ? ? ? ?] - D34

    [0 1 0 0 0 0 1 1] - E1

    [0 0 0 0 ? ? ? ?] - E19

    [? ? ? ? ? ? ? ?] - E2

    [? ? ? ? ? ? ? ?] - E20

    [0 0 0 1 0 1 0 1] - E3

    [? ? ? ? ? ? ? ?] - E21

    [? ? ? ? ? ? ? ?] - E4

    [? ? ? ? ? ? ? ?] - E22

    [1 0 1 1 1 1 1 0] - E5

    [0 1 1 0 1 0 0 0] - E23

    [? ? ? ? ? ? ? ?] - E6

    [? ? ? ? ? ? ? ?] - E24

    [0 1 0 1 0 0 0 1] - E7

    [0 1 1 0 0 0 0 0] - E25

    [? ? ? ? ? ? ? ?] - E8

    [? ? ? ? ? ? ? ?] - E26

    [1 1 1 1 1 1 0 0] - E9

    [1 0 0 1 1 0 1 1] - E27

    [0 1 0 1 1 0 0 0] - E10

    [1 0 1 0 0 0 0 0] - E28

    [? ? ? ? ? ? ? ?] - E11

    [? ? ? ? ? ? ? ?] - E29

    [? ? ? ? ? ? ? ?] - E12

    [1 0 1 1 0 1 0 0] - E30

    [? ? ? ? ? ? ? ?] - E13

    [0 0 1 0 1 0 0 0] - E31

    [1 0 1 0 0 1 1 0] - E14

    [? ? ? ? ? ? ? ?] - E32

    [? ? ? ? ? ? ? ?] - E15

    [? ? ? ? ? ? ? ?] - E33

    [? ? ? ? ? ? ? ?] - E16

    [0 1 1 1 1 1 1 1] - E34

    [0 0 0 0 1 1 0 1] - E17

    [? ? ? ? ? ? ? ?] - E35

    [? ? ? ? 1 0 1 1] - E18

    [0 1 0 0 1 1 1 0] - E36
}
```

---

### Structuring the final message

As this is a version 3 QR we will have to restructure the bits to get the final message. 

Recall our message is 25 bits. Using the legend in this picture

![alt text](https://datagenetics.com/blog/november12013/zig.png "version 3")

and this [table](https://www.thonky.com/qr-code-tutorial/error-correction-table)

we can see how our message will be structured. The data in this message is split into 2 blocks with corresponding error bytes

Block 1: D1-D17, E1-18 

Block 2: D18-34, E19-E36

So the first part of our message is in D1-D17 and the second half is in D18-D36.

---

### Data Encoding

Lets see if we have enough to get the flag without having to preform error encoding.

From this [link](https://www.thonky.com/qr-code-tutorial/data-encoding) we see more information on data and error encoding of a QR code.

Lets scroll down to Step 3. We see that each QR code has a mode indicator which identifies how the data is encoded. The first 4 bits on every QR code identifies the mode being used. 

For our QR code the first 4 bits are [0 1 0 0] which indictaed Byte mode encoding. 

Continuing to Step 4 we see the next n bits identify the character count (or the length of our string). Where n represents a n bit binary dependent on the QR code version and encoding.

Recall we have a version 3 QR code with Byte more encoding so according to the table, the next 8 bits identify the length of the message. 

For us, folling the restructuring mentioned earlier, the 8 bits are [0 0 0 1 1 0 0 1]. Decoding from binary we get 25 indicatinga 25 character string. 

Reading more into byte mode encoding [here](https://www.thonky.com/qr-code-tutorial/byte-mode-encoding) we see that each character in the message is represented by a 8bit binary value. 

Using all this inofrmation we gathered lets start reading the message

```
{
    [0 1 0 0]           - MODE INDICATOR

    [0 0 0 1 1 0 0 1]   - CHARACTER COUNT (25)

    [0 1 1 0 1 1 0 1]   - m

    [0 1 1 0 0 0 0 1]   - a

    [0 1 1 0 0 1 1 1]   - g

    [0 1 1 1 0 0 0 0]   - p

    [0 1 1 0 1 0 0 1]   - i

    [0 1 1 0 0 1 0 1]   - e

    [? ? ? ? ? ? ? ?] 

    [0 1 1 0 ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? (end of block 1

    start of block 2) ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  
        
    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? 0 0 1 0] 

    [? ? ? ? ? ? ? ?]   - }
            
    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]

    [? ? ? ? ? ? ? ?]

    [? ? ? ? ? ? ? ?]

    [? ? ? ?]
}
```

WHAT A TROLL! We are only given enough data to get the part of the flag we already know. Lets see if we can structure the final message and apply so we can use our error encoding to figure out the rest.

According to this [table](https://www.thonky.com/qr-code-tutorial/error-correction-table) a version 3 format Q QR code gives us 34 bytes or 272 bits of data and 36 bytes or 288 bits of error data for a total of 70 bytes or 560 bits. (280 bits in each block)

We currently have 

```
{
    Block 1: 

    4 bits from Mode Indicator

    8 bits from Character Count

    52 bits from message

    68 bits from error

}
```
```
{
    Block 2: 

    4 bits from message

    68 bits from error
    
}
```

Looks like we are still missing a lot of data so we will likely have to do error encoding. 

---

### Error Encoding

We are using Q level error encoding which can account for 25% of missing data. However accoding tot he site, applying reedSolomon formula can double the bits we get back from error encoding allowing us to be missing a maximum of 50% of the bits per block. 

Lets start with block 1 as we are missing fewer bits there. 

132 of the 280 bits. We need 50% or 140 to preform error ecoding so we are only missing 8 bits. So far in our message we have magpie ... and we know what comes next. a '{'. 

Translating from binary we get 01111011. So now block 1 data bits looks like The first 4 bits should be added at the end of the D8 block and the last 4 bits should be added to the begninning fo the D9 block.

``` 
{
    [0 1 0 0]           - MODE INDICATOR

    [0 0 0 1 1 0 0 1]   - CHARACTER COUNT (25)

    [0 1 1 0 1 1 0 1]   - m

    [0 1 1 0 0 0 0 1]   - a

    [0 1 1 0 0 1 1 1]   - g

    [0 1 1 1 0 0 0 0]   - p

    [0 1 1 0 1 0 0 1]   - i

    [0 1 1 0 0 1 0 1]   - e

    [0 1 1 1 1 0 1 1]   - {

    [0 1 1 0 ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ?
}
```

Now that we have enough bits to error encode part 1 lets see if we can fix part 2. 

So far for part 2 we have only 72 of the required 280 bits. Meaning we need to somehow recover 68 bits! Lets start slowly and take it step by step.

Firstly we know the flag ends with '}' but we dont know where this will go. Or do we?

Recall the flag is 25 bits long. Counting out the bits we can find where it goes and place the binary value for the '}' (01111011) in the corresponing place. The first 4 bits should be added at the end of the D26 block and the last 4 bits should be added to the begninning fo the D27 block.

That goes almost in the middle if that block. Then what would the bytes at the end be? 

Doing some more reading on the website, specifcially this [page](https://www.thonky.com/qr-code-tutorial/data-encoding) we can figure this out pretty easy and see we can recover a bunch more bytes. 

First we must pad with 0's until the length at that point is evenly divisble by 8. This means we add 4 0's. These should be added the the end of the D27 block.

Now for part 2 of 2 we add the pad bytes which is a pattern of 16 bits we keep repeating untill we reach the max length of the message. The 16 bit pattern is 11101100 00010001. We can fill D28-D36 with these bytes. 

After all those steps, part 2 data bits should look like this. 

```
{
    ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  
        
    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?]  

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? ? ? ? ?] 

    [? ? ? ? 0 0 1 0] 

    [0 1 1 1 1 1 0 1]   - }

    [0 0 0 0]           - add 0's to end to make length divisible by 8 

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

}
```

We now have 72 data bits + 68 error bits giving us the required 140 bits for error correction in block 2. 

Now that both block 1 and block 2 have only half their bits missing we can preform error correction. 

---

### Error Correction

Looking on the [error correction page](https://www.thonky.com/qr-code-tutorial/error-correction-coding) we see they are preforming ReedSolomon error correction whohc looks super complicated. thankfully, there exists a handly python library that can do all these calculations for us. 

Doing some more digging we even find an [example code](https://github.com/pwning/public-writeup/blob/master/mma2015/misc400-qr/rs_recover.py) for a QR code error encoding. All we have to do is make it work for our QR code. 

You can download the required python library using

```cmd
    pip install reedsolo==1.4.3
```

Now lets start modifying the code to make it work for us. 

Firstly we are running using python3 so we need to modify the print statement to be 

```python
    print('{:08b}'.format(c))
```

Moving on, the next part we need to fix comes from reedsolo.rs_correct_msg. Using the reedsolo library we see the second argument this takes is the # of error bytes, in our case we have 18 not 22 so we adjust this line to read as

```python
    mes, ecc = reedsolo.rs_correct_msg(part1, 18, erase_pos=erasures)
```

Finally, we, of course, need to edit the data we are passing in. We don't want someones old used data. 

Recall we have 2 code blocks.

Block 1: D1-D17 and E1-E18

Block 2: D18-D34 and E19-E36

we create 2 qr blocks to contain the following data and get our final code. (Can be found in error_solve.py)

Now running the code 

```cmd
    python3 error_solve.py
```

We get the following output.

```
{
    01000001
    10010110
    11010110
    00010110
    01110111
    00000110
    10010110
    01010111
    10110110
    10100111
    01010011
    01010011
    01110101
    11110011
    01110110
    10000011
    00110101
    11110111
    01110100
    00000111
    10010101
    11110101
    00010101
    11110011
    01000101
    00100111
    11010000
    11101100
    00010001
    11101100
    00010001
    11101100
    00010001
    11101100
}
```

Its all the bits, and it looks so beautiful I could just take a byte out of it. All we need to do now is deocde it and we get our flag.

```
{
    [0 1 0 0]

    [0 0 0 1 1 0 0 1]   - Character count

    [0 1 1 0 1 1 0 1]   - m

    [0 1 1 0 0 0 0 1]   - a

    [0 1 1 0 0 1 1 1]   - g

    [0 1 1 1 0 0 0 0]   - p

    [0 1 1 0 1 0 0 1]   - i

    [0 1 1 0 0 1 0 1]   - e

    [0 1 1 1 1 0 1 1]   - {

    [0 1 1 0 1 0 1 0]   - j

    [0 1 1 1 0 1 0 1]   - u

    [0 0 1 1 0 1 0 1]   - 5

    [0 0 1 1 0 1 1 1]   - 7

    [0 1 0 1 1 1 1 1]   - _
    
    [0 0 1 1 0 1 1 1]   - 7

    [0 1 1 0 1 0 0 0]   - h

    [0 0 1 1 0 0 1 1]   - 3

    [0 1 0 1 1 1 1 1]   - _

    [0 1 1 1 0 1 1 1]   - w

    [0 1 0 0 0 0 0 0]   - @

    [0 1 1 1 1 0 0 1]   - y

    [0 1 0 1 1 1 1 1]   - _

    [0 1 0 1 0 0 0 1]   - Q

    [0 1 0 1 1 1 1 1]   - _

    [0 0 1 1 0 1 0 0]   - 4

    [0 1 0 1 0 0 1 0]   - R

    [0 1 1 1 1 1 0 1]   - }

    [0 0 0 0]           - add 0's to end to make length divisible by 8 

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

    [0 0 0 1 0 0 0 1]   - extra padding for full length

    [1 1 1 0 1 1 0 0]   - extra padding for full length

}
```

And we have our flag. 

## Flag

magpie{ju57_7h3_w@y_Q_4R}
