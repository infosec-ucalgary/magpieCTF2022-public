# Magpie2022 - Blame the Intern
### Category: Web
### Author: Josh Novak (rm -rf /)
---
## Description
"It was the intern" said Jimmy. His boss was not happy. A vulnerable web application was hosted on company servers. See if you can find the flag using the interns app.

---
## Hints
1. Luckily, the intern was vaccinated. He got his INJECTION recently.

---
## Solution
1. Download app.py and examine the render function
2. Determine that template injection is possible when passing things in the textbox
3. Input `{{ state.flag }}` (you could also do `{{ state }}` and get the flag)

---
## Flag
magpie{tr34t_y0ur_1nt3rn5_n1c3ly}
