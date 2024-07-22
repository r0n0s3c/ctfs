# Intro

Flowers!
Flag format: CACI{}
Author: CACI | @nihilistpenguin

# Website

Once we open the link, we get three different functionalities: login, sign up and password reset. 
In this challenge we get a zip file that contains the website source code. Lets analyze the source code for vulnerabilities.
Looking at the admin.php seems like our goal is to ge into the admin page because there is the flag.
In order to get there we need fulfill two requirements: 
- Have a session: `$_SESSION['userid']`
- Be admin: `$_SESSION['username'] == "admin"`

One strange thing I notice is that in the home page they refer to webhook to reset the password. Additionally in dbh.php they create the admin user with the following fields: username, password and webhook. This last field is not common to be saved because it can be accessed without having credentials. 
The modules login.inc.php, logout.inc.php, reset.inc.php and signup.inc.php are the entry points of our requests.
We need to find a hole in one of them in order to exploit this challenge. Login and logout do not have any problems, login verifies the username and password separately, first the user and then the password. The logout is a simple logout php script.
Signup.inc.php has two functions: check user and setup user. Check user verifies if the user passed already exists and setup user performs a INSERt query if the user does not exists. This module apparently do not have any way we can do nothing. 
Reset.inc.php module receives two values, a token and the username. It will check if the user exists, and if so, it will extract the webhook link, generate a temppass and execute a command: `exec("php ../scripts/send_pass.php " . $this->tmpPass . " " . $this->wh . " > /dev/null 2>&1 &");` If we can create a user and developed a payload iin the webhook field maybe we can execute this command with the desired action.  Our goal is to obtain the flag so we need to look at the contents of the admin.php. 
