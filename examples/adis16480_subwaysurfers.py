# This demo application converts adis16480's accel channel values into keyboard inputs
# great for controlling existing games

import adi #pyadi-iio
import keyboard #pip install keyboard
from collections import Counter
import time

dev = adi.adis16480(uri='ip:172.20.10.10')

dev.rx_output_type = "raw"
dev.rx_enabled_channels = [3, 4, 5]
dev.sample_rate = 20000
dev.rx_buffer_size = 100

print("Product id: " + str(dev.product_id))
print("Serial number: " + dev.serial_number)
print("Firmware revision: " + dev.firmware_revision)
print("Firmware date: " + dev.firmware_date)
print("\nSampling frequency: " + str(dev.sample_rate))


print("\nX acceleration: " + str(dev.accel_x_conv) + " m/s^2")
print("Y acceleration: " + str(dev.accel_y_conv) + " m/s^2")
print("Z acceleration: " + str(dev.accel_z_conv) + " m/s^2")

# limits
directions = {
    "center" : (-1.9,1.9),
    "soft_right" : (-6.9,-2),
    "hard_right" : (-15,-7),
    "soft_left" : (2,6.9),
    "hard_left" : (7,15),
}

# directions
actions=[
    "center",
    "soft_right",
    "soft_left",
    "hard_right",
    "hard_left",
]

recent_actions = []

def move_x(action):
    if action in ["hard_left", "soft_left"]:
        recent_actions.append('left')
    elif action in ["hard_right", "soft_right"]:
        recent_actions.append('right')

def move_y(action):
    if action in ["hard_left", "soft_left"]:
        recent_actions.append('up')
    elif action in ["hard_right", "soft_right"]:
        recent_actions.append('down')

while(True):
    for action in actions:
        ll,ul = directions[action]
        if ll <= dev.accel_x_conv <= ul:
            move_x(action)
        if ll <= dev.accel_y_conv <= ul:
            move_y(action)
    if len(recent_actions) > 2:
        counter = Counter(recent_actions)
        key, count = counter.most_common(1)[0]
    # if len(recent_actions) > 0:
        key = recent_actions[0]
        keyboard.press(key)
        keyboard.release(key)
        print(key)
        # time.sleep(0.05)
        recent_actions = []


