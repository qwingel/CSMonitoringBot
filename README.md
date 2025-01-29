# Telegram Bot Monitoring Servers 
Telegram bot monitoring of game servers. The following games are supported: <b>Half-Life, Half-Life 2, Left 4 Dead, Left 4 Dead 2, Team Fortress 2, Counter-Strike, Counter-Strike 2</b>

[Now bot is starting with @CSServerMonitoringBot](https://t.me/CSServerMonitoringBot)

![Static Badge](https://img.shields.io/badge/GitHub-Antarktida-qwingel?style=for-the-badge&color=blue&link=https%3A%2F%2Fgithub.com%2Fqwingel)
![GitHub top language](https://img.shields.io/github/languages/top/qwingel/CSMonitoringBot?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/qwingel/CSMonitoringBot?style=for-the-badge)
![Logotype](./banner/logo.png)

## Dependencies 
This program depends on the Python interpreter version 3.6 or higher, PIP 9.0.1 or higher.

## Installation (Linux)
1. Cloning a repository
   
    ```git clone https://github.com/qwingel/CSMonitoringBot.git```

2. Move to word directory

    ```cd CSMonitoringBot```

3. Creating a virtual environment

    ```python -m venv venv```

4. Activating the virtual environment

    ```source venv/bin/activate```

5. Installing dependencies
   
   ```pip install -r requirements.txt```

6. Starting bot
   
   ```python main.py```

## Files descrtiptions
|   Name      |   Description                                                                  |
|-------------|--------------------------------------------------------------------------------|
| .env	      | Stores the key of the telebot                                                  |
| database.py | Works with dictionaries of servers and their categories and the data.json file |
| datas.json  | Stores lists of user servers                                                   |
| lang.py	  | Working with users language                                                    |
| lang.json	  | Stores users language                                                          |
| lang.yaml	  | Stores phrases of different languages                                          |
| main.py	  | Is the entry point. Works with TeleBot.                                        |
| requirements.txt | Stores dependies of project.                                              |
| server.py	  | Gets information about servers                                                 |

## Support
### If you have any questions/recommendations or have a problem, please contact [Me (t.me)](https://t.me/koreanrating).