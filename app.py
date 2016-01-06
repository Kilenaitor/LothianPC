#!/usr/bin/env python

from colorama import Fore, Back, Style
from getpass import getpass as getswipe
import os
import re
import time

'''
Extracts name from r'card swipe
string
@param carddump {String}
@return {String, None}
'''

def parse_name(carddump):
    # Last Name is after a ^ symbol
    # First name is after a /
    # Characters are in carddump
    name = ""

    regex = '\^(.*?)/'

    # There should only be one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        name += matches[0]
    else:
        return None

    regex = '/([^\s]+)'
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        name = matches[0] + " " + name
    else:
        return None

    return name.title()


'''
Parse id from r'card swipe
int
@param carddump {String}
@return {int, None}
'''

def parse_id(carddump):
    #ID follows a string of 6 zeros, and is 9 numbers long

    regex = '000000([0-9]{9}).*'

    # There should only be one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        return matches[0]
    else:
        return None


'''
Extracts r'card number from card swipe
string
@param carddump {String}
@return {String,None}
'''


def parse_number(carddump):
    # R'card number is always 16 numerical digits
    # long and starts with %B. %B should be the first
    # characters in carddump
    regex = '%B([0-9]{16}).*'

    # There should be only one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        return matches[0]
    else:
        return None


'''
Print strings in different colors
@param string {String}
@return none
'''

def print_error(string):
    print '{}{}{}{}'.format(Fore.RED, Style.BRIGHT, string, Style.RESET_ALL)


def print_success(string):
    print '{}{}{}{}'.format(Fore.GREEN, Style.BRIGHT, string, Style.RESET_ALL)


def print_status(string):
    print '{}{}{}{}'.format(Fore.CYAN, Style.BRIGHT, string, Style.RESET_ALL)

'''
Ask for string input
@param request {String}
@return {String}
'''

def get_info(request):
    response = raw_input('{}{}{}{} => '.format(Fore.YELLOW, Style.BRIGHT, request, Style.RESET_ALL))
    return response

if __name__ == '__main__':

    # Main event loop
    while 1:
        os.system('clear')

        card_dump = getswipe("Swipe R'card\n")
        card_number = parse_number(card_dump)

        # If we were NOT able to get a valid number
        # from the swipe, let the user know and skip everything
        # else
        if card_number is None:
            print_error("Invalid swipe. Try again")
            continue

        name = None
        s_id = None

        # Get name and email
        #name = get_info("Enter your full name")
        name = parse_name(card_dump)
        s_id = parse_id(card_dump)

        # Break out if student is content
        with open('program_attendance.txt', 'a+') as f:
            f.write(name + " " + s_id + "\n")

        print_success("Successfully checked in {}.".format(name))

        # Some sleep so person can see results
        time.sleep(2)
