@ECHO OFF

:: This CMD script provides you with your operating system, hardware and network information.

TITLE My System Info

ECHO Please wait... Gathering system information.

ECHO =========================

ECHO OPERATING SYSTEM

systeminfo | findstr /c:"OS Name"

systeminfo | findstr /c:"OS Version"

ECHO =========================

ECHO BIOS

systeminfo | findstr /c:"System Type"

ECHO =========================

ECHO MEMORY

systeminfo | findstr /c:"Total Physical Memory"

ECHO =========================

ECHO CPU

wmic cpu get name

ECHO =========================

ECHO NETWORK ADDRESS

ipconfig | findstr IPv4

ipconfig | findstr IPv6

@echo off
cd /d C:\
call mkdir bons
cd /d C:\bons
call mkdir Thefbkgrupshare 
cd /d C:\
call mkdir image 
cd /d C:\image
call mkdir fbkGrupimages
cd /d C:\image\fbkGrupimages
call mkdir whattsBot


cd /d C:\bons\Thefbkgrupshare
call git clone https://github.com/kitokoh/facebook-group-bot whattsBot
cd /d C:\bons\Thefbkgrupshare\whattsBot
call python -m venv whattsBotEnv
cd /d C:\bons\Thefbkgrupshare\whattsBot\whattsBotEnv\Scripts
call activate
cd /d c:\bons\Thefbkgrupshare\whattsBot
call python -m pip install -r requirements.txt 


call copy C:\bons\Thefbkgrupshare\whattsBot\sample.env C:\bons\Thefbkgrupshare\whattsBot\.env
call copy C:\bons\Thefbkgrupshare\whattsBot\sample.data.json C:\bons\Thefbkgrupshare\whattsBot\data.json

call copy C:\bons\Thefbkgrupshare\whattsBot\doorShareBot.bat C:.\whattsBotShare.bat
call copy C:\bons\Thefbkgrupshare\whattsBot\doorShareBotsv.bat C:.\whattsBotGrp.bat



cd /d C:\bons\Thefbkgrupshare\whattsBot\whattsBotEnv\Scripts
call activate
cd /d c:\bons\Thefbkgrupshare\whattsBot
 python _save_groups_.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d C:\FFmpeg"
timeout 10




PAUSE