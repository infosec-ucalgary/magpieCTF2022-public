# Compare and Contrast
### Category: Forensics
### Author: e-seng (Petiole#4224)

## Description
An anonymous messenger sent us this website. Explore the site and see what
secrets it holds.

## Hints
1. https://youtu.be/i9CBKGLVCME
2. order matters with the initials, both between names and between first and last names
3. nth character rotates by the nth value in ascending order

## Solution
This would be the solution to the challenge!

1. Explore the provided "terminal"
  - Typing in `help` provides commands
  ```
  > help
  help    -  this help menu
  sites   -  links of importance
  solve   -  attempt to guess the passphrase
  ```
  - typing in `sites` provides links to websites, some that are already possibly
    known
  ```
  > sites
  http://momandpopsflags.ca
  http://omniflags.com
  ```
2. Explore the HTML of the page
  - In the background of the terminal, there is some weird text that is revealed
    in the page source.
  - this gives
  ```
  4f 6e 6c 79 20 74 72 75
  73 74 20 74 68 65 20 63
  6f 6d 62 69 6e 65 64 20
  69 6e 69 74 69 61 6c 73
  20 6f 66 20 77 6f 72 6b
  65 72 73 20 61 77 61 79
  20 66 72 6f 6d 20 4f 6d
  6e 69 20 74 6f 70 20 74
  6f 20 62 6f 74 74 6f 6d
  2e 20 54 68 65 79 20 73
  68 69 66 74 20 62 79 20
  6e 75 6d 62 65 72 73 20
  77 69 74 68 20 66 6f 72
  74 75 6e 65 2c 20 62 75
  74 20 6e 6f 74 20 62 79
  20 74 68 6f 73 65 20 74
  68 61 74 20 61 72 65 20
  70 72 69 6d 65 73 20 6f
  66 20 74 68 65 20 6c 75
  6e 61 72 20 61 6c 67 6f
  72 69 74 68 6d 2e
  ```
  and
  ```
  aHR0cHM6Ly9naXRodWIuY29tL21vbW5wb3BzZGV2dGVhbS9tb21ucG9wc193ZWJzaXRl
  ```
    - When decoded, these resolve to
    ```
    Only trust the combined initials of workers away from Omni top to bottom.
    They shift by numbers with fortune, but not by those that are primes of the
    lunar algorithm.

    (hex -> ascii)
    ```
    and
    ```
    https://github.com/momnpopsdevteam/momnpops_website
    ```
3. Solve the provided riddle, found within the hex.
  - "Only trust the [...] workers away from Omni"
    - this indicates to determine the employees who are working in Mom & Pops,
      but do not work in Omniflags.
  - "trust the combined initials of workers [...] top to bottom."
    - this indicates to use the initials of the employees in order as they
      appear, in some combinational way. In this case, it is through string
      concatenation.
    - eg. if names were "Lulu Miller" and "Anston Oeren", they would be combined
      to make `lmao`.
  - "They shift by numbers with fortune, but not by those that are primes of
    the lunar algorithm."
    - implies a letter rotation over a list of numbers.
    - the list of numbers is given by the list of [Fortunate Numbers](https://oeis.org/A005235)
      (numbers with fortune) without the list of [Lunar Primes](https://oeis.org/A087097)
    - in this case, each character would be rotated by a unique integer within
      the list as defined above.
      - the 0th-index character would be rotated by the 0th-index number within the list.
4. Retrieving the list of employees within Omniflags and Mom & Pops Flag Shop
  - Omniflags' employee list is publicly listed for (?)
  - Mom & Pops Flag Shop's employee list requires some additional digging
  1. When retrieving the base64 with the GitHub link, there is a comment stating
  ```HTML
  <!--Reminder: Pages of the past still exist-->
  ```
    - this indicates that old pages likely still exist on the current hosted page,
      even if they are not directly linked to.
  2. Following the GitHub link, there is a change log. One states `Remove hidden address`
    - The page link was removed in this github repository, but was done so as a git commit.
    - GitHub allows previous commits to be viewed.
      - Reading commit `32e27fabff76f4efc6376f9797abd8b3de59c994` shows that a page link
        `/momandpops-employees` was removed.
    - going to `http://momandpopsflags.ca/momandpops-employees` gives their current employees.
  3. Both lists of employees can be compared to determine which employees are unique
    to Mom & Pops Flag Shop.
    - within this repository, there is a python3 script containing a function that does this
    - `./source/dev/encode_message.py`, which should be run interactively within
      `./source/dev`.
      - (ie. `./source/dev$ python3 -i encode_message.py`)
    - the line of note is 91
      - `unique_names = [names for name in mompops_names if name not in omni_names]`
    - line 92 reverses the names to be in proper format
      - (from `Last-name, First-name` to `First-name Last-name`)
5. The list of initials may be retrieved and parsed
  - Initials are determined by the first character of an individual's first and
    last name, in that order.
  - thus, the ciphertext may be determined by finding each individual's initial
    in order of appearance and concatenating them together.
  - within the python3 script at `./source/dev/encode.py`, this is done on lines
    97 to 103.
6. Determine the set of values to rotate each character by
  - From the hint, it may be determined that Fortunate Numbers and Lunar Primes are needed.
  - Specifically, Fortunate Numbers not found within the set of Lunar Primes
    define the list.
  - thus, the list of values can be determined by creating a new set with Fortunate
    Numbers, but without Lunar Primes.
  - this is done on lines 6 to 31 within `./source/dev/encode_message.py`
7. Each character of the cipher text may be rotated by each number within the list
  - the n-th character of the ciphertext is rotated by the n-th value within the
    list of values.
  - this is done via the `decode_message(...)` function within `./source/dev/encode_message.py`
    between lines 54 - 77
  - this returns some readable pattern, `omniflagsstoleallcontrol`
8. This string may now be entered into the terminal.
  - the `solve` command may be entered into the terminal
    - this will prmopt for the cipher text, which is the concatenated string of employee
      initials. (`lhgviudvjdkvqbrmqnroucrw`)
    - if the ciphertext is correct, then the passphrase may be entered
      - `omniflagsstoleallcontrol` may be entered into the terminal
  - this dumps text with some story onto the screen, giving the flag.

## Flag
`magpie{|\/|ix1ng_|\|umb3r$_t0g3t43r}`
