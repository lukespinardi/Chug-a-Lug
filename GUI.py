# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:11:01 2017

@author: ltspinardi
"""
from Timer import FollowTimer
import time
import ttk
from collections import deque
#from Tkinter import Tk, Frame, Label, Button, Text
from Tkinter import *
import tkMessageBox

import followScripts

def changeRemaining(amount):
    global totalRemaining
    totalRemaining.set(totalRemaining.get() - amount)

# Code to write to log window. May need to edit to make output an imported var
def writeToLog(msg):
    numlines = output.index('end - 1 line').split('.')[0]
    output['state'] = 'normal'
    if numlines == 24:
        output.delete(1.0, 2.0)
    if output.index('end-1c') != '1.0':
        output.insert('end', '\n')
    output.insert('end', msg)
    output['state'] = 'disabled'
    window.update()

def saveInput():
    remaining = totalRemaining.get()
    user = username.get()
    passw = password.get()
    strat = strategy.get()
    search = searchTerm.get()
    time = timer.getTime()
    with open('config.txt', 'w') as file:
        file.write(str(remaining)+"\n")
        file.write(user+"\n")
        file.write(passw+"\n")
        file.write(strat+"\n")
        file.write(search+"\n")
        file.write(str(time))

def time_remaining(time):
    if time < 0:
        return "You are now able to follow more accounts"
    seconds = int(time % 60)
    minutes = int((time / 60) % 60)
    hours = int(time / 60 / 60)
    output = str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds left until you " \
                                                                                        "are able to follow more accounts."
    return output

def makeWindow():
    # Create the window using Tkinter
    global window
    window = Tk()
    window.title("Chug-a-lug")  # window Title
    window.resizable(width=False, height=False)  # Lock aspect ratio

    global top
    top = Frame(window)  # Column of Fields
    top.grid(column=0, row=0, sticky=(N, W, E, S))
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)

    currentState = StringVar()  # Current State field
    Label(top, text="Current State:").grid(column=1, row=1, sticky=W)
    Label(top, textvariable=currentState).grid(column=2, row=1, sticky=(W, E))
    """
    Code to change label ON / OFF
    """
    global username
    username = StringVar()  # Username field
    Label(top, text="Username:").grid(column=1, row=2, sticky=W)
    username_entry = Entry(top, width=15, textvariable=username)
    username_entry.grid(column=2, row=2, sticky=W)
    username_entry.focus()

    global password
    password = StringVar()  # Password field
    Label(top, text="Password:").grid(column=1, row=3, sticky=W)
    password_entry = Entry(top, width=15, show="*", textvariable=password)
    password_entry.grid(column=2, row=3, sticky=(W, E))

    global totalRemaining
    totalRemaining = IntVar()
    totalRemaining.set('1000')
    Label(top, text="# of Follows\nRemaining:").grid(column=1, row=4, sticky=W)
    remaining = Label(top, textvariable=totalRemaining).grid(column=2, row=4, sticky=(W))

    global strategy
    strategy = StringVar()  # Strategy combobox
    Label(top, text="Follower Strategy:").grid(column=1, row=6, sticky=W)
    combobox = ttk.Combobox(top, textvariable=strategy)

    combobox['values'] = ('Follower\'s followers', 'Follow via Search Term', 'Follow Back Accounts')
    combobox.current(0)
    combobox.grid(column=2, row=6, sticky=W)

    global searchTerm
    searchTerm = StringVar()  # Username field
    Label(top, text="Search Term: ").grid(column=1, row=7, sticky=W)
    searchterm_entry = Entry(top, width=15, textvariable=searchTerm)
    searchterm_entry.grid(column=2, row=7, sticky=W)

    global timer
    timer = FollowTimer()
    global startDate

    # Formula Design methods
    def followFormula(option):
        try:
            writeToLog("Beginning Follow-Back Formula...")
            if time.strftime('%a') == 'Mon' or time.strftime('%a') == 'Wed' or time.strftime('%a') == 'Fri':
                writeToLog("Executing Phase 0: Purge")
                #followScripts.UnfollowUnfollowers(username, password)
            writeToLog("Executing Phase 1: Fortify")
            #followScripts.FollowFollowers(output, username, password, totalRemaining.get())
            if option == 'Follow via Search Term':
                writeToLog("Executing Phase 2: Increase (Breadth Mode)")
                followScripts.searchFollow(username, password, totalRemaining.get(), searchTerm.get())
                writeToLog("Executing Phase 3: Fill")
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            elif option == 'Follow Back Accounts':
                writeToLog("Executing Phase 2: Increase (Bulk Mode)")
                followScripts.searchFollow(username, password, totalRemaining.get(), "TeamFollowBack")
                writeToLog("Executing Phase 3: Fill")
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            else:
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            timer.startTime()
            saveInput()
        except UserWarning as error:
            writeToLog(error)
            tkMessageBox.showerror("Error","Username or Password incorrect")
        except Exception as error:
            saveInput()
            writeToLog("ProgrammingError: " + str(error))
            raise

    def loadInput():
        x = deque([])  # Deque is more efficient for front end access
        with open("config.txt") as file:
            for l in file:
                x.append(l.rstrip())
        totalRemaining.set(int(x.popleft()))
        username.set(x.popleft())
        password.set(x.popleft())
        strategy.set(x.popleft())
        searchTerm.set(x.popleft())
        writeToLog("Welcome Back to Chug-a-Lug.")
        try:
            timer.setTime(float(x.popleft()))
            writeToLog(time_remaining(timer.getRemaining()))
        except ValueError:
            writeToLog("Click 'Run' to Begin")
            pass

    # Row of Buttons
    # Need to update start and pause Values
    start = Button(top, text="Run",
                   command=lambda: followFormula(strategy.get())).grid(column=2,row=8,sticky=W)
    pause = Button(top, text="Unfollow",
                   command=lambda: followScripts.UnfollowUnfollowers(username, password)).grid(column=2, row=8,sticky=E, padx=(0, 10))
    save = Button(top, text="Save Login",
                   command=lambda:saveInput()).grid(column=2, row=9,sticky=E,padx=(0, 10))

    # Output Text Box
    Label(top, text="Output").grid(column=1, row=10, sticky=W)
    global output
    output = Text(top, wrap=WORD, width=40, state='disabled')
    output.grid(column=1, row=11, columnspan=2, padx=(10, 10))

    def checkTime():
        if (timer.getElapsed() > 86401):
            totalRemaining = 1000
            followFormula(strategy.get())
            print (timer.getElapsed())
        window.after(1000, checkTime)

    def on_closing():
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()

    try:
        loadInput()
    except IOError as error:
        writeToLog("Welcome to Chug-a-Lug.")
        writeToLog("Click 'Run' to gain users.")
        writeToLog("Click 'Unfollow' to unfollow users that aren't following you back.")
        writeToLog("Click 'Save' to save your Twitter login information.")
        writeToLog("Enter your Twitter Login, choose a strategy, save your credentials, then click 'Run' to begin.")
    window.after(1000,checkTime)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    return window

if __name__ == "__main__":
    window = makeWindow()
    window.mainloop()


# ESTABLISH PHASE
# [[[DONE]]]Make Unfollow Script on button press
# [DONE]Make Search follow script. Go to general sear. Search terms. Go to profiles. Follow profiles
# [DONE]Make Follow Followers script. Select First follower. Go to their followers page (userVar"/followers"). Run follow script.
# [DONE]Make it into growth fromula. Follow Followers. Follow Followers Followers.
# [DONE]While amount of follows is not enough, keep on scrolling
# Convert to phantomJS (aka invisibrowser) https://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver

# SAVE PHASE
# [DONE]Save Variables to file
# [DONE]Save file on button click
# [DONE]Load file on startup,

# ENCRYPT PHASE
# Ask user for password at save
# Save file found. Please input password.
# Save a different save file for each profile.
# Prevent from overwriting without password

# CLEANUP
# Output wont update while in a def loop
# Upon open, print time left til next run OR Welcome, enter your twitter login
# [Done]Make stopwatch class. Make object.
# Make Tkinter a class, not a method

# AUTOMATIC PHASE
# [Done]Figure out if you can catch errors.
# Make it so that unfollow unfollowers if error caught. Then reset timer.
# [DONE]Figure out database concept. Keep username, password (encrypted), time, date, last ran
# Figure out how to run process in background. http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

# CHECK STATS
# Tells the user upon start whether or not they gained followers.
# Checks to see how many of them are organic vs follow backs (via Labels)

# ADVANCED PHASE
# Record everyprofile followd using element.text in database
# Make sure you don't refollow account that has already been followed
