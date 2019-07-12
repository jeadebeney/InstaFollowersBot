# What the bot does
- You give 4 lists of hashtags as parameters, example: my_hashtags_list = ["beach", "sun", "nature", "mountain"]
- You enter your IG credentials in the .env file
- The robot opens a window on your chrome browser and logs into your IG account.
- Then, it searches in the research bar the first hashtag of the first list of hashtags you gave as a parameter, here "beach". 
- For each one of the 200 first pictures that are displayed, it leaves a like to the picture, and display a comment. There are 1500+ combinations of different comments, and time out of three, it leaves in the comment the username of the picture. Once the bot left commments one the 200 pictures, it does the same for the second hashtag ("sun") etc. When it reaches the end of the hashtags list, it restarts from the beginning of the list. 
- The bot does this operation 4 times in parallel. This is why you have to give 4 lists of hashtags


# How to use the bot
- Use virtualenv to create your python3 wrapper environment (please call it `virtualenv`, or make sure it is git ignored)
- Run `pip install -r requirements.txt` to install dependencies
- Download your platform's chrome driver (https://chromedriver.storage.googleapis.com/index.html?path=73.0.3683.20/) and save it in your projects directory as `chromedriver`
- Create a `.env` file and add the following environment variables:
```
PYI_IG_EMAIL=...
PYI_IG_PASSWORD=...
CHROME_DRIVER_PATH=./chromedriver
```
- launch the bot with `python3 run.py`
