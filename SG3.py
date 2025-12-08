#!/usr/bin/env python3

'''
Created using Thonny and Visual Studio Code

SG3
'''

from tkinter import *
from tkinter.messagebox import showinfo
from os import path
from collections import defaultdict
from pathlib import Path
import string
import sys
import re

# SG2 Methods
#constant
file_extension = "txt" 
#Prompt User what this program does, return nothing.
def promptUser(): 
    print("This app reads up to 10 text files, stores each file into a wordlist, displays a summary table, shows how many times a specific word appears, and builds a concordance listing each word’s locations across all files.") 
    return 0 
 
#Prompt user to enter filename, takes in x as parameter, and returns nothing when succesful
""" Take in filename, check if it has .txt on end and if it exists in filepath and then return boolean. 
"""
def getFile(temp):
    filename = ""
    while True:
        filename = input("Please Enter a filename, you can enter up to 10 a filenames(All must be within the same folder as the app):").strip() # Added strip to eliminate any spaces before and after the filename
       
        # Check if filename ends with .txt (case-insensitive)
        if filename.lower().endswith(".txt"):
            file = Path(filename).resolve()
            if not file.exists():
                print("File does not exist. Please try again.")
            else:
                # Added check for duplicate filenames
                if str(filename) in temp:
                    print("ERROR: You have already entered that filename")
                else:
                    return str(filename)
        else:
            if len(filename) == 0:
                print("Input is empty, please try again.")
            else:
                print("Invalid file type. Must be a text (*.txt) file.")

#Get continuancy boolean value from if user wants to continue entering files.
def getContinuancy(z):
    #con = continue variable
    con = input("Would you like to continue entering Files? Please enter Yes or No:").strip().lower()
    if con == "yes" or con == "y":
        z = True
    elif con == "no" or con == "n":
        z = False
    else:
        print("That answer is not valid, please try again")
        #Recursively call the definition again and return its value
        return getContinuancy(z)
    return z
    
#Clean text
def remove_punctuation(text):
    # Finds and removes all punctuation from the string
    # pattern = r'[^\w\s-]|(?<!\w)-(?!\w)|(?<!\w)-(?!\r)|(?<!\w)-(?!\n)'
    pattern = r'[^\w\s-]|(?<!\w)-(?!\w)'
    return re.sub(pattern, '', text).replace('\r', '').replace('\n', '')

#Get Content from file and make into wordlist
# Modified for SG3
def getContent(filename): 
    wordlist = []
    try:
        if filename in all_wordlists:
            MessageUser(f"Error: file '{filename}' has already been added!")
            return
        with open(filename, 'r', encoding="utf-8") as f: 
            content = f.read()
            content = remove_punctuation(content).lower()
            wordlist = content.split()
        if len(wordlist) > 0:
            all_wordlists[filename] = wordlist
            print(all_wordlists) # FLAG: Delete
            ToggleButtonsOn()
            MessageUser("File added successfully!")
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        MessageUser(f"Error: file '{filename}' not found.")

def getSearchWord():
    endFunction = False # if true the function ends
    LegalCharacters = 'abcdefghijklmnopqrstuvwxyz-'
    searchWord = ""
    while endFunction == False:
        answer = input("Enter a Word to search for \n(must be all alphabet or a - with no space in between 2 words): ")
        if len(answer) > 0:
            # Check Word
            valid = True
            for char in answer: # check each character
                if LegalCharacters.find(char.lower()) > -1:
                    if char == "-":
                        cindex = answer.find("-")
                        if (cindex > 0 and cindex < (len(answer)-1)):
                            continue
                        else:
                            endFunction = False
                            break
                    else:
                        valid = True
                        
                if valid == True:
                    searchWord = answer
                    endFunction = True
                else:
                    print("Word is invalid")
                    print("word must only contain letters \n(or a hyphen in between the words with no space)")
                    endFunction = False
        else:
            print("Please enter a word to search")
            endFunction = False
    return searchWord

def countOccurrences(wordList, searchWord):
    count = 0     
    for word in wordList:
        low = word.casefold()
        if low.find(searchWord.casefold()) > -1:
            count = count + 1
    return count

def continueSearch():
    yes =  ["yes", "y"]
    no = ["no", "n"]
    valid = False
    while not valid:
        answer = input("Do you want to search for another word? Please answer with Yes or No: ").strip().lower()
        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            print("Invalid answer: must be yes or no.")

def print_file_summary(all_wordlists):
    """
    This Definition will print a well-formatted table that includes:
    - 3 columns, that show filename, total number of words in file,
    and total number of distinct words in file.
    """
    if not all_wordlists:
        print("There are no files to display")
        return
        
    #Prepare data in specific format.
    rows = []
    #Append Filename, total words, and distinct words in first row. 
    for fullpath, words in all_wordlists.items():
        FileName = Path(fullpath).name
        #t_words = total   d_words = distinct
        t_words = len(words)
        d_words = len(set(w.casefold() for w in words if len(w) > 0))
        rows.append((FileName, t_words, d_words))
    
    #Create column width
    #fn_width = filename, t_width = total, d_width = distinct_width
    fn_width = max(len(r[0]) for r in rows)
    t_width = max(len(str(r[1])) for r in rows)
    d_width = max(len(str(r[2])) for r in rows)
    
    #Create Header
    header_fn = "Filename"
    header_distinct = "Distinct"
    header_total = "TotalWords"
    fn_width = max(fn_width, len(header_fn))
    t_width = max(t_width, len(header_total))
    d_width = max(d_width, len(header_distinct))
    
    
    #Print Header
    print() #Blank Line before 
    print(f'{header_fn:>{fn_width}}  {header_total:>{t_width}}  {header_distinct:>{d_width}}')
    print('-' * (fn_width + 2 + t_width + 2 + d_width))

    #Print each row now
    for name, total_words, distinct_words in rows:
        print(f'{name:>{fn_width}}  {total_words:>{t_width}}  {distinct_words:>{d_width}}')

    print()  # blank line after table


#Builds the Concordance.
def build_Concordance(all_wordlists, ignore_Words):
    print("Building Concordance")
    
    concordance = defaultdict(list)
    file_Number = 1

    for filename in all_wordlists.keys():
        with open(filename, "r", encoding="utf-8") as f:
            line_Number = 0
            hyphen = []
            for line in f:
                line_Number += 1
                line_words = remove_punctuation(line).lower().split()
                word_Number = 0
                
                for word in line_words:
                    word_Number += 1
                    clean = word
                    if clean.endswith('-'):
                        hyphen = [clean,file_Number,line_Number,word_Number]
                    elif hyphen:
                       #  print(hyphen)
                        clean = f"{hyphen[0]}{clean}" 
                        if not clean or clean in ignore_Words:
                            hyphen = []
                            continue
                        concordance[clean].append((hyphen[1], hyphen[2], hyphen[3]))
                        concordance[clean].append((file_Number, line_Number, word_Number))
                        hyphen = []
                    else:
                        if not clean or clean in ignore_Words:
                            continue
                        concordance[clean].append((file_Number, line_Number, word_Number))
        file_Number += 1

    # Return concordance
    return concordance
                
def create_Concordance(concordance, highlight_Words):
    
    #Now sort words alphabetically
    sort_Words = sorted(concordance.keys(), key=lambda w: w.replace("-", "\x00")) # \n00 acts as a null character. 
    
    #Open file to write to
    with open("Concordance.txt", "w", encoding="utf-8") as f:
        #Loop through every word.
        for word in sort_Words:
            if word in highlight_Words:
                display_word = word.upper()
            else:
                display_word = word
            #Get Location
            location = concordance[word]
            #Format location
            format_Location = [f"{file}.{line}.{word_num}" for file, line, word_num in location]
            #Format by adding ; and end with .
            output = f"{display_word} " + "; ".join(format_Location) + "."
            #Write to file
            f.write(output + "\n")
            #Write output
            print(output)
            
    #Finally print output that its done.
    print("Concordance.txt was created and written to.")

def read_Extra_Lists(filename="ExtraLists.txt"):
    ignore_Words = []
    highlight_Words = []
    section = None
    
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.upper() == "IGNORE:":
                    section = "ignore"
                elif line.upper() == "HIGHLIGHT:":
                    section = "highlight"
                elif section == "ignore":
                    ignore_Words.append(line.lower())
                elif section == "highlight":
                    highlight_Words.append(line.lower())
    except FileNotFoundError:
        print(f" {filename} not found. Will Continue. ")
        
    return ignore_Words, highlight_Words
                  
                  
def build_ExtraLists(concordance, total_Files):
    print("\nBuilding Extra Lists.")
    
    #Create Dictionary of word counts
    word_Counts = {}
    #List that Track each words file it is in.
    word_Files = {}
    
    for word, refs in concordance.items():
        word_Counts[word] = len(refs)
        file_nums = {ref[0] for ref in refs}
        word_Files[word] = file_nums
        
    #Sort top 10 frequent
    top_Ten = sorted(word_Counts.items(), key=lambda x: (-x[1], x[0]))[:10]
    
    #Sort words that are in all file.
    all_Files_Words = [w for w, files in word_Files.items() if len(files) == total_Files]

    #Sort words that are only in one file
    one_File_Words = [w for w, files in word_Files.items() if len(files) == 1]
    
    with open("ExtraLists.txt", "w") as out:
        out.write("Top 10 Frequent Words:\n")
        out.write(f"{'Word':>15} {'Count':>10} {'Files':>10}\n")
        out.write("-" * 37 + "\n")
        for word, count in top_Ten:
            num_files = len(word_Files[word])
            out.write(f"{word:>15} {count:>10} {num_files:>10}\n")
        out.write("\nWords that appear in All Files are:\n")
        out.write("-" * 27 + "\n")
        for w in sorted(all_Files_Words):
            out.write(f"{w:>15}\n")
        out.write("\n")
        out.write("Words that appear in only one file are:\n")
        out.write(f"\n{'Word':>15} {'File#':>10}\n")
        out.write("-" * 27 + "\n")
        for w in sorted(one_File_Words):
            file_num = list(word_Files[w])[0]  # only one file
            out.write(f"{w:>15} {file_num:>10}\n")
        
    #Print
    print("Top 10 Frequent Words:\n")
    print(f"{'Word':>15} {'Count':>10} {'Files':>10}")
    print("-" * 37)
    for word, count in top_Ten:
        num_files = len(word_Files[word])
        print(f"{word:>15} {count:>10} {num_files:>10}")

    print("\nWords that appear in All Files:\n")
    for w in sorted(all_Files_Words):
        print(f"{w:>15}")

    print("\nWords that appear in only one file:\n")
    print(f"{'Word':>15} {'File#':>10}")
    print("-" * 27)
    for w in sorted(one_File_Words):
        file_num = list(word_Files[w])[0]  # only one file
        print(f"{w:>15} {file_num:>10}")

    print("\nAll tasks complete. Program will now exit.")


# SG3: GUI
# Variables
hist_word = []
hist_count = []
all_wordlists = {} #This List stores all File lists.

# Main Window Creation
mainWindow = Tk()
mainWindow.title("SG3")
mainWindow.geometry("250x300")


def Info_Window():
    startText = "This app reads text files, stores each file into a wordlist, displays a summary table, shows how many times a specific, searched word appears, and builds a concordance listing each word’s locations across all files."
    
    infoWin = Toplevel(mainWindow)
    infoWin.title("SG3: Info")
    Label(infoWin, text=startText, wraplength=500).pack(padx = 20, pady = 20)
    Button(infoWin, text = "Ok", command = infoWin.destroy, height = 1, width = 10).pack(pady = 10)
    infoWin.transient(mainWindow)
    infoWin.grab_set()
    mainWindow.wait_window(infoWin)

# Opens a new window to open a file
def OpenFile_Window():
    fileName = StringVar()
    
    openWin = Toplevel(mainWindow)
    openWin.geometry("250x125")
    openWin.title("Open A File")
    Label(openWin, text = "Enter file name, including .txt: ").pack(padx = 5, pady = 5)
    Entry(openWin, width = 30, textvariable = fileName).pack(pady = 5)
    Button(openWin, text = "Submit", command = lambda:getContent(fileName.get()), height = 1, width = 10).pack(pady = 10)

# Toggles buttons 2, 3, and 4 on the main menu window
# Use in OpenFile_Window with OpenFile
def ToggleButtonsOn():
    b2.config(state=NORMAL)
    b3.config(state=NORMAL)
    b4.config(state=NORMAL)
    
# Toggles buttons 2, 3, and 4 off on the main menu window
# Use when last file has been closed
def ToggleButtonsOff():
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)
    b4.config(state=DISABLED)
    

# Function to display a message to a user
# Used in OpenFile_Window
def MessageUser(message):
    showinfo("Message", message)


# Opens a new window to search for words
# TODO: 
def SearchWords_Window():
    wordWin = Toplevel(mainWindow)
    wordWin.geometry("250x125")
    wordWin.title("Search For Words")

## Main Menu
'''
Buttons 2, 3, and 4 are set to DISABLED until a file is opened
'''
b1 = Button(mainWindow, text = "1. Open A File", command = OpenFile_Window, height = 2, width = 25)
b2 = Button(mainWindow, text = "2. Search For Words", height = 2, width = 25, state = DISABLED)
b3 = Button(mainWindow, text = "3. Build Concordance", height = 2, width = 25, state = DISABLED)
b4 = Button(mainWindow, text = "4. Close File", height = 2, width = 25, state = DISABLED)
b5 = Button(mainWindow, text = "5. Exit", height = 2, width = 25)

# Pack displays the buttons
b1.pack(pady = 5)
b2.pack(pady = 5)
b3.pack(pady = 5)
b4.pack(pady = 5)
b5.pack(pady = 5)

Info_Window()
mainWindow.deiconify()

mainWindow.mainloop()