#!/usr/bin/env python2.7

"""
Author: Luke Spinardi
Summary: Module that combines a tkinter GUI with the followScripts formula"""

from Timer import FollowTimer
import time
import ttk
from collections import deque
from Tkinter import *
import tkMessageBox
import followScripts


def changeRemaining(amount):
    """
    A method that changes the totalRemaining StrVariable
    :param amount: int value to decrese the StrVariable
    :return: """

    global totalRemaining
    totalRemaining.set(totalRemaining.get() - amount)


def writeToLog(msg):
    """
    # Code to write to log window.
    :param msg: str value that is written to the output window
    :return: """

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
    """
    Exports the current StrVaraible values that are necessary to running
    Chug-a-Lug to an external file
    :return: """

    remaining = totalRemaining.get()
    user = username.get()
    passw = password.get()
    strat = strategy.get()
    search = searchTerm.get()
    time = timer.get_time()
    with open('config.txt', 'w') as file:
        file.write(str(remaining) + "\n")
        file.write(user + "\n")
        file.write(passw + "\n")
        file.write(strat + "\n")
        file.write(search + "\n")
        file.write(str(time))


def time_remaining(time):
    """
    Converts the time remaining into a return string.
    :param time: a value in seconds that is the time remaining
    :return: string value communicating how much time is left or a message"""

    if time < 0:
        return "You are now able to follow more accounts"
    seconds = int(time % 60)
    minutes = int((time / 60) % 60)
    hours = int(time / 60 / 60)
    output = str(hours) \
             + " hours, " + str(minutes) + " minutes, and " \
             + str(seconds) + " seconds left until you " \
                              "are able to follow more accounts."
    return output


def main():
    """
    Main Script the body of Chug-a-Lug
    :return: Tk object named window """

    def followFormula(option):
        """
        The formula and its variations that are used to complete the actions
        :param option: int value from 1 to 5 dictating which mode to use
        :return: null """

        try:
            writeToLog("Beginning Follow-Back Formula...")
            if time.strftime('%a') == 'Mon' or time.strftime('%a') == 'Wed' or time.strftime('%a') == 'Fri':
                writeToLog("Executing Phase 0: Purge")
                followScripts.UnfollowUnfollowers(username, password)
            writeToLog("Executing Phase 1: Fortify")
            followScripts.FollowFollowers(output, username, password, totalRemaining.get())
            if option == 'Breadth Mode':
                writeToLog("Executing Phase 2: Increase (Breadth Mode)")
                followScripts.searchFollow(username, password, totalRemaining.get(), searchTerm.get())
                writeToLog("Executing Phase 3: Fill")
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            elif option == 'Bulk Mode':
                writeToLog("Executing Phase 2: Increase (Bulk Mode)")
                followScripts.searchFollow(username, password, totalRemaining.get(), "TeamFollowBack")
                writeToLog("Executing Phase 3: Fill")
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            else:
                writeToLog("Executing Phase 2: Increase (Depth Mode)")
                followScripts.followFollowersFollowers(username, password, totalRemaining.get())
            timer.start_time()
            writeToLog("Formula is complete. Running again in 24 hours")
            saveInput()
        except UserWarning as error:
            writeToLog(error)
            tkMessageBox.showerror("Error", "Username or Password incorrect")
        except Exception as error:
            saveInput()
            writeToLog("ProgrammingError: " + str(error))
            raise

    def loadInput():
        """
        Grabs the values from a file and imports them to the GUI
        :return:"""

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
            timer.set_time(float(x.popleft()))
            writeToLog(time_remaining(timer.time_left_until_24hours()))
        except ValueError:
            writeToLog("Click 'Run' to Begin")
            pass

    def checkTime():
        """
        Recursive method that runs every second to see if the time in
        seconds is equal to the amount of seconds in 24 hours
        :return:"""

        if (timer.get_elapsed() > 86401):
            totalRemaining = 1000
            followFormula(strategy.get())
            print (timer.get_elapsed())
        window.after(1000, checkTime)

    def on_closing():
        """
        It confirms the quit then closes the Tk window properly
        :return:"""

        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()

    global timer
    timer = FollowTimer()
    global startDate

    # Main window
    global window
    window = Tk()
    window.title("Chug-a-lug")  # window Title
    window.resizable(width=False, height=False)  # Lock aspect ratio

    # Frame inside window
    global top
    top = Frame(window)  # Column of Fields
    top.grid(column=0, row=0, sticky=(N, W, E, S))
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)

    # GUI section title
    Label(top, text="Twitter Login:").grid(column=1, row=1, sticky=W)

    # Username field
    global username
    username = StringVar()  # Username field
    Label(top, text="Username:").grid(column=1, row=2, sticky=W)
    username_entry = Entry(top, width=15, textvariable=username)
    username_entry.grid(column=2, row=2, sticky=W)
    username_entry.focus()

    # Password field
    global password
    password = StringVar()  # Password field
    Label(top, text="Password:").grid(column=1, row=3, sticky=W)
    password_entry = Entry(top, width=15, show="*", textvariable=password)
    password_entry.grid(column=2, row=3, sticky=(W, E))

    # Total Remaining variable display
    global totalRemaining
    totalRemaining = IntVar()
    totalRemaining.set('1000')
    Label(top, text="# of Follows\nRemaining:").grid(column=1, row=4, sticky=W)
    remaining = Label(top, textvariable=totalRemaining).grid(column=2, row=4, sticky=(W))

    global strategy
    strategy = StringVar()  # Strategy combobox
    Label(top, text="Follow Formula Mode:").grid(column=1, row=6, sticky=W)
    combobox = ttk.Combobox(top, textvariable=strategy)

    combobox['values'] = ('Depth Mode', 'Breadth Mode', 'Bulk Mode')
    combobox.current(0)
    combobox.grid(column=2, row=6, sticky=W)

    #
    global searchTerm
    searchTerm = StringVar()  # Username field
    Label(top, text="Target Market: ").grid(column=1, row=7, sticky=W)
    searchterm_entry = Entry(top, width=15, textvariable=searchTerm)
    searchterm_entry.grid(column=2, row=7, sticky=W)

    # Row of Buttons
    # Need to update start and pause Values
    run = Button(top, text="Run",
                 command=lambda: followFormula(strategy.get())).grid(column=2, row=8, sticky=W)
    unfollow = Button(top, text="Unfollow",
                      command=lambda: followScripts.UnfollowUnfollowers(username, password)).grid(column=2, row=8,
                                                                                                  sticky=E,
                                                                                                  padx=(0, 10))
    save = Button(top, text="Save Login",
                  command=lambda: saveInput()).grid(column=2, row=9, sticky=E, padx=(0, 10))

    # Output Text Box
    Label(top, text="Output").grid(column=1, row=10, sticky=W)
    global output
    output = Text(top, wrap=WORD, width=40, state='disabled')
    output.grid(column=1, row=11, columnspan=2, padx=(10, 10))

    # Tries to load in the values from config.txt. If nothing is there,
    # then its the user's first time, therefore issue the except messages.
    try:
        loadInput()
    except IOError as error:
        writeToLog("Welcome to Chug-a-Lug.")
        writeToLog("Click 'Run' to gain users.")
        writeToLog("Click 'Unfollow' to unfollow users that aren't following you back.")
        writeToLog("Click 'Save' to save your Twitter login information.")
        writeToLog("Enter your Twitter Login, choose a strategy, save your credentials, then click 'Run' to begin.")
    window.after(1000, checkTime)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    return window


if __name__ == "__main__":
    window = main()
    window.mainloop()


def run():
    """
    Creates the GUI when Chug-a-Lug is called from an executable directory
    :return: null"""

    window = main()
    window.mainloop()
