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

```bash
$ pip install -r requirements.txt
```

# Usage

- for help, run `python3 midi2key.py -h`
- if you are using this for a first time, you need to know the name of your MIDI device. You can list all available devices by running `python3 midi2key.py -p`. This will list all available MIDI devices (ports) that are connected to your computer - you need to find the name of your MIDI device in this list and copy it. You will need to change the `port_name` variable in `config.yaml` to match the name of your MIDI device, e.g. `port_name: 'Piaggero-1 0'` for Yamaha Piaggero NP-12 keyboard.
- to listen and discover your notes, run `python3 midi2key.py -l`. This will turn the script into a listener mode, where you can press any key on your MIDI device and the script will print out the note number and velocity of the pressed key
- to start the script, run `python3 midi2key.py`. This will start the script and it will listen to your MIDI device keys. When you press a key on your MIDI device, the script will simulate a key press on your PC keyboard or a mouse action, depending on the configuration you've set in the `config.yaml`.

  _Psst!_ Works better when you run your terminal as an administrator!

# Configuration

## Setting up your device and mouse sensitivity

Open `config.yaml` in your favorite text editor.
At the top of the file, you can set your MIDI port name, e.g. for Casio USB-MIDI device it would be something like this:
`port_name: 'CASIO USB-MIDI 0'`
You can also adjust the default speed of the mouse cursor movements by modifying the `sensitivity: 30` parameter.

## Mapping MIDI device keys to PC keyboard keys

In order to map your MIDI notes to PC keystrokes, scroll down to the `bindings` section in the `config.yaml`. For example, if you want to map your MIDI device key number (**note**) 28 to your PC keyboard key `A`, you will have to add a line:
`28: A`
You can find all available string representations of the key codes inside the `keys` section in the yaml file.

You can also use numbers directly or ignore a node via null like this:
`55: null`
(although notes that are not mapped to any key will be ignored by default, so you can just skip them without adding a null value)

Currently, the script **does not support** mapping a combination of keys, like `ctrl+c` or `shift+1`.

## Mapping MIDI device keys to mouse types and sensitivity adjustments

You can also map your mouse buttons and mouse movement directly to your MIDI device keys within the same `bindings` section. For example, if you want to map your MIDI device key number 60 to your mouse "move up" action, simply use its string representation:
`60: mouse_move_up`

Available mouse and setting functions are:

- `mouse_move_up`, `mouse_move_down`, `mouse_move_left`, `mouse_move_right`
- `mouse_left_click`, `mouse_middle_click`, `mouse_right_click`
- `increase_sensitivity`, `decrease_sensitivity`, `reset_sensitivity`

# Disclaimer

This script is intended for educational and entartainement purposes only. I am not responsible for any damage caused by this script. Use it at your own risk. Also, I am aware that this script is not perfect and it can be improved in many ways. If you have any suggestions or improvements, feel free to open an issue or a pull request. This script may not work in the games like Fortnite, PUBG, etc. because of the anti-cheat software that is blocking the usage of such scripts. This script is intended for educational and entertainment purposes only and should not be used for cheating in games or any other malicious activities. (But you can use it to play Muck with your MIDI device!)
