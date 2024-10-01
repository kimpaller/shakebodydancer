# Copyright (C) 2021 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import sys

import adi
import matplotlib.pyplot as plt
import numpy as np

def calculate_rms(values):
    return np.sqrt(np.mean(np.square(values)))

# Set up ADIS16480
dev = adi.adis16480(uri='ip:172.27.13.245')

dev.rx_output_type = "raw"
dev.rx_enabled_channels = [3, 4, 5]
dev.sample_rate = 20000
dev.rx_buffer_size = 10

print("Product id: " + str(dev.product_id))
print("Serial number: " + dev.serial_number)
print("Firmware revision: " + dev.firmware_revision)
print("Firmware date: " + dev.firmware_date)

print("\nX acceleration: " + str(dev.accel_x_conv) + " m/s^2")
print("Y acceleration: " + str(dev.accel_y_conv) + " m/s^2")
print("Z acceleration: " + str(dev.accel_z_conv) + " m/s^2")



print("\nSampling frequency: " + str(dev.sample_rate))

9
for _ in range(1000):
    data = dev.rx()
    # print(calculate_rms(data[0]))
    # print(calculate_rms(data[1]))
    # print(calculate_rms(data[2]))
    # print("----------")


    # print(data[0])
    # print(data[1])
    # print(data[2])
    plt.clf()
    for i, d in enumerate(data):
        plt.plot(d, label=dev._rx_channel_names[dev.rx_enabled_channels[i]])
    plt.legend()
    plt.show(block=False)
    plt.pause(0.1)
