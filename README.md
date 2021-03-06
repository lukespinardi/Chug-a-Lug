NAME
	Chug-a-Lug

INSTALLATION
	Once the repository is installed on the user’s device, there will be a 
	folder named 'Chug-a-Lug’ containig python scripts, a README.txt file, a 
	FUTURE.txt file, and a setup.sh bash script. The bash script is 
	executable, and is used to setup the environment for Chug-a-Lug. 

	To install Chug-a-lug on your device run 'setup.sh'. It may take a while. 

	If there are any errors that occur during the installation of Chug-a-Lug, 
	the user must install the dependencies manually. 

	To run Chug-a-Lug, these programs and modules must be installed on the 
	user’s device: 

	First, the user must install Python, preferably a variation of 
	version 2.7.*. It is the foundation for the program. 

	Next, install pip, a python based downloading agent. 

	Finally using pip, download selenium, Tkinter, and gecko-webdriver. The 
	script is currently designed to do all of these automatically, 
	except for the gecko-webdriver. Gecko-webdriver must be installed manually.
	
DESCRIPTION	
	Chug-a-Lug can either be run by either one of two ways. Both of these 
	methods require the user to have python as an environmental variable 
	pointing to the location of their Python 2.7.* directory. The preferred 
	way is to run the directory 'Chug-a-Lug' as a module.

	    $ python Chug-a-Lug

	The other method of running Chug-a-Lug is by running the 'ChugaLug.py' file
	inside of the 'Chug-a-Lug' directory.

	    $ cd Chug-a-Lug
	    $ python Chug-a-Lug

    	When the user runs the module (or script) a GUI pops up. There are several 
	fields contained within the GUI that the user must fill. 
	
    'Username' and 'password' 
	The login credential for the twitter accountthe user wishes the formula to
	be run on.

    "# of follows remaining' 
	Represents the amount of followers the account is allowed to follow before
	they reach their daily limit. 

    'Follow Formula Mode' 
	A drop down box that contains the variations of the formula for gaining 
	followers. 
	
    'Target Market' 
	A field where the user is able to write an interest their desired users may
 	have. The 'Breadth Mode' script will pursue these followers.

	An output box issues different messages depending on the status of the 
	user. If the user is arriving for the first time, then there will be a 
	message greeting them and giving instructions on how to us the application.
 	If the user has used the program before but has never excuted the formula 
	on their account, the output displays a different message. Finally, if 
	the user has run the formula successfully, there will be a message saying 
	how long until the formula runs again.

	As long the application remains open and it has been run once before, 
	Chug-a-Lug will run continuously. The formula will automatically follow 
	and unfollow accounts on Twitter, obtaining followers for the user in a 
	gloriously endless cycle.

