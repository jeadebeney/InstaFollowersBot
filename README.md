# What the bot does :
Given a list of hashtags, this bot will like and comment the first 200 pictures found for each one.
There are over 1500 different comment combinations, which you can extend in the `config.py` file.

The bot can run in multiple concurrent threads : also set up in `config.py` file.

An export summary will be created for each instance in the `/exports` directory.

# How to use :
- Use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create your Python 3 wrapper environment (please call it `virtualenv`, or make sure it is git ignored).
- Install dependencies : `pip install -r requirements.txt`
- Download your corresponding chromedriver [here](http://chromedriver.chromium.org/downloads) and save it in your root project's root directory as `chromedriver`. To check your current Chrome version, go [here](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have).
- Create the following `.env` file and your your instagram credentials :
```
PYI_IG_EMAIL=...
PYI_IG_PASSWORD=...
CHROME_DRIVER_PATH=./chromedriver
```
- Run the bot : `python run.py`

# Configuration : `config.py`
Add as many slaves as you want: 
```
SLAVES = [
    {
        'name': 'slave_name', # used to name the export file
        'hashtags': ['hashtag_1', 'hashtag_2', 'hashtag_3'],
    },
    ...
]
```
Create your custom comments by populating the different `comments` fields :
```
COMMENTS = {
    'adjectives': ['Nice', 'Cool', ...],
    'photos': ['photo', 'pic', ...],
    'smileys': [':-)', ':)', ...],
    'ponctuation': ['!', '!!', ...]
}

```
