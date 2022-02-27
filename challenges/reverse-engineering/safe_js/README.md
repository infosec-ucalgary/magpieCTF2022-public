# Safe.js
### Category: Reverse Engineering
### Author: e-seng (Petiole#4224)

## Description
When poking around some of the old servers Mom and Pop were running, this link
found to be pretty interesting. Unfortunately, the code is completely unknown
to us. Is there a way to get this safe open?

## Hints
1. How do most websites function? Is there a special file that websites use to
perform tasks?
2. Wow, this code is *really* ugly. Is there any way to make it more readable?
3. Are there any functions within the code that could be run by the user?

## Solution
This would be the solution to the challenge!

1. Open the JavaScript the website is using
    * This may be done through a browser's developer tools or through
    identifying source links from `/js/app.js`
    * This returns an obfuscated JavaScript file
2. Beautify the JavaScript file
    * This is typicially done with the appropreate button within a
    browser, but there exist other online tools.
    * This is technically not necessary, but really helps
3. Identify declarations of global functions
    * This includes `openSafe`, `typeNumKey` and `console.log`
    * `console.log` was added to imply these are publicly accessible functions
    * This is found on lines 55 - 58 when obfuscated with FireFox.
    ```js
    // ...
        document['querySelector']('#safe-inner') ['innerText'] = _0x5d88c8;
      }
      window['openSafe'] = _0x2b86cd;
      window['typeNumKey'] = _0x47e16f;
      window['checkCode'] = _0x47e5a0;
      window['console.log'] = console['log'];
    }
    window['addEventListener']('load', () =>{
      f();
      var _0x1dece9 = [
    // ...
    ```
4. The function `openSafe` can be called
    * This opens the safe and reveals the flag

## Flag
magpie{s0m3_08fusC@7i0n,_hvh}
