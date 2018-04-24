from django.shortcuts import render
import json
from django.http import JsonResponse
import pigpio
import time
import RPi.GPIO as GPIO

#Init Pigpio
pi = pigpio.pi()

# Enable power pins
power_enable_pins = [23,24,25]
GPIO.setmode(GPIO.BCM)
for x in power_enable_pins:
    GPIO.setup(x,GPIO.OUT, initial=0)

# Colors
red = 0
green = 120
blue = 200
half_of_min = int(green/2)
blue_green_ratio = blue/green

# Create your views here.
counter = 0
def micron_slider(request):
    leds_off()
    power_disable_all_pins()
    context={}
    return(render(request, 'demo/micron_slide_show.html',context))

def change_led(request):
    params = request.GET
    slide = str(params["slide"])
    
    leds_off()
    power_disable_all_pins()
    
    # Main Overview Page
    # Power all LEDs on 1/2 way.
    if slide == '0':
        power_enable_all_pins()
        leds_on_half_1()
    # AI Slide
    elif slide == "1":
        power_disable_all_pins()
        GPIO.output(23,GPIO.HIGH)
        leds_on_half_1()
        time.sleep(2)
        leds_on_half_2()
    #DRAM Slide
    elif slide == "2":
        power_disable_all_pins()
        GPIO.output(24,GPIO.HIGH)
        leds_on_half_1()
        time.sleep(2)
        leds_on_half_2()
    #Storage Slide
    elif slide == "3":
        power_disable_all_pins()
        GPIO.output(25,GPIO.HIGH)
        leds_on_half_1()
        time.sleep(2)
        leds_on_half_2() 
    
    context = {
    }
    return JsonResponse(json.loads(json.dumps(context)))

# LEDs color to off.
def leds_off():
    pi.set_PWM_dutycycle(22,0) #Red
    pi.set_PWM_dutycycle(27,0) #Green
    pi.set_PWM_dutycycle(17,0) # Blue

# LEDs color to half brightness
def leds_on_half_1():  
    for x in range(0,half_of_min):
        pi.set_PWM_dutycycle(22,0) #Red
        pi.set_PWM_dutycycle(27,x) #Green
        pi.set_PWM_dutycycle(17,int(x*blue_green_ratio)) # Blue
        time.sleep(.05)

# LEDs color to full brightness
def leds_on_half_2():  
    for x in range(0,half_of_min):
        x=x+60
        pi.set_PWM_dutycycle(22,0) #Red
        pi.set_PWM_dutycycle(27,x) #Green
        pi.set_PWM_dutycycle(17,int(x*blue_green_ratio)) # Blue
        time.sleep(.05)

# Disable all LED power
def power_disable_all_pins():
    for x in power_enable_pins:
        GPIO.output(x,GPIO.LOW)

# Enable all LED power (used for slide 0)
def power_enable_all_pins():
    for x in power_enable_pins:
        GPIO.output(x,GPIO.HIGH)
