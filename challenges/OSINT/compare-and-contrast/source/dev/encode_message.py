#!/usr/bin/env python3
"""
This python file contains all the necessary function to encode and decode the
messages found on within this challenge
"""
import re

fortunate_nums = [
        3, 5, 7, 13, 23, 17,
        19, 23, 37, 61, 67,
        61, 71, 47, 107, 59,
        61, 109, 89, 103, 79,
        151, 197, 101, 103, 233,
        223, 127, 223, 191, 163,
        229, 643, 239, 157, 167,
        439, 239, 199, 191, 199,
        383, 233, 751, 313, 773,
        607, 313, 383, 293, 443,
        331, 283, 277, 271, 401,
        307, 331
        ]
# from https://oeis.org/A005235

lunar_primes = [
        19, 29, 39, 49, 59,
        69, 79, 89, 90, 91,
        92, 93, 94, 95, 96,
        97, 98, 99, 109, 209,
        219, 309, 319, 329, 409
        ]
# from https://oeis.org/A087097

rot_set = [x for x in fortunate_nums if x not in lunar_primes]

def encode_message(message):
    """
    The script to encode the provided message.

    essentially the decode message, but done in reverse.
    """
    encoded_msg = ""

    for i, c in enumerate(message):
        c = c.lower()

        # get the position of the letter within the alphabet
        char_num = ord(c) - ord('a') # 'a' will be 0

        # perform the rotation
        rot_char_num = abs(char_num + (26 - rot_set[i]) % 26) % 26

        print("[encode] rotating:", f"{c} ({char_num})", "by", (-rot_set[i] + 26), "->", rot_char_num)
        encoded_msg += chr(rot_char_num + ord('a'))
    return encoded_msg

def decode_message(encoded_msg):
    """
    This is an expected script to decode a given encoded message.

    basically, just a rotation by some value n_i, where i is an element of
    [0, len(encoded_msg)) and n_i is the ith element of fortunate_nums intecepted
    with elements not found in lunar_primes.
    """
    message = ""

    for i, c in enumerate(encoded_msg):
        c = c.lower()

        # get the position of the letter within the alphabet
        char_num = ord(c) - ord('a') # 'a' will be 0

        # perform the rotation
        rot_char_num = (char_num + rot_set[i]) % 26

        print("[decode] rotating:", char_num, "by", rot_set[i], "->", rot_char_num)

        message += chr(rot_char_num + ord('a'))

    return message

def get_unique_names(mompops_file, omni_file):
    mompops_employees = open(mompops_file, 'r')
    omni_employees = open(omni_file, 'r')

    mompops_names = [name.split(' - ') [0] for name in mompops_employees.read().split('\n') if len(name) > 0]
    omni_names = [name.split(' - ') [0] for name in omni_employees.read().split('\n') if len(name) > 0]

    # print("mom & pops:", mompops_names)
    # print("omni:", omni_names)

    # isolate unique names employed at Mom & Pops and set them to be in a correct form
    # correct form would be "First Last"
    unique_names = [name for name in mompops_names if name not in omni_names]

    print("unique:", unique_names)

    # get initials of remaining employees
    names = []
    for name in unique_names:
        names += name.split(' ')

    initials = [name[0] for name in names]

    ciphertext = ''.join(initials)

    print(ciphertext)

    mompops_employees.close()
    omni_employees.close()

    return ciphertext

# padding messages
def padding(msg):
    add_padd = 8 - len(msg) % 8
    msg = bytes(msg, 'utf-8')
    msg += b'\x00' * add_padd
    return msg

# fix names
def fix_name_order(filename):
    updated_details = ""

    with open(filename, "r") as emp_file:
        employee_details = emp_file.read().split('\n')

        for index, employee_det in enumerate(employee_details):
            employee_list = re.split(", | - ", employee_det)
            if(len(employee_list) < 3): break
            updated_employee_str = f"{employee_list[1]} {employee_list[0]} - {employee_list[2]}\n"
            updated_details += updated_employee_str

            print(f"writing line {index+1}/{len(employee_details)}", end="\r")

        print("\nfinished!")

    with open(filename, "w") as emp_file:
        print("writing...")
        emp_file.write(updated_details)

def main(): # this is here to double check if everything has gone well
    msg = decode_message(get_unique_names("./mompops_employees.txt", "./omni_employees.txt"))
    print(msg)
    return 0

if __name__ == "__main__": main()
