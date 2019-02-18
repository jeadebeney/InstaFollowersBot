# Readme if you want this to work, don't if you don't care
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