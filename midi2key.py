'''This code handles MIDI inputs and simulates keyboard or mouse actions.'''
import argparse
import os
import sys
import time
from ctypes import c_uint, windll
import mido
import yaml

KEYEVENTF_UP = 0x0002
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
SENSITIVITY = 30 # Configured via yaml
mouse_events = set()
action_map = {}

# Setup argparse
def setup_argparse():
    '''Setup argparse for the program.'''
    version = "2.0"
    parser = argparse.ArgumentParser(
        prog="midi2key.py",
        description="Handle MIDI inputs and simulate keyboard or mouse actions.",
        epilog="https://www.github.com/xEdziu/midi2key")
    parser.add_argument('-l', '--listen-only',
                        action='store_true',
                        help='Only listen to MIDI inputs without simulating any action.')
    parser.add_argument('-p', '--ports',
                        action='store_true',
                        help='Display available MIDI ports')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'%(prog)s {version}',
                        help='Show program\'s version number')
    return parser.parse_args()
def handle_ports(args, config_port_name):
    '''Handle MIDI ports and return the port name.'''
    if args.ports:
        # pylint: disable=no-member
        ports = mido.get_input_names()
        if not ports:
            print("No MIDI ports available. Please connect a MIDI device and try again.")
            return None
        print("Accessible MIDI ports:")
        for port in ports:
            print("- ", port)
        return None
    # pylint: disable=no-member
    ports = mido.get_input_names()
    port_name = config_port_name
    if not ports:
        print("No MIDI ports available. Please connect a MIDI device and try again.")
        return None
    return port_name
def handle_note_down(note, listen_only):
    '''Handle a key down event.'''
    if listen_only or not note:
        return
    ret = action_map.get(note)
    if ret is not None:
        if note in mouse_events and callable(ret):
            ret()
        else:
            press_key(ret)

def handle_note_up(note, listen_only):
    '''Handle a key up event.'''
    if listen_only or not note:
        return
    ret = action_map.get(note)
    if ret is not None and note not in mouse_events:
        release_key(ret)

def handle_messages(inport, args):
    '''Handle MIDI messages and simulate actions.'''
    while True:
        for message in inport.iter_pending():
            if message.type == 'note_on':
                if message.velocity > 0:
                    print(f'\n\nKey down: {message.note} with velocity: {message.velocity}')
                    handle_note_down(message.note, args.listen_only)
                else:
                    print(f'Key up: {message.note}')
                    handle_note_up(message.note, args.listen_only)
            elif message.type == 'note_off':
                print(f'Key up: {message.note}')
                handle_note_up(message.note, args.listen_only)
        time.sleep(0.01)
def load_config():
    '''Load configuration from config.yaml.'''
    # pylint: disable=global-statement
    global SENSITIVITY
    config_file = 'config.yaml'

    if not os.path.exists(config_file):
        print(f"Error: '{config_file}' not found.")
        print("Please ensure 'config.yaml' is in the same directory.")
        sys.exit(1)

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    key_map = config.get('keys', {})
    func_map = {
        'mouse_move_up': mouse_move_up,
        'mouse_move_down': mouse_move_down,
        'mouse_move_left': mouse_move_left,
        'mouse_move_right': mouse_move_right,
        'mouse_left_click': mouse_left_click,
        'mouse_middle_click': mouse_middle_click,
        'mouse_right_click': mouse_right_click,
        'increase_sensitivity': lambda: modify_sensitivity(10),
        'decrease_sensitivity': lambda: modify_sensitivity(-10),
        'reset_sensitivity': reset_sensitivity
    }

    SENSITIVITY = config.get('sensitivity', 30)
    port_name_cfg = config.get('port_name', '')

    bindings = config.get('bindings', {})
    action_map.clear()
    mouse_events.clear()

    for note, action_name in bindings.items():
        if action_name is None:
            continue
        # Convert integer keys to string to match YAML keys if needed
        action_name_str = (
            str(action_name).upper() if isinstance(action_name, (int, str))
            else action_name
        )

        if action_name in func_map:
            action_map[note] = func_map[action_name]
            mouse_events.add(note)
        elif action_name_str in key_map:
            action_map[note] = key_map[action_name_str]
        elif action_name in key_map:
            action_map[note] = key_map[action_name]
        else:
            print(f"Warning: Unknown action '{action_name}' for note {note}")

    return port_name_cfg

def main():
    '''Main function to run the program.'''
    port_name_cfg = load_config()
    args = setup_argparse()
    port_name = handle_ports(args, port_name_cfg)
    if port_name:
        # pylint: disable=no-member
        try:
            with mido.open_input(port_name) as inport:
                print(f"Listening on port: {port_name}")
                handle_messages(inport, args)
        except OSError:
            print(f"\nError: Could not open MIDI port '{port_name}'.")
            print("Please check your configuration or connect the device.")
            print("- Use 'python midi2key.py -p' to list available ports.")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            sys.exit(0)
def press_key(hex_code):
    '''Press a key based on the hex code provided.'''
    windll.user32.keybd_event(hex_code, 0, 0, 0)
    print(f"Pressed key: {chr(hex_code)}")
def release_key(hex_code):
    '''Release a key based on the hex code provided.'''
    windll.user32.keybd_event(hex_code, 0, KEYEVENTF_UP, 0)
    print(f"Pressed key: {chr(hex_code)}")
def mouse_move_right():
    '''Move the mouse right.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(SENSITIVITY), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move right")
def mouse_move_left():
    '''Move the mouse left.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(-SENSITIVITY), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move left")
def mouse_move_up():
    '''Move the mouse up.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(-SENSITIVITY), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move up")
def mouse_move_down():
    '''Move the mouse down.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(SENSITIVITY), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move down")
def mouse_left_click():
    '''Simulate a left mouse click.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_LEFTDOWN), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_LEFTUP), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse left click")
def mouse_right_click():
    '''Simulate a right mouse click.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_RIGHTDOWN), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_RIGHTUP), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse right click")
def mouse_middle_click():
    '''Simulate a middle mouse click.'''
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MIDDLEDOWN), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MIDDLEUP), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(0), # dy - vertical change
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse middle click")
def modify_sensitivity(value):
    '''Modify the mouse sensitivity.'''
    # pylint: disable=global-statement
    global SENSITIVITY
    SENSITIVITY = max(1, SENSITIVITY + value)
    print(f"New sensitivity: {SENSITIVITY}")
def reset_sensitivity():
    '''Reset the mouse sensitivity to default.'''
    # pylint: disable=global-statement
    global SENSITIVITY
    SENSITIVITY = 30
    print(f"Sensitivity reset: {SENSITIVITY}")
if __name__ == '__main__':
    main()
    