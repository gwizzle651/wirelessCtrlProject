from machine import ADC
from picozero import Servo, DistanceSensor
from time import sleep, ticks_us, ticks_diff
import network
import socket
import secrets

# networking setup
ssid = "placeholder"
password = "placeholder"
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(ssid, password)

connectionTimeout = 10

while connectionTimeout > 0:
    if nic.status() == 3:
        break
    connectionTimeout -= 1
    print(f"Connection attempts remaining: {connectionTimeout}")
    sleep(1)

if nic.status() != 3:
    raise RuntimeError(f"Failed to establish a network connection to {ssid}")
else:
    print("Connetion successful")
    networkInformation = nic.ifconfig()
    print(f"IP address: {networkInformation[0]}")

print(nic.isconnected())

'''
# sensor and actuator setup
blue_servo = Servo(16, min_pulse_width=0.00055, max_pulse_width=0.0026)
ds = DistanceSensor(echo=2, trigger=3)
pot_pin = ADC(26)

lastError = 0
errorSum = 0

Kp = .018
Ki = .01480263158
Kd = .005472

servo_base_position = 0.54 # servo midpoint

lastTime = ticks_us() # for intergral and derivative component

buffer = []
while len(buffer) < 3:
    if ds.distance is not None:
        current_cart_position = round(ds.distance * 100, 1)
        buffer.append(current_cart_position)
        if len(buffer) > 3:
            buffer.pop(0)
    sleep(.03)

blue_servo.value = servo_base_position
sleep(1)

while True:
    now = ticks_us()
    timeChange = ticks_diff(now, lastTime) / 1000000

    pot_value = pot_pin.read_u16()
    desired_cart_position = int(33.2 * (pot_value/65535))
    if desired_cart_position < 2:
        desired_cart_position = 2

    if ds.distance is not None:
        current_cart_position = round(ds.distance * 100, 1)
        buffer.append(current_cart_position)
        if len(buffer) > 3:
            buffer.pop(0)
    current_cart_position_average = sum(buffer) / len(buffer)

    error = desired_cart_position - current_cart_position_average

    P_output = Kp * error
    errorSum = errorSum + (error * timeChange)
    I_output = Ki * errorSum
    D_output = Kd * (error - lastError) / timeChange

    servo_correction = P_output + I_output + D_output
    print(servo_correction)
    servo_command = round(servo_base_position - servo_correction, 2)
    print(servo_command)

    if servo_command > .9:
        servo_command = .9
    if servo_command < .18:
        servo_command = .18

    blue_servo.value = servo_command
    lastError = now
    lastTime = ticks_us()

    print(desired_cart_position, current_cart_position_average, servo_command)
    
    sleep(0.03)
'''