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
call mkdir botSutolcer


cd /d C:\bons\Thefbkgrupshare
call git clone https://github.com/kitokoh/facebook-group-bot botSutolcer
cd /d C:\bons\Thefbkgrupshare\botSutolcer
call python -m venv botSutolcerEnv
cd /d C:\bons\Thefbkgrupshare\botSutolcer\botSutolcerEnv\Scripts
call activate
cd /d c:\bons\Thefbkgrupshare\botSutolcer
call python -m pip install -r requirements.txt 
call pip install selenium


call copy C:\bons\Thefbkgrupshare\botSutolcer\sample.env C:\bons\Thefbkgrupshare\botSutolcer\.env
call copy C:\bons\Thefbkgrupshare\botSutolcer\sample.data.json C:\bons\Thefbkgrupshare\botSutolcer\data.json

call copy C:\bons\Thefbkgrupshare\botSutolcer\doorShareBot.bat C:.\botSutolcerShare.bat
call copy C:\bons\Thefbkgrupshare\botSutolcer\doorShareBotsv.bat C:.\botSutolcerGrp.bat



cd /d C:\bons\Thefbkgrupshare\botSutolcer\botSutolcerEnv\Scripts
call activate
cd /d c:\bons\Thefbkgrupshare\botSutolcer
 python _save_groups_.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d C:\FFmpeg"
timeout 10




PAUSE