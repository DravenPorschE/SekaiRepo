import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


timesClicked = 0
isClicking = False

# ----------------------------
# LED Setup
# ----------------------------
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# ----------------------------
# I2C Setup for ADS1115
# ----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# ----------------------------
# FSR on channel 0 (A0)
# ----------------------------
chan = AnalogIn(ads, 0)  # 0 = A0, 1 = A1, 2 = A2, 3 = A3

# ----------------------------
# Threshold to detect touch
# ----------------------------
THRESHOLD = 100  # Adjust after testing your FSR

# ----------------------------
# Main loop
# ----------------------------
try:
    while True:
        fsr_value = chan.value

        if fsr_value > THRESHOLD and isClicking == False:            
            #GPIO.output(LED_PIN, GPIO.HIGH)
            isClicking = True
            timesClicked += 1
            if timesClicked == 2:

                print("Sekai is awake, say a command")
                GPIO.output(LED_PIN, GPIO.HIGH)
                timesClicked = 0
                isClicking = False
                time.sleep(5)
                print("Sekai stopped listening")
        else:
            isClicking = False
            GPIO.output(LED_PIN, GPIO.LOW)

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
