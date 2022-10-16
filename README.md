# MagicMirror
A Magic Mirror Web Interface Deployed to Heroku


Due to the increasing prices of the Rapsberry Pi in 2022, It was unlikely that I could afford to buy one. 

The Pi Zero, which I had a couple of, were used to run a Magic Mirror. Unfortunately, the Pi Zero W was not cut out to run chromium, let alone any kind of a webserver which could serve pages. 

I split the desired task load as follows

1) The Rapsberry Pi would just run a browser on startup and load a Webpage running on the internet. 

2) A Flask app which would run on heroku, that the browser in the Pi loads. 

This Repo hosts the Flask Application which can be deployed to Heroku. 


# Setting up the Raspberry Pi

Install Raspbian Lite on an SD card. Use the Pi Imager software (https://www.raspberrypi.com/software/) to write the image of the Raspbian List onto the SD card. 

# Minimum Environment for GUI Applications

Usually the graphical environment for GNU/Linux consists of four parts:

X server (usually X.Org)
Window manager (Openbox, XFWM, …)
Desktop environment (PIXEL, LXDE, MATE, …)
Login manager (for example LightDM)

However, we only want to run a single application (the web browser) in full screen – so we don’t need a desktop environment. And we already have autologin enabled (and no other users will ever use the Pi) – so we don’t need a login manager either.

The bare minimum we need are X server and window manager. Let’s install just that:


[code]sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox[/code]

