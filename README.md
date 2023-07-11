

# Instagram Bot

Script to automate various activities on Instagram using Selenium.


# Installation

This bot is a Python script and requires Python 3 to be installed in your system. If Python is not installed, you can download it from [Python's official site](https://www.python.org/downloads/).

The bot also requires Selenium, which can be installed using pip (Python's package manager):

```bash
pip install selenium
```

To control the browser, Selenium requires a driver. If you're using Google Chrome, download the appropriate version of ChromeDriver from the [ChromeDriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place the executable in your system's PATH or in the same directory as your script.

# Usage

1.  Open your preferred Python editor.
    
2.  Paste the provided code into the editor.
    
3.  Replace `'your_username'` and `'your_password'` in the line `bot = IGbot('your_username', 'your_password')` with your Instagram username and password.
    
4.  Choose the actions you want to perform. For example:
    
-   If you want the bot to interact with certain posts, you could write:
    
	```python
	bot.activity(['business', 'nature'], [''], 5)
	```
    
    In the example above, the bot will interact with posts that are tagged with 'business' or 'nature'. The second parameter is a list of comments to use when commenting on posts, and the last parameter (5) is the number of seconds to scroll down in the tag page.
    
-   If you want the bot to download images from certain users, you could write:
    
	```python
	bot.download_user_images(['instagram'])
	```
    
In the example above, the bot will download images from the user 'instagram'.
    
5.  Once you have written your commands, you can run your script.
    

Remember to always use bots responsibly and respect the guidelines and rules of the website you're interacting with.

## Classes and Methods:

### IGbot:

This is the main class for interacting with Instagram.

#### `__init__(self, username, password)`

The constructor accepts `username` and `password` as arguments for logging into the Instagram account.

#### `login(self)`

This method is used to log into the Instagram account with the username and password provided during instantiation.

#### `scroll(self, secs)`

This method is used to scroll down the Instagram webpage for the number of seconds provided in the argument.

#### `infinite_scroll(self)`

This method scrolls the Instagram page indefinitely.

#### `nav_user(self, user)`

This method navigates to the profile of the specified user.

#### `click_element(self, xpath)`

This method is used to find an HTML element by its XPATH and perform a click action on it.

#### `write_text(self, xpath, text)`

This method is used to find an HTML element by its XPATH and write text into it.

#### `like_and_follow(self)`

This method is used to like a post and follow the user who posted it.

#### `comment(self, x, comments)`

This method is used to post a comment on a photo.

#### `close(self)`

This method closes the current dialog box on the webpage.

#### `activity(self, tags, comments, secs)`

This method automates the process of interacting with posts on Instagram.

#### `unfollow(self)`

This method reads the usernames from the 'unfollow.txt' file and unfollows them.

#### `download_image(src, image_filename, folder)`

This static method is used to download an image from the provided source URL and save it to a specified folder with a specified filename.

#### `download_user_images(self, users)`

This method downloads all images from the provided list of usernames and saves them into the respective user's folder.

## To-Do:

1.  Change all selectors from XPATH to CLASS_NAME.
2.  Update class names to match the current Instagram's HTML structure.
3.  Add feature to generate comments for posts using GPT-3.