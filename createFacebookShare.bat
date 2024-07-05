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
cd /d D:\bons\Thefbkgrupshare
call git clone https://github.com/darideveloper/facebook-groups-post-bot botSutolcer
cd /d D:\bons\Thefbkgrupshare\botSutolcer
call python -m pip install -r requirements.txt 
call python -m venv botSutolcerEnv
call copy d:\bons\Thefbkgrupshare\shareFarmoos\.env d:\bons\Thefbkgrupshare\botSutolcer\.env
call copy d:\bons\Thefbkgrupshare\shareFarmoos\data.json d:\bons\Thefbkgrupshare\botSutolcer\data.json

call copy d:\bons\gESpROJET\bots\marketingBot\doorShareBot.bat d:\bons\gESpROJET\bots\marketingBot\botSutolcerShare.bat
call copy d:\bons\gESpROJET\bots\saveGroup\doorShareBot.bat d:\bons\gESpROJET\bots\saveGroup\botSutolcerGrp.bat

cd /d D:\bons\fbkGrupimages
call mkdir botSutolcer


cd /d D:\bons\Thefbkgrupshare\botSutolcer\Scripts
call activate
cd /d D:\bons\Thefbkgrupshare\botSutolcer
 python __save_groups__.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d D:\FFmpeg"
timeout 10




PAUSE
