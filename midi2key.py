'''This code handles MIDI inputs and simulates keyboard or mouse actions.'''
import argparse
from ctypes import c_uint, windll
import mido

KEYEVENTF_UP = 0x0002
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
SENSITIVITY = 30 # Change this to adjust default mouse sensitivity
mouse_events = {60, 62, 59, 64, 71, 74, 72, 58, 54, 56}

# Setup argparse
def setup_argparse():
    '''Setup argparse for the program.'''
    version = "1.0"
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
def handle_ports(args):
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
    port_name = 'Piaggero-1 0'  # Change this to your MIDI port name
    if not ports:
        print("No MIDI ports available. Please connect a MIDI device and try again.")
        return None
    return port_name
def handle_messages(inport, args):
    '''Handle MIDI messages and simulate actions.'''
    for message in inport:
        if message.type == 'note_on':
            if message.velocity > 0:
                print(f'\n\nKey down: {message.note} with velocity: {message.velocity}')
                if not args.listen_only and message.note:
                    ret = action_map.get(message.note)
                    if message.note in mouse_events and callable(ret) and ret:
                        ret()
                    else:
                        press_key(ret)
            else:
                print(f'Key up: {message.note}')
                if not args.listen_only and message.note:
                    ret = action_map.get(message.note)
                    if ret and message.note not in mouse_events:
                        release_key(ret)
        elif message.type == 'note_off':
            print(f'Key up: {message.note}')
            if not args.listen_only and message.note:
                ret = action_map.get(message.note)
                if ret and message.note not in mouse_events:
                    release_key(ret)
def main():
    '''Main function to run the program.'''
    args = setup_argparse()
    port_name = handle_ports(args)
    if port_name:
        # pylint: disable=no-member
        with mido.open_input(port_name) as inport:
            print(f"Listening on port: {port_name}")
            handle_messages(inport, args)
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
    action_map = {
        28: 0x41, #A
        29: 0x57, #W
        31: 0x53, #S
        33: 0x44, #D
        60: mouse_move_up,
        62: mouse_move_down,
        59: mouse_move_left,
        64: mouse_move_right,
        48: 0x20, #Spacebar
        37: 0x10, #Shift
        35: 0x45, #E
        30: 0x09, #Tab
        61: 0x4D, #M
        58: lambda: modify_sensitivity(10),
        54: reset_sensitivity,
        56: lambda: modify_sensitivity(-10),
        71: mouse_left_click,
        72: mouse_middle_click,
        74: mouse_right_click
    }
    main()
    