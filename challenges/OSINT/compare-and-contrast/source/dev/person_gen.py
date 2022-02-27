#!/usr/bin/python3

import sys
import requests
import json
import random

def main():
    # usage ./person_gen.py <NUMBER OF PEOPLE>
    # prints names, emails to stdout
    # prints in the form : "<LAST NAME>, <FIRST NAME> - <EMAIL>

    if len(sys.argv) < 2:
        print("USAGE:", sys.argv[0], " <NUMBER OF PEOPLE>")
        return -1

    # list of names retrieved from https://www.randomlists.com/fake-name-generator
    # first names
    fn_res = requests.get("https://www.randomlists.com/data/names-first.json")
    first_names = json.loads(fn_res.text)["data"]

    ln_res = requests.get("https://www.randomlists.com/data/names-surnames.json")
    last_names = json.loads(ln_res.text)["data"]

    # randomly pair a first name with a last name.
    for _ in range(int(sys.argv[1])):
        fn = first_names[random.randrange(0, len(first_names))]
        ln = last_names[random.randrange(0, len(last_names))]
        email = f"{fn[0:3]}.{ln}@momandpopsflags.ca".lower()
        print(f"{ln}, {fn} - {email}")

if __name__ == "__main__": main()
