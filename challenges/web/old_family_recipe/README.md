# Old Family Recipe

### Category: Web Exploitation
### Author: Joshua Cordeiro-Zebkowitz (Rasenha)

## Description
Your team has uncovered an old admin login page that Mom & Pops Flag Shop used to run back in the day. They overhauled their website after buying up all those other shops, but rumour has it that an old family flag was left behind. Forge a path, find the flag, and enjoy your baked goods.

## Hints
1. Ever had to forge a signature? Flask gives you good practice.

## Solution

1. When you first enter the site, you'll be met with a login page. Try and login using username: admin and password: admin. (Could change these for anything, doesn't really matter).

2. You'll then see a page saying that the login was incorrect, and to visit one of Mom & Pops' recently acquired companies. In here are a few random names, but one points to 'Robots.txt'.

3. Go to the robots.txt page for the site and you'll find that it tells you that your browser is unsupported and point you towards Internet Explorer 6.01.

3. The User-Agent for IE 6.01 is "Mozilla/4.0 (compatible; MSIE 6.01; Windows NT 6.0)" (from http://www.useragentstring.com/index.php?id=7730)

4. Next you can change your browser's user-agent by (in chromium):
    - Go to 'Inspect'
    - Click on the 3 dots in the right-hand corner
    - 'More Tools'
    - 'Network Conditions'
    - Uncheck 'Use browser default'
    - Enter the User-Agent for IE 6.01

5. Now, reload the page with the new user-agent and you'll find:

```
User-agent: *
Disallow: 
# Dear Pop,
# It was awfully nice of those kinda fellas at Omni to help us out with our website, they told me
# to give them some sorta secret key for the cookies, sounds like they could use a good ol' family recipe.
# Would you be able to pass this secret key onto them?

# flour_sugar_chocolate_and_lotsalove

# Love,
# Mom

# P.S. I think they may be lost in the giggle juice, talking about their flasks...
```

6. There are some interesting words in here that might catch your eye and that relate to websites: cookies, flasks, and secret keys. If you're familiar with flask and how its session cookies work, you'll know that it signs them rather than encrypting, and to do this a "secret key" is used. If not, googling the key terms should get you a page like this one: https://blog.paradoxis.nl/defeating-flasks-session-management-65706ba9d3ce

7. Now you have a the secret key by which the cookies of this site are made: flour_sugar_chocolate_and_lotsalove. To obtain your current cookie, you could use 'Inspect' -> Storage -> Cookies and get the value. This is a Base64 encoding of the session data, a time stamp, and a cryptographic hash.

8. You can decode the cookie to obtain the session data with a tool like cyberchef: https://gchq.github.io/CyberChef/.

```
E.g.

eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiYWRtaW4ifQ.Ya2IDw.nr-R-kOeBryBOrcb6Pp0n8oKSq4

Becomes

{"admin":false,"username":"admin"}..Ø.ð.´d9àkÈ.«q¾.§Iü ¤ªä

```

9. Since this is the admin account you're trying to access, you probably want to set the 'admin' field to 'true'. Unfortunately, you can't just change it to 'true' and send it off in a POST request because Flask still has the SHA1 hash which is based on the session data, the timestamp, and the secret key. Fortunately, Mom's leaked email gave you the secret key!

10. To craft the session cookie, that previous site (https://blog.paradoxis.nl/defeating-flasks-session-management-65706ba9d3ce) gives a good script, into which you just need to add the secret key and some session data for setting admin to true.

```
import hashlib
from flask import Flask
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

session = {"admin":True,"username":"admin"}

def solve():
    s = URLSafeTimedSerializer(
        secret_key='flour_sugar_chocolate_and_lotsalove',
        salt='cookie-session',
        serializer=TaggedJSONSerializer(),
        signer=TimestampSigner,
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': hashlib.sha1
        }
    )
    return s.dumps(session)
```

11. Running this script will give the new session cookie, which you can send to the site by intercepting an HTTP request/using a cookie editor tool.

12. Press 'login' on the login page once that new cookie's been put in and VOILA! The Flag!

## Flag
magpie{d3l1c10u5_h0m3m4d3_c00k1e5}
