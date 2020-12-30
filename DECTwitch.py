import socket
import logging
import os
import subprocess
import re
from emoji import demojize


server = 'irc.chat.twitch.tv'
port = 6667
nickname = "NICKNAME"
token = 'OAUTH'     # Get this from https://twitchapps.com/tmi/
channel = '#[CHANNEL NAME]' # This is the name of your twitch channel


# Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="&Y/&m/&d - &H:&M:&S", handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

sock = socket.socket()
sock.connect((server, port))

# Send details
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send('PONG\n'.encode('utf-8'))

    elif len(resp) > 0:

        demojizedResp = demojize(resp)
        logging.info(demojizedResp)
        user = demojizedResp.strip().split(":")
        msg = re.sub(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :', " ", demojizedResp)
        print(f'{user[1].split("!")} says: {msg}')
        subprocess.Popen(f'say.exe [:rate 300] [:phoneme on] {user[1].split("!")[0]} says: {msg}')
        # os.system(f'say.exe [:rate 300] [:phoneme on] """" {user[1].split("!")[0]} says: {msg} """"')     !!! LITERALLY A FUCKING RAT, DONT USE !!!
        
