![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/xEdziu/midi2key/total)
![GitHub Tag](https://img.shields.io/github/v/tag/xEdziu/midi2key)
![pylint](https://img.shields.io/badge/PyLint%20Score-10.00-brightgreen?logo=python&logoColor=white)


# MIDI to PC Keystrokes script

> Can I play Muck on my yamaha keyboard? Let me check...

# Introduction

This script is a product of curiosity and will to have fun with friends! I've created this script to be able to play games on my PC using my Yamaha Piaggero NP-32 keyboard.

One could ask: "Why would you want to do that?". Well, the answer is simple - because I can! And because it's fun!

It's build from the scratch using `mido` and `ctypes` libraries.
I've also used `argparse` to read cli arguments.

# Requirements

- python version `>=3.10`
- install required python libraries:
- - `pip3 install mido`
- - `pip3 install ctype`
- - `pip3 install argparse`

# Usage

- for help, run `python3 midi2key.py -h`
- if you are using this for a first time, you need to know the name of your MIDI device. You can list all available devices by running `python3 midi2key.py -p`. This will list all available MIDI devices (ports) that are connected to your computer - you need to find the name of your MIDI device in this list and copy it. You will need to change the `port_name` (line 39) variable in the script to match the name of your MIDI device, e.g. `port_name = 'Piaggero-1 0` for Yamaha Piaggero NP-12 keyboard
- to listen and discover your notes, run `python3 midi2key.py -l`. This will turn the script into a listener mode, where you can press any key on your MIDI device and the script will print out the note number and velocity of the pressed key
- to start the script, run `python3 midi2key.py`. This will start the script and it will listen to your MIDI device keys. When you press a key on your MIDI device, the script will simulate a key press on your PC keyboard or a mouse action, depending on the configuration you've set in the script.

   *Psst!* Works better when you run your terminal as an administrator!

# Configuration

## Mapping MIDI device keys to PC keyboard keys

In order to do that, scroll down to the `action_map` dictionary and map your MIDI device keys (so called **notes**) to your PC keyboard keys. For example, if you want to map your MIDI device key number (**note**) 60 to your PC keyboard key `a`, you will have to add a new key-value pair to the `action_map` dictionary: `60: 0x41,`. The value is a hexadecimal representation of the key code. You can find the key codes [here](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes).

Currently, the script __does not support__ mapping a combination of keys, like `ctrl+c` or `shift+1`. 

## Mapping MIDI device keys to mouse buttons and mouse movement

You can also map your mouse buttons and mouse movement to your MIDI device keys. For example, if you want to map your MIDI device key number 60 to your left mouse button, you will have to add a new key-value pair to the `action_map` dictionary: `60: mouse_left_click`. You can find other mouse actions in the example `action_map` dictionary I've provided in the script.

After choosing notes that will be responsible for mouse movement and actions, remember to replace already existing notes with yours chosen one in the `mouse_events` list. (You can find it at the top of the script). This list is used to distinguish between normal key presses and special actions like mouse movement or mouse clicks.

# Disclaimer

This script is intended for educational purposes only. I am not responsible for any damage caused by this script. Use it at your own risk. Also, I am aware that this script is not perfect and it can be improved in many ways. If you have any suggestions or improvements, feel free to open an issue or a pull request. This script will not work in the games like Fortnite, PUBG, etc. because of the anti-cheat software that is blocking the usage of such scripts. This script is intended for educational purposes only and should not be used for cheating in games or any other malicious activities. (But you can use it to play Muck with your MIDI device!)

# Making of
This script was initially written from scratch on stream, you can watch it [here](https://www.twitch.tv/videos/2143092512)

