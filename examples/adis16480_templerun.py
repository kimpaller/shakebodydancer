# This demo application converts adis16480's accel channel values into keyboard inputs
# great for controlling existing games

import adi #pyadi-iio
import keyboard #pip install keyboard

dev = adi.adis16480(uri='ip:172.20.10.10') # dependent on network

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

def move_x(action):
    if action in ["hard_left", "soft_left"]:
        # keyboard.release('down')
        print("left")
        keyboard.release('right')
        keyboard.press('left')
    elif action in ["hard_right", "soft_right"]:
        # keyboard.release('up')
        print("right")
        keyboard.release('left')
        keyboard.press('right')
    else:
        print("center")
        keyboard.release('right')
        keyboard.release('left')

def move_y(action):
    if action in ["hard_left", "soft_left"]:
        # keyboard.release('down')
        print("up")
        keyboard.press('up')
    elif action in ["hard_right", "soft_right"]:
        # keyboard.release('up')
        print("down")
        keyboard.press('down')
    else:
        print("center")
        keyboard.release('down')
        keyboard.release('up')

while(True):
    for action in actions:
        ll,ul = directions[action]
        if ll <= dev.accel_x_conv <= ul:
            move_x(action)
        if ll <= dev.accel_y_conv <= ul:
            move_y(action)

