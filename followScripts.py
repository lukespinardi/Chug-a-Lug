import time
import GUI

from selenium import webdriver


def UnfollowUnfollowers(user, passw):
    '''
    Phase 0 Script. Purge = Get rid of extra bulk.
    Summary: Opens the browser, goes to the user's following page, then unfollows the users that arent following
    the user.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI'''
    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/following?lang=en")
    scrollToBottom(browser)
    profiles = browser.find_elements_by_css_selector(".ProfileCard-content ")
    unfollowIfNotFollowing(profiles)
    browser.close()


def FollowFollowers(user, passw, total):
    '''
    Phase 1 Script. Fortify = Make stronger / more solid.
    Summary: Opens the browser, goes to the user's followers page, then follows the users that the users is not
    currently following.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI'''
    global browser
    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/followers?lang=en")
    scroll(browser,10)
    followProfiles(browser, total)
    browser.close()


def followFollowersFollowers(user, passw, total):
    '''
    Phase 2 Script. Increase = Gain. Depth = Go deeper.
    Summary: Opens the browser, goes to the user's followers page, selects 4 followers, then follows a determined amount
    of that follower's followers.
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI'''
    GUI.writeToLog("Executing Phase 2: Increase (Depth Mode)")
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
    '''
    Phase 2 / 3 Script. Increase = Gain. Fill = Utilize the rest of the follows. Bulk = Gain  indescriminately, in mass.
    Breath = Expand to further reaches.
    Summary: Opens the browser, goes to the search page of the term specifcied in the GUI, then follows a determined
    amount of those followers
    :param user: string twitter login username from GUI
    :param passw: string twitter login password from GUI
    :param total: int number based off the totalRemaining variable in the GUI
    :param searchTerm: string word determined by the searchTerm field in GUI'''
    browser = webdriver.Firefox()
    login(browser, user, passw)
    browser.get("https://twitter.com/search?f=users&vertical=default&q=" + searchTerm + "&src=typd")
    scroll(browser, 4)
    followProfiles(browser, total)
    browser.close()


def followProfiles(driver, total, depth=False):
    """
    Takes all of the profile-cards on the screen, stores them in a list, then follows them using the follow() method
    :param driver: Browser window opened by a 'Phase' script further up the chain
    :param total: int number based off the totalRemaining variable in the GUI
    :param search: bool value that determines the styling of Phase 2: Depth Mode's output
    :return:
    """

    def follow(profiles, clicks, total):
        """
        Takes all of the profile-cards on the screen, stores them in a list, then follows them using the follow() method
        :param profiles: list of browser objects which represent the follow button of the unfollowed profiles
        :param total: int number based off the totalRemaining variable in the GUI
        :param clicks: int taken from the loop. Determines which follow button in the list the program clicks
        """
        #profiles[clicks].click()
        #GUI.writeToLog("Following " + str(clicks) + "/" + str(total))
        print (clicks)
        #time.sleep(random.randint(1, 5))

    clicks = 0  # Counts
    errors = 0
    profiles = driver.find_elements_by_css_selector(".Grid-cell .not-following .follow-text")
    if len(profiles) < total:
        total = len(profiles) - 1
    while clicks < total:
        # IF i made this a method, would it updtate it between flicks? I think so
        try:
            follow(profiles, clicks, total)
        except:
            errors = errors + 1  # Keep Track of how many erred follows occur
        clicks = clicks + 1  # Increment profile
    if depth:
        GUI.writeToLog("Sub-phase Complete: Followed " + str(clicks - errors) + " accounts.")
    else:
        GUI.writeToLog("Phase Complete: Followed " + str(clicks-errors) + " accounts.")
    GUI.changeRemaining(clicks - errors)  # Changes the total remaining on GUI


def login(driver, user, passw):
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
    for i in xrange(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def scrollToBottom(driver):
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
    profiles = browser.find_elements_by_css_selector(".ProfileCard .not-following .follow-text")
    while len(profiles) < total:
        scroll(browser, 1)
        profiles = browser.find_elements_by_css_selector(".ProfileCard .not-following .follow-text")


def unfollowIfNotFollowing(profileList):
    unfollowedTotal = 0
    for profile in profileList:  # here. Profile are fine.
        try:
            unfollowButton = profile.find_element_by_css_selector('.user-actions-follow-button')
            status = profile.find_element_by_css_selector('.FollowStatus')
        except:
            unfollowButton.click()  # not selecting the right object
            unfollowedTotal = unfollowedTotal + 1
    GUI.writeToLog("Phase Complete: Unfollowed " + str(unfollowedTotal) + " accounts")



