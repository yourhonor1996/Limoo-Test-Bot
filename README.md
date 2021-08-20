# This is a test bot for the limoo platform


## How to install the bot:
    1- install python on your system
    2- extract the files or fork the repository
    3- open install.exe 

## How to run the bot
    1- open terminal and cd to the bot directory (or open a terminal in the directory)
    2- run this command in the terminal:
        py runbot.py

### Bot Management Commands
All bot management commands must be run through "botmange.py"

The commands include:
#### runbot
Starts the bot.

    python botmanage.py runbot
####  install
Upgrades pip and installs all requirements.

    python botmanage.py install
#### runfile {modular filename under src}
Runs a **file inside the "src" folder.** The file path should be modular:

    python botmanage.py runfile utility.gitlab_api

---
### نحوه استفاده از از بات در لیمو
با استفاده از دستوری های زیر میتونید از این بات استفاده بکنید:

### /gitlab-projects : 

بعد از نوشتن این دستور باید نوع پروژه هایی که میخواید مشاهده بکنید رو بنویسید.
یعنی یکی از سه عبارت "private" – "public" – "internal" و یا "all".

هر کدوم از سه عبارت بالا باعث میشن انواع پروژه های مربوط با این visibility ها برای شما نشون داده بشه و عبارت all هم تمام پروژه های شما رو براتون لیست میکنه.
بعد از نوشتن نوع پروژه ها باید gitlab private access token خودتون رو وارد کنید.

برای مثال:

/gitlab-pojects private <<your_token>>

### /help : 

با استفاده از این دستور میتونید به توضیحات روش های استفاده از بات دسترسی پیدا کنید.
