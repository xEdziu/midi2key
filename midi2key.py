import mido
import argparse
from ctype import c_uint, windll

KEYEVENTF_UP = 0x0002
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

mouse_events = {60, 62, 59, 64, 71, 74, 72, 58, 54, 56}
senisitivity = 30 # Change this to adjust default mouse sensitivity

# Setup argparse
def setup_argparse():
    version = "1.0"
    parser = argparse.ArgumentParser(
        prog="midi2key.py",
        description="Handle MIDI inputs and simulate keyboard or mouse actions.",
        epilog="https://www.github.com/xEdziu/midi2key")
    parser.add_argument('-l', '--listen-only', action='store_true', help='Only listen to MIDI inputs without simulating any action.')
    parser.add_argument('-p', '--ports', action='store_true', help='Display available MIDI ports')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}', help='Show program\'s version number')
    return parser.parse_args()

def main():
    
    args = setup_argparse()

    if args.ports:
        ports = mido.get_input_names()
        if not ports:
            print("No MIDI ports available. Please connect a MIDI device and try again.")
            return
        print("Accessible MIDI ports:")
        for port in ports:
            print("- ", port)
        return

    ports = mido.get_input_names()
    port_name = 'Piaggero-1 0'  # Change this to your MIDI port name
    
    if not ports:
        print("No MIDI ports available. Please connect a MIDI device and try again.")
        return
    
    with mido.open_input(port_name) as inport:
        print(f"Listening on port: {port_name}")
        for messeage in inport:
            if messeage.type == 'note_on':
                if messeage.velocity > 0:
                    print(f'\n\nKey down: {messeage.note} with velocity: {messeage.velocity}')
                    if not args.listen_only and messeage.note:
                        ret = action_map.get(messeage.note)
                        if ret:
                            if messeage.note in mouse_events and callable(ret):
                                ret()
                            else:
                                press_key(ret)
                else:
                    print(f'Key up: {messeage.note}')
                    if not args.listen_only and messeage.note:
                        hex = action_map.get(messeage.note)
                        if hex and messeage.note not in mouse_events:
                            release_key(hex)
            elif messeage.type == 'note_off':
                print(f'Key up: {messeage.note}')
                if not args.listen_only and messeage.note:
                    hex = action_map.get(messeage.note)
                    if hex and messeage.note not in mouse_events:
                        release_key(hex)

def press_key(hexCode):
    windll.user32.keybd_event(hexCode, 0, 0, 0)
    print(f"Pressed key: {chr(hexCode)}")
    
def release_key(hexCode):
    windll.user32.keybd_event(hexCode, 0, KEYEVENTF_UP, 0)
    print(f"Pressed key: {chr(hexCode)}")
    
def mouse_move_right():
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(senisitivity), # dx - horizontal change
        c_uint(0), # dy - vertical change 
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move right")
    
def mouse_move_left():
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(-senisitivity), # dx - horizontal change
        c_uint(0), # dy - vertical change 
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move left")
    
def mouse_move_up():
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(-senisitivity), # dy - vertical change 
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move up")
    
def mouse_move_down():
    windll.user32.mouse_event(
        c_uint(MOUSEEVENTF_MOVE), #hex for event that we will be simulating
        c_uint(0), # dx - horizontal change
        c_uint(senisitivity), # dy - vertical change 
        c_uint(0), # if mouse wheel used
        c_uint(0)  # additional flags
    )
    print("Mouse move right")
    
def mouse_left_click():
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
    
def mouse_left_click():
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
    
def modify_sensitivity(value):
    global senisitivity
    senisitivity = max(1, senisitivity + value)
    print(f"New sensitivity: {senisitivity}")

def reset_sensitivity():
    global senisitivity
    senisitivity = 30
    print(f"Sensitivity reset: {senisitivity}")
    
    
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
    