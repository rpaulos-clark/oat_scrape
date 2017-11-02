from lxml import html
import requests
import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import string

# Newline Extraction Seems to be working dandy. Will need to screen for empty strings and those comprised exclusively of integers
# Also works for program outcomes!!!!
integer_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


# def detect_consecutive_integers(string):
#
#     # Returns a tuple
#     # Detects 4 or more consecutive integers. If detected, will return the slice preceeding the consecutive integers
#     # and the slice following the consecutive integers. If no set of 4+ integers are detected, it will return the
#     # original string and
#
#     # Working to make obsolete 11/2/2017
#
#     i = 0
#     consecutive_ints = 0
#     while i < len(string):
#
#         if string[i] in integer_list:
#             consecutive_ints += 1
#         else:
#             consecutive_ints = 0
#         if consecutive_ints >= 4:
#             return_slice = string[0:i-3]
#             while string[i] in integer_list:
#                 i += 1
#             remainder_string = string[i:]
#             return return_slice, remainder_string
#         i += 1
#     return string, False
#
# def extract_course_and_outcomes(tag_text):
#
# # takes in one of the beautiful soup4 tagResultSet cast to a string. This is fed into detect_consecutive_integers to
# # return the string slice preceeding the integer set and the slice after. This occurs until there are no more integer
# # sets to remove. A list of the returned string slices is then returned
# # Working to make obsolete. Will be template for newline version 11/2/2017
# #
#     entry_list = []
#     string_tuple = detect_consecutive_integers(tag_text)
#     entry_list.append(string_tuple[0].strip())
#
#     while string_tuple[1]:
#         string_tuple = detect_consecutive_integers(string_tuple[1])
#         entry_list.append(string_tuple[0].strip())
#     return entry_list

def detect_newlines(string):

    # Takes in string. Begins first slice after last consecutive newline from beginning and ends first slice before next newline.
    # Returns the remainder of the string at the most recently detected newline.  Returns False if the initial string
    # is entirely newlines

    i = 0
    k = 1
    slice_start = 0
    flag = True
    while i < len(string) and flag:
        if string[i] == '\n': # Begins walking out from first detected newline
            if i+k < len(string):
                if string[i+k] =='\n':  # Checking if next character is a newline
                    k += 1
                else:     # Character is not a newline, so mark beginning of slice and set flag to break loop
                    slice_start = i + k
                    i = i + k
                    flag = False
            else:
                return string, False # If the string is comprised entirely of newlines, will return original string and False
        else:   #string does not begin with a newline
            slice_start = i
            flag = False
    while string[i] != '\n':
        i += 1

    return string[slice_start:i], string[i:]


def remove_newlines(tag_text):

    # Calls the detect_newlines function and appends each returned slice into entry_list. This continues until False
    # is returned, which indicates a newline-only string and thus the end of the initial string. The list of string
    # slices is returned

    entry_list = []
    string_tuple = detect_newlines(tag_text)
    entry_list.append(string_tuple[0].strip())

    while string_tuple[1]:
        string_tuple = detect_newlines(string_tuple[1])
        entry_list.append(string_tuple[0].strip())
    return entry_list


def filter_entries(entry_list):

    filtered_list = remove_integer_strings(entry_list)
    return filtered_list


def remove_integer_strings(input_list):

# Removes any string in the input_list that is comprised entirely of integers. Returns a list sans these s
# This filters out empty strings as well because they are len 0, the default for int count.
    filtered_list = []
    for strings in input_list:
        int_count = 0
        for chars in strings:
            if chars in integer_list:
                int_count += 1
        if int_count != len(strings):
            filtered_list.append(strings)
    return filtered_list

def get_BS4_resultset(url):
    #Feed in local path to saved HTML page. Only works for one page at a time - not interactive with JS
    req = urllib.request.Request(url)
    page = urllib.request.urlopen(req)
    page_soup = BeautifulSoup(page, 'lxml') #Creates BS object from page
    tag = page_soup.find_all('tbody')   #creates ResultSet object featuring all 'tbody' hits. iterable. use .get_text()
    return tag




if __name__ == "__main__":


    #print(page_soup)
    # Below stores resultset in tag and is iterable. objects held in tag can be cast to string. Need to extract info.
    ################################
    tag = get_BS4_resultset("file:///C:/Users/rpaulos/Desktop/Outcomes%20Assessment%20Toolbox_files/medical%20information.html")

    z = 0


    while z < len(tag):
        # How is the below line removing integer strings AND empty strings/?!
       # print(remove_integer_strings(remove_newlines(tag[z].get_text())))
        print(filter_entries(remove_newlines(tag[z].get_text())))
        z+=1










