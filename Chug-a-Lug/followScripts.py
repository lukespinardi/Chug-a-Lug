#! usr/bin/env python2.7
""""
Author: Luke Spinardi
Summary: A module containig scripts that make automated actions on the
Twitter social media platform
"""

import time
import ChugaLug
import random
from selenium import webdriver


def UnfollowUnfollowers(user, passw):
    """
    Phase 0 Script. Purge = Get rid of extra bulk.
    Summary: Opens the browser, goes to the user's following page, then unfollows the users that arent following
    the user.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI"""

    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/following?lang=en")
    scrollToBottom(browser)
    profiles = browser.find_elements_by_css_selector(".ProfileCard-content ")
    unfollow_if_not_following(profiles)
    browser.close()


def FollowFollowers(user, passw, total):
    """
    Phase 1 Script. Fortify = Make stronger / more solid.
    Summary: Opens the browser, goes to the user's followers page, then follows the users that the users is not
    currently following.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI"""

    global browser
    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/followers?lang=en")
    scroll(browser,10)
    followProfiles(browser, total)
    browser.close()


def followFollowersFollowers(user, passw, total):
    """
    Phase 2 Script. Increase = Gain. Depth = Go deeper.
    Summary: Opens the browser, goes to the user's followers page, selects 4 followers, then follows a determined amount
    of that follower's followers.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI"""

    global browser
    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/followers?lang=en")
    profile_elements = browser.find_elements_by_css_selector(".ProfileCard-screenname .username .u-linkComplex-target")
    profile_elements = profile_elements[0:4]
    profiles = []
    for profile_element in profile_elements:
        profiles.append(profile_element.text)
    for profile in profiles:
        browser.get("https://twitter.com/" + profile + "/followers")
        scroll_until_total(browser, total/4)
        followProfiles(browser, (total / 4), True )
    browser.close()


def searchFollow(user, passw, total, searchTerm):
    """
    Phase 2 / 3 Script. Increase = Gain. Fill = Utilize the rest of the follows. Bulk = Gain  indescriminately, in mass.
    Breath = Expand to further reaches.
    Summary: Opens the browser, goes to the search page of the term specifcied in the GUI, then follows a determined
    amount of those followers
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI
    :param searchTerm: string word determined by the searchTerm field in GUI"""

    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/search?f=users&vertical=default&q=" + searchTerm + "&src=typd")
    scroll(browser, 4)
    followProfiles(browser, total)
    browser.close()


def followProfiles(driver, total):
    """
    Takes all of the profile-cards on the screen, stores them in a list, then follows them using the follow() method
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :param total: int number based off the totalRemaining variable in the GUI
    :param search: bool value that determines the styling of Phase 2: Depth Mode's output
    :return:"""

    def follow(profiles, clicks):
        """
        Collects the follow button elements on the page and follows those accounts, increasing the clicks variable with
        each follow, then subtracting the errors at the end.
        :param profiles: list of browser objects which represent the follow button of the unfollowed profiles
        :param total: int number based off the totalRemaining variable in the GUI
        :param clicks: int taken from the loop. Determines which follow button in the list the program clicks"""

        profiles[clicks].click()
        time.sleep(random.rand(3, 6))

    clicks = 0  # Counts
    errors = 0  # Subtracts
    profiles = driver.find_elements_by_css_selector(".Grid-cell .not-following .follow-text")
    if len(profiles) < total:
        total = len(profiles) - 1   #profiles is array, starts at 0
    while clicks < total:
        try:
            follow(profiles, clicks, total)
        except:
            # Occurs when the account was already followed, or if there was a click error
            errors = errors + 1  # Keep Track of how many errored follows occur
        clicks = clicks + 1  # Increment profile
    ChugaLug.changeRemaining(clicks - errors)  # Changes the total remaining on GUI


def login(driver, user, passw):
    """
    Takes all of the profile-cards on the screen, stores them in a list, then follows them using the follow() method
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :param user: string value used to log into a Twitter account
    :param passw: string value used to log into a Twitter account
    :return:"""

    driver.get('https://twitter.com/login/')  # Open window with the followers page
    usernameField = driver.find_element_by_css_selector("input.js-username-field")
    usernameField.click()
    usernameField.send_keys(user.get())

    passwordField = driver.find_element_by_css_selector("input.js-password-field")
    passwordField.click()
    passwordField.send_keys(passw.get())

    login = driver.find_element_by_css_selector("button.submit")
    login.click()
    time.sleep(1)
    test = str(driver.current_url)
    if str(driver.current_url) != 'https://twitter.com/':
        driver.close()
        raise UserWarning("Login Error: Username or Password incorrect.")
    time.sleep(1)


def scroll(driver, times):
    """
    Goes to the last element on the page, which on twitter, loads more accounts
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :param times: int value, represents the number of time the process repeats
    :return: """

    for i in xrange(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def scrollToBottom(driver):
    """
    Repeats the scoll() script until the last element on the page matches after a scroll
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :return: """

    oldLastProfile = 'a'
    newLastProfile = 'b'
    while oldLastProfile != newLastProfile:
        oldLastProfile = newLastProfile
        scroll(driver, 1)
        time.sleep(2)  # work on the timing
        profiles = driver.find_elements_by_css_selector(".ProfileCard-content")
        newLastProfile = profiles[len(profiles) - 1]
        scroll(driver, 2)


def scroll_until_total(browser, total):
    """
    Scrolls until the follow elements on a page reach a certain total
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :param total: int value that is used to control the len of profiles
    :return: """

    scrollCount = 0
    profiles = browser.find_elements_by_css_selector(".ProfileCard .not-following .follow-text")
    while len(profiles) < total:
        scroll(browser, 1)
        scrollCount = scrollCount + 1
        profiles = browser.find_elements_by_css_selector(".ProfileCard .not-following .follow-text")
        if scrollCount > 20: # Fix endless loop from small amount of followers
            break

def unfollow_if_not_following(profileList):
    """
    The action taken by the Phase 0 script after reaching the bottom of the page.
    Searches the page that have the 'not-following' css class then finds the unfollow
    button and clicks it
    :param profileList: list of elements from driver that are to be unfollowed
    :return: """

    unfollowedTotal = 0
    for profile in profileList:  # here. Profile are fine.
        try:
            unfollowButton = profile.find_element_by_css_selector('.user-actions-follow-button')
            status = profile.find_element_by_css_selector('.FollowStatus')
        except:
            unfollowButton.click()  # not selecting the right object
            unfollowedTotal = unfollowedTotal + 1

def test():
    ChugaLug.set_print_value("hello")

