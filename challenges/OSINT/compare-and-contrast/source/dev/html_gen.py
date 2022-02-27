#!/usr/bin/python3

import sys

def main():
    # usage: ./html_gen.py
    # input: a list of names (in any format) and then an email address
    #        (separated by a ' - ')
    # output: some html containing contact information for a given list of names
    #         html is dependent on an existing file with '{}' somewhere in it.
    #         content will be placed at the position of '{}'
    DELIMITER = " - "

    employees_html = open("./public/employees.html", "r").read().split('{}')

    print(employees_html[0].strip())

    for line in sys.stdin:
        name, email = line.strip().split(DELIMITER)
        html_line = f"<tr><td>{name}</td><td>{email}</td></tr>"
        print(html_line)

    print(employees_html[1][1:])

if __name__ == "__main__": main()
