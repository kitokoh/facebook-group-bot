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
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.freqtrade.io/en/stable/configuration/

@echo off
cd /d D:\bons\fbkgrupshare\sharefbkgrp\Scripts
call activate
cd /d D:\bons\fbkgrupshare

 python __post_in_groups__.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d D:\FFmpeg"
timeout 10




PAUSE
