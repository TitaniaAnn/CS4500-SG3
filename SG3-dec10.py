#!/usr/bin/env python3

'''
Created using Thonny and Visual Studio Code

SG3
'''

from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import messagebox
from tkinter import ttk
from os import path
from collections import defaultdict
from pathlib import Path
import string
import sys
import re

# SG2 Methods
#constant
file_ext = ".txt" 
#Prompt User what this program does, return nothing.
# def promptUser(): 
#    print("This app reads up to 10 text files, stores each file into a wordlist, displays a summary table, shows how many times a specific word appears, and builds a concordance listing each word’s locations across all files.") 
#    return 0 
 
#Prompt user to enter filename, takes in x as parameter, and returns nothing when succesful
""" Take in filename, check if it has .txt on end and if it exists in filepath and then return boolean. 
"""
def getFile(temp):
    filename = ""
    while True:
        filename = input("Please Enter a filename, you can enter up to 10 a filenames(All must be within the same folder as the app):").strip() # Added strip to eliminate any spaces before and after the filename
       
        # Check if filename ends with .txt (case-insensitive)
        if filename.lower().endswith(file_ext):
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
#def getContinuancy(z):
#    #con = continue variable
#    con = input("Would you like to continue entering Files? Please enter Yes or No:").strip().lower()
#    if con == "yes" or con == "y":
#        z = True
#    elif con == "no" or con == "n":
#        z = False
#    else:
#        print("That answer is not valid, please try again")
#        #Recursively call the definition again and return its value
#        return getContinuancy(z)
#    return z
    
# 1. Clean text
def remove_punctuation(text):
    # Finds and removes all punctuation from the string
    # pattern = r'[^\w\s-]|(?<!\w)-(?!\w)|(?<!\w)-(?!\r)|(?<!\w)-(?!\n)'
    pattern = r'[^\w\s-]|(?<!\w)-(?!\w)'
    return re.sub(pattern, '', text).replace('\r', '').replace('\n', '')

# 1. Get Content from file and make into wordlist
# Modified for SG3
def getContent(entry): 
    wordlist = []
    filename = entry.get()
    try:
        if filename in all_wordlists:
            messagebox.showerror('Error', f"Error: file '{filename}' has already been added!")
            return
        with open(filename, 'r', encoding="utf-8") as f: 
            content = f.read()
            content = remove_punctuation(content).lower()
            wordlist = content.split()
        if len(wordlist) > 0:
            all_wordlists[filename] = wordlist
            print(all_wordlists) # FLAG: Delete
            ToggleButtonsOn()
            messagebox.showinfo('Success', "File added successfully!")
            entry.delete(0, END).delete(0, END)
    except FileNotFoundError:
        messagebox.showerror('Error', f"Error: file '{filename}' not found.")


# 2. Validate entry
def getSearchWord(entry):
    LegalChars = r"^[a-zA-Z-]+$"
    searchWord = entry.get()

    # Check length of word and that it is valid
    if len(searchWord) > 0 and re.match(LegalChars, searchWord):
        return searchWord.lower()
    else:
        # if entry is invalid show error box and return to entry window
        messagebox.showerror('Error', "Word is invalid. \nWord must contain only letters and hyphen. \nPlease enter a word to search")
        return
    

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

# GUI version of Build Concordance functionality
def BuildConcordance_Window():
    if not all_wordlists:
        messagebox.showerror('Error', "No files loaded to process.")
        return

    # Optional: include ignore/highlight lists if you use them
    ignore_Words, highlight_Words = read_Extra_Lists()

    messagebox.showinfo('Working', "Building concordance... please wait.")
    concordance = build_Concordance(all_wordlists, ignore_Words)
    create_Concordance(concordance, highlight_Words)

    # Automatically build ExtraLists after concordance
    build_ExtraLists(concordance, len(all_wordlists))
    messagebox.showinfo('Success', "Concordance and ExtraLists successfully generated!")

                  
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
hist_word = {}
hist_count = []
all_wordlists = {} #This List stores all File lists.

# Main Window Creation
mainWindow = Tk()
mainWindow.title("SG3")
mainWindow.geometry("250x300")


# 0. Info Window: Opens with Main Menu
# User can NOT use Main Menu until "Ok" is clicked on Info Window
def Info_Window():
    startText = "This app reads text files, stores each file into a wordlist, displays a summary table, shows how many times a specific, searched word appears, and builds a concordance listing each word’s locations across all files."
    
    infoWin = Toplevel(mainWindow)
    infoWin.title("SG3: Info")
    Label(infoWin, text=startText, wraplength=500).pack(padx = 20, pady = 20)
    init_button = Button(infoWin, text = "Ok", command = infoWin.destroy, height = 1, width = 10)
    init_button.pack(pady = 10)
    infoWin.bind('<Return>', lambda event: init_button.invoke())
    infoWin.transient(mainWindow)
    infoWin.grab_set()
    mainWindow.wait_window(infoWin)
    

# 1. Opens a new window to open a file
def OpenFile_Window():
    fileName = StringVar()
    #fileName.trace("w", validate_filename) # Call validate_filename when the variable is written to

    openWin = Toplevel(mainWindow)
    openWin.geometry("250x125")
    openWin.title("Open A File")
    openWin.attributes('-topmost', True)
    Label(openWin, text = "Enter file name, including .txt: ").pack(padx = 5, pady = 5)

    entry = Entry(openWin, width = 30, textvariable = fileName) #, validate="focusout", validatecommand=(vcmd, '%P'))
    entry.pack(pady = 5)
    submit_button = Button(openWin, text = "Submit", command = lambda:FileName_Validation(entry), height = 1, width = 10)
    submit_button.pack(pady = 10)
    openWin.bind('<Return>', lambda event: submit_button.invoke())
    openWin.mainloop()

# 1. Validate Filename
def FileName_Validation(entry):
    filename = entry.get()
    if filename.strip().lower().endswith(".txt"):
        getContent(entry)
    else:
        messagebox.showerror("Invalid Input", "File name must end with '.txt'.")
        # Prevent further submission actions by simply returning
        return
    
# 1. Toggles buttons 2, 3, and 4 on the main menu window
# Use in OpenFile_Window with OpenFile
def ToggleButtonsOn():
    b2.config(state=NORMAL)
    b3.config(state=NORMAL)
    b4.config(state=NORMAL)


# Function to display a message to a user
# Used in OpenFile_Window
def MessageUser(message):
    showinfo("Message", message)

# 2. Opens a new window to search for words
def SearchWords_Window():
    wordText = StringVar()

    wordWin = Toplevel(mainWindow)
    wordWin.geometry("540x210")
    wordWin.title("Search For Words")


    frame1 = Frame(wordWin, width=150)
    frame1.pack(padx=10, pady=10,side=LEFT, fill=BOTH, expand=False)



    Label(frame1, text = "Enter a word:").pack(padx = 5, pady = 5)
    entry = Entry(frame1, width = 30, textvariable = wordText)
    entry.pack(pady = 5)

    submit_btn = Button(frame1, text = "Submit", command = lambda:wordInfo(getSearchWord(entry), tree), height = 1, width = 10)
    submit_btn.pack(pady = 10)
    cancel_btn = Button(frame1, text="Cancel", command=wordWin.destroy, height=1, width=10)
    cancel_btn.pack(pady=10)

    wordWin.bind('<Return>', lambda event: submit_btn.invoke())

    nested_frame2 = Frame(wordWin, width=350)
    nested_frame2.pack(padx=10, pady=10, side=TOP, fill=BOTH, expand=True)

    columns = ('word', 'file', 'number')
    tree = ttk.Treeview(nested_frame2, columns=columns, show='headings')
    tree.heading('word', text='Word')
    tree.heading('file', text='FileName')
    tree.heading('number', text='Count')

    for ws in hist_word:
        tree.insert('', 'end', values=(ws.key(),"",""))
        for wi in ws.items:
            tree.insert('','end',values=("",wi[0], wi[1]))
    
    tree.pack(pady=10, padx=10)
    wordWin.mainloop()

# 2. Get Info on search word
def wordInfo(word, tree):
    # Check if any files are open
    if not all_wordlists:
        messagebox.showerror('Error', "No files to search.")
        return
    
    if word in hist_word:
        messagebox.showerror('Error', "Word already searched.")
        return
    else:
        hist_word[word] = {}
        wordPrint = ""
        tree.insert('', 'end', values=(word,"",""))
        for key, value in all_wordlists.items():
            count = sum(v == word for v in value)
            hist_word[word] = {key, count}
            wordPrint += f"{key}: {count}\n"
            tree.insert('','end',values=("",key, count))

        if wordPrint:
            # messagebox.showinfo('Word Info', wordPrint)
            return
        else:
            messagebox.showinfo('Not Found', f"{word} is not found")
            return

# The close window part was annoying.
# 4. This would opens a dialog listing all currently loaded files and lets the user close one.
def CloseFile_Window():
    # Check if any files are open
    if not all_wordlists:
        messagebox.showerror('Error', "No files to close.")
        return

    # Build display window
    closeWin = Toplevel(mainWindow)
    closeWin.title("Close a File")
    closeWin.geometry("275x175")

    # Window content
    Label(closeWin, text="Select a file to close:").pack(pady=5)
    file_list = Listbox(closeWin, width=35, height=6, selectmode=SINGLE)
    for f in all_wordlists.keys():
        file_list.insert(END, f)
    file_list.pack(pady=5)

    # Remove file function
    def remove_selected():
        selection = file_list.curselection()
        if not selection:
            messagebox.showinfo('', "Please select a file to close.")
            return
        filename = file_list.get(selection[0])
        del all_wordlists[filename]
        messagebox.showinfo('Success', f"File '{filename}' has been closed.")
        if not all_wordlists:
            ToggleButtonsOff()
        closeWin.destroy()

    # When the last file is closed, it disables buttons 2,3 and 4
    Button(closeWin, text="Close File", command=remove_selected).pack(pady=10)


# 4. Toggles buttons 2, 3, and 4 off on the main menu window
# Use when last file has been closed
def ToggleButtonsOff():
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)
    b4.config(state=DISABLED)


# 5. A function to exit to end the main loop
def ExitProgram():
    messagebox.showinfo('Info', "Exiting program.")
    mainWindow.destroy()


## Main Menu
'''
Buttons 2, 3, and 4 are set to DISABLED until a file is opened
Pack displays the buttons
Added key bindings to 1-5
'''
# Open File Button
b1 = Button(mainWindow, text = "1. Open A File", command = OpenFile_Window, height = 2, width = 25)
b1.pack(pady = 5)
mainWindow.bind("1", lambda event: b1.invoke())

# Word Search Button
b2 = Button(mainWindow, text = "2. Search For Words", command=SearchWords_Window, height = 2, width = 25, state = DISABLED)
b2.pack(pady = 5)
mainWindow.bind("2", lambda event: b2.invoke())

# Build Concordence Button
b3 = Button(mainWindow, text = "3. Build Concordance", command=BuildConcordance_Window, height = 2, width = 25, state = DISABLED)
b3.pack(pady = 5)
mainWindow.bind("3", lambda event: b3.invoke())

# Close File Button
b4 = Button(mainWindow, text = "4. Close File", command=CloseFile_Window, height = 2, width = 25, state = DISABLED)
b4.pack(pady = 5)
mainWindow.bind("4", lambda event: b4.invoke())

# Exit Button
b5 = Button(mainWindow, text = "5. Exit", command=ExitProgram, height = 2, width = 25)
b5.pack(pady = 5)
mainWindow.bind("5", lambda event: b5.invoke())


# Display Info Window on Start of Program
Info_Window()
mainWindow.deiconify()
mainWindow.mainloop()