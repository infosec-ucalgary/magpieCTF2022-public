# Last Act of Defiance

### Category: Web Exploitation
### Author: Greg Vance (Expergefied)

## Description
We received a message from the founder of Flag West. They said that there was one flag that they were able to hide before Mom & Pops got them all. The message said that it is hidden somewhere in the website, and that you just need to inspect it a little. Flag West was one of the first aquisitions that Mom & Pops made, so it is surprising to hear that there still might be a flag left. Get in there and find that flag, make Flag West's last act of defiance worth something.

## Hints
1. Use Dirb

## Solution
1. The flag is broken up into three parts that can be found by inspecting the code.
2. The first part is found as a comment within the HTML.
3. The second part of the flag is found as a comment in the style.css file
4. By using Dirb the thrird part of the flag can be found in the path academic/developers/secrets/final.txt
5. Combine all of the parts for the full flag submission

## Flag
magpie{w3_5pi7_1n_7h3_f4c3_0f_7yr4nny}
