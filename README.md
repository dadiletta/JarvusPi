# JarvusPi

Home automation project using Raspberry Pi's.  
Designed to use cloud-based variables in the Adafruit.io platform to manage a host of terminal nodes.

### To-Do List
    - Experiment with new IFTTT feeds into Jarvus displays
    - 
    - Incorperate play_speech from https://github.com/mattdy/alarmpi/blob/master/MediaPlayer.py 
        - Festivus: https://learn.adafruit.com/speech-synthesis-on-the-raspberry-pi/speak
    - Phillips Hue https://github.com/studioimaginaire/phue
    - FontAwesome implementation
    - MediaScreen
        - Kodi implementation
        - Bluetooth screen
    
#### Wish List
    - Idle timer sends back to home
    - Install script: http://stackoverflow.com/questions/29222269/is-there-a-way-to-have-a-conditional-requirements-txt-file-for-my-python-applica
    - Cloud-based variables to unify alarm settings
    
#### To-Do Done List
    1. [DONE] Store time and alarm_set in a file so a restarted app can pick-up at last condition
        - http://stackoverflow.com/questions/18040596/how-to-update-a-variable-in-a-text-file
    2. [DONE-ish] Toggle brightness of screen, screen off + restore on touch
    3. [DONE] use cron to reboot machine periodically
    4. [DONE] Hour, minute minus controls
    5. [DONE] Change transitions to slide
    6. [DONE] UI/UX basic grasp of Kivy 

## Hardware

- Raspberry Pi 3 + SD card: https://www.amazon.com/gp/product/B01CD5VC92/
- 7" Touch Screen: https://www.amazon.com/gp/product/B0153R2A9I/
- Display case: https://www.amazon.com/gp/product/B01FZ2RJN8/
                https://www.amazon.com/gp/product/B01HKWAJ6K/
- USB hub: https://www.amazon.com/gp/product/B01285VSCS/
- USB powered speaker: 
- USB cables: https://www.amazon.com/gp/product/B00ZGVMNRQ/


## Manual Installation

- **Raspberry Pi Image**
    - https://www.raspberrypi.org/downloads/raspbian/
    - If rotating the screen is needed, add `lcd_rotate=2` line to /boot/config.txt
    - `sudo apt-get update`, `sudo apt-get upgrade`, `sudo rpi-update` or `sudo apt-get dist-upgrade`
- **Kivy and Things**
    - Follow install instructions: https://kivy.org/docs/installation/installation-rpi.html
        - `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev blueman`
    - `sudo python3 -m pip install Cython`
    - `sudo python3 -m pip install pygments docutils`
    - `sudo python3 -m pip install pygame`
        - If you're using a Mac to test this: https://pythonhosted.org/pyobjc/
    - `sudo python3 -m pip install kivy`
    - `sudo nano /root/.kivy/config.ini` - (after you run a Kivy app)
        - Goto `[input]` section and set it to:
        - `mouse = mouse`
        - `mtdev_%(name)s = probesysfs,provider=mtdev`
        - `hid_%(name)s = probesysfs,provider=hidinput`
- **PyBluez**
    - (Troubleshooting Bluetooth)
        - start with Advanced Communications options provided by the Dexter Industries image
        - `sudo bluetoothctl`
        - `agent on`
        - `default-agent`, `exit`
        - `systemctl status bluetooth`
        - `sudo systemctl start bluetooth`
        - `sudo service bluetooth start`
        - `sudo reboot`
    - http://karulis.github.io/pybluez/
    - `sudo apt-get -y install bluez-hcidump checkinstall libusb-dev libbluetooth-dev`
    - `sudo python3 -m pip install pybluez`
- **Adafruit**
    - `sudo python3 -m pip install Adafruit_IO`
- **playsound**
    - `sudo python3 -m pip install playsound`
- **APScheduler**
    - `sudo python3 -m pip install apscheduler`
- **RPI-Backlight**
    - https://github.com/linusg/rpi-backlight
    - `sudo python3 -m pip install rpi_backlight`
    - `sudo nano /etc/udev/rules.d/backlight-permissions.rules`
    - Insert the line: 
    - `SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"`
- **CEFPython3**  --- EXPERIMENAL CHROME 
    - https://github.com/cztomczak/cefpython/blob/master/docs/Build-instructions.md
    - https://github.com/cztomczak/cefpython/blob/master/docs/Build-instructions.md#requirements
    - `~/cefpython/tools $ sudo python3 build.py 56.0`
- **Setup Folder**
    - `git clone http://github.com/dadiletta/JarvusPi`
    - `touch log_jarvus.log`
    - `mkdir obj`
    - `touch obj/profiles.pkl`
    - `sudo nano private.py`  <-- paste your private vars
        
                MAKER_SECRET = ""
                AIO_KEY = ""
                PROFILE1 = ''
                PROFILE2 = ''
                PI_NAME = ''

- **Auto-Run Jarvus**
    - https://www.raspberrypi.org/documentation/linux/usage/cron.md
    - `sudo crontab -e` and paste the following:
    - `@reboot sudo python3 /home/pi/JarvusPi/jarvus.py` (you may need to adjust your path)
    - `0 0 * * *  reboot` to make sure the script keeps running

## Customizing Jarvus

   - Load your own Private.py
   - Customize your own Adafruit.io feeds
   - Setup your IFTTT triggers