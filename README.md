**Telegram-HTTP-Bridge**

Provides a Python3 based HTTP interface, to which messages (title,message,key) can be pushed, which forwards it to a pre set up telegram bot (https://python-telegram-bot.readthedocs.io/en/stable/)

Can be used to provide all kinds of notifications or alerts to a telegram client on a smartphone or browser.

The key in the keyfile must be the same on all hosts, otherwise the bridge will not forward anything.

The pushnotification shell script can be copied to any host - alter the hostname and port if neccesary.
It uses curl to post to the telegram-http-bridge

You can post with any other http client too, if neccesary.

If you want to use SSL, I suggest using a reverse proxy (e.g. NginX)

**Usage**

Install and spin up the service, then use the included pushnotification script to push messages to the bridge.
The bridge will automatically send them to your telegram bot.

You can use curl directly, or you can use any other HTTP Post request, as long as it contains the needed parameters

**Installation**


Install Python3 and python3-pip
```
apt-get install python3
pip3 install telegram
```


create a group and a user telegram-bridge
```
groupadd -g 800 telegram-bridge
useradd -u 800 -g 800 telegram-bridge
```

git clone this repo
```
git clone https://github.com/GeneralGresi/telegram-http-bridge
```


Select a random key and write it to the keyfile
```
echo -n <SECRET_HTTP_KEY> > keyfile.key
```


Gather the Bottoken from Botfather and write it to bottoken.key
https://www.teleme.io/articles/create_your_own_telegram_bot?hl=en
```
echo -n <BOT_TOKEN> > bottoken.key
```


Get the chat_id from you chat with your bot, and write it to chatid.key
https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659
```
echo -n <CHAT_ID> > chatid.key
```

chown the complete repo (-R) to telegram-bridge:telegram-bridge
```
chown -R telegram-bridge:telegram-bridge <path_to_repo>
```

copy the servicefile to /etc/systemd/system/telegram-http-bridge.service and change paths in accordance to your path
```
cp <path_to_repo>/telegram-http-bridge.service /etc/systemd/system/telegram-http-bridge.service
```

Reload services, enable and start the bridge
```
systemctl daemon-reload
systemctl enable telegram-http-bridge
systemctl start telegram-http-bridge
```
