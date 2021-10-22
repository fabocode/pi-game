#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO_1 = 16
BUTTON_GPIO_2 = 5
BUTTON_GPIO_3 = 17
BUTTON_GPIO_4 = 22
BUTTON_GPIO_5 = 26
BUTTON_GPIO_6 = 8
BUTTON_GPIO_7 = 7
BUTTON_GPIO_8 = 14
BUTTON_GPIO_9 = 15
BUTTON_GPIO_10 = 21

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback_1(channel):
    print("Button pressed! 1")
def button_pressed_callback_2(channel):
    print("Button pressed! 2")
def button_pressed_callback_3(channel):
    print("Button pressed! 3")
def button_pressed_callback_4(channel):
    print("Button pressed! 4")
def button_pressed_callback_5(channel):
    print("Button pressed! 5")
def button_pressed_callback_6(channel):
    print("Button pressed! 6")
def button_pressed_callback_7(channel):
    print("Button pressed! 7")
def button_pressed_callback_8(channel):
    print("Button pressed! 8")
def button_pressed_callback_9(channel):
    print("Button pressed! 9")
def button_pressed_callback_10(channel):
    print("Button pressed! 10")

    

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    
    GPIO.setup(BUTTON_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_1, GPIO.FALLING, 
            callback=button_pressed_callback_1, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_2, GPIO.FALLING, 
            callback=button_pressed_callback_2, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_3, GPIO.FALLING, 
            callback=button_pressed_callback_3, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_4, GPIO.FALLING, 
            callback=button_pressed_callback_4, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_5, GPIO.FALLING, 
            callback=button_pressed_callback_5, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_6, GPIO.FALLING, 
            callback=button_pressed_callback_6, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_7, GPIO.FALLING, 
            callback=button_pressed_callback_7, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_8, GPIO.FALLING, 
            callback=button_pressed_callback_8, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_9, GPIO.FALLING, 
            callback=button_pressed_callback_9, bouncetime=300)
    
    GPIO.setup(BUTTON_GPIO_10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO_10, GPIO.FALLING, 
            callback=button_pressed_callback_10, bouncetime=300)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
