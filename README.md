# What the bot does :
Given a list of hashtags, this bot will like and comment the first 200 pictures found for each one.
Use the `config.py` file to configure each instagram account you want to run this bot with.

An export summary will be created for each instance in the `/exports` directory.

# How to use :
- Use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create your Python 3 wrapper environment.
- Install dependencies : `pip install -r requirements.txt`
- Download your corresponding chromedriver [here](http://chromedriver.chromium.org/downloads) and save it in your root project's root directory as `chromedriver`. To check your current Chrome version, go [here](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have).
- Configure the `config.py` file.
- Run the bot : `python run.py`

# Configuration : `config.py`
Add as many slaves as you want: 
```
CONFIG_SLAVES = [{ 'ig_login': '',
                   'ig_password': '',
                   'comments': [],
                   'hashtags':[]}, 
                   ...
                ]
```