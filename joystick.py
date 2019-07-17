#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes

map = {
    "304 (['BTN_A', 'BTN_GAMEPAD', 'BTN_SOUTH']), down": "Red Down",
    "304 (['BTN_A', 'BTN_GAMEPAD', 'BTN_SOUTH']), up": "Red Up",
    "305 (['BTN_B', 'BTN_EAST']), down": "Yellow Down",
    "305 (['BTN_B', 'BTN_EAST']), up": "Yellow Up",
    "306 (BTN_C), down": "Green Down",
    "306 (BTN_C), up": "Green Up",
    "307 (['BTN_NORTH', 'BTN_X']), down": "Blue Down",
    "307 (['BTN_NORTH', 'BTN_X']), up": "Blue Up",
    "308 (['BTN_WEST', 'BTN_Y']), down": "Left Up Down",
    "308 (['BTN_WEST', 'BTN_Y']), up": "Left Up Up",
    "309 (BTN_Z), down": "Right Up Down",
    "309 (BTN_Z), up": "Right Up Up",
    "310 (BTN_TL), down": "Left Down Down",
    "310 (BTN_TL), up": "Left Down Up",
    "311 (BTN_TR), down": "Right Down Down",
    "311 (BTN_TR), up": "Right Down Up",
    "312 (BTN_TL2), down": "Select Down",
    "312 (BTN_TL2), up": "Select Up",
    "313 (BTN_TR2), down": "Start Down",
    "313 (BTN_TR2), up": "Start Up"
}

device = InputDevice("/dev/input/by-id/usb-Gravis_GamePad_Pro_USB-event-joystick")
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print(map[str(categorize(event))[32:]])
