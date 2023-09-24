import os
from sys import platform
from pathlib import Path
import subprocess
import webbrowser
import urllib.parse
import time




if platform != "win32":
    print('fuck off') # would make this use linux instead but im not on my main
    exit()

my_file = Path("PlayIt.exe")
if my_file.is_file():
    print('playit already downloaded')
else:
    print('downloading playit.gg.exe')
    os.system('powershell Invoke-WebRequest -Uri "https://github.com/playit-cloud/playit-agent/releases/download/v0.13.0/playit-windows-x86_64.exe" -OutFile "./PlayIt.exe"')

# check and print playit version
output = subprocess.check_output("PlayIt.exe version", shell=True, encoding="utf-8")
output = output.strip()
output = output.strip("agent ")
print("using playit version " + output)

### Create guest account code

output = subprocess.check_output("PlayIt.exe claim generate", shell=True, encoding="utf-8")
lines = output.splitlines()
whitelist = set('1234567890abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ') # get rid of problematic characters
accode = lines[-1]
accode = accode.strip()
accode = ''.join(filter(whitelist.__contains__, accode))
accode = accode[5:]
print("account creation code is " + accode)
accode = urllib.parse.quote(accode)
webbrowser.open(r"https://playit.gg/login/create?redirect=%2Fclaim%2F" + accode + r"%3F")

### Create Account Secret Token

output = subprocess.check_output("PlayIt.exe claim exchange " + accode, shell=True, encoding="utf-8")
lines = output.splitlines()
whitelist = set('1234567890abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ') # get rid of problematic characters
secret = lines[-1]
secret = ''.join(filter(whitelist.__contains__, secret))
secret = secret[-64:]
print("account secret token is " + secret)

### Create Tunnel

tunnelId = subprocess.check_output("playit.exe --secret " + secret + " tunnels prepare udp 1", shell=True, encoding="utf-8")
tunnelId = tunnelId[:36]
print('Tunnel ID is ' + tunnelId)
# wait for things to generate on their end
print('Generating...')
time.sleep(20)
tunnelIp = subprocess.check_output("playit.exe --secret " + secret + " tunnels list", shell=True, encoding="utf-8")
tunnelPort = tunnelIp
whitelist = set('1234567890.') # get rid of problematic characters
tunnelIp = tunnelIp[280:]
tunnelIp = tunnelIp[:15]
tunnelIp = ''.join(filter(whitelist.__contains__, tunnelIp))
tunnelPort = tunnelPort.strip()
tunnelPort = tunnelPort[:-312]
tunnelPort = tunnelPort[-5:]
tunnelPort = ''.join(filter(whitelist.__contains__, tunnelPort))

print('Tunnel IP is ' + tunnelIp + ':' + tunnelPort)


### Start Up Tunnel

ans = None
ans = input('(leave empty for portal 2 default) Port: ')
whitelist = set('1234567890') # get rid of problematic characters
ans = ''.join(filter(whitelist.__contains__, ans))

if ans == '':
    ans = '27015'

ans = int(ans)
while True:
    if ans > 65535:
        print('Invalid Port.')
        ans = input('(leave empty for portal 2 default) Port: ')
        ans = ''.join(filter(whitelist.__contains__, ans))
        if ans == '':
            ans = '27015'
        ans = int(ans)
    else:
        break
ans = str(ans)
print(r'Using port ' + ans)


os.system("playit.exe --secret " + secret + ' run "' + tunnelId + '=127.0.0.1:' + ans + '"')

print('---------------------')

