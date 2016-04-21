#!/usr/bin/python

import time

import uinput
import random

import pygame


import pygame, sys, time
from pygame.locals import *

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

interval = .03

# get count of joysticks=1, axes=27, buttons=19 for DualShock 3

joystick_count = pygame.joystick.get_count()
print("joystick_count")
print(joystick_count)
print("--------------")

numaxes = joystick.get_numaxes()
print("numaxes")
print(numaxes)
print("--------------")

numbuttons = joystick.get_numbuttons()
print("numbuttons")
print(numbuttons)
print("--------------")

loopQuit = False
events = (
    uinput.REL_X,
    uinput.REL_Y,
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
)

left = False
right = False

xspeed = 0
yspeed = 0

with uinput.Device(events) as device:
    while loopQuit == False:

        # test joystick axes
        outstr = ""
        for i in range(0,4):
            axis = joystick.get_axis(i)
            outstr = outstr + str(i) + ":" + str(axis) + "|"
        # print(outstr)

        # test controller buttons
        outstr = ""
        for i in range(0,numbuttons):
            button = joystick.get_button(i)
            outstr = outstr + str(i) + ":" + str(button) + "|"
        # print(outstr)

        for event in pygame.event.get():
            continue
        # if event.type == pygame.JOYBUTTONDOWN:
        #print("joy button down")
        # if event.type == pygame.JOYBUTTONUP:
        #print("joy button up")
        # if event.type == pygame.JOYBALLMOTION:
        #print("joy ball motion")
        # axis motion is movement of controller
        # dominates events when used
        # if event.type == pygame.JOYAXISMOTION:
        # print("joy axis motion")
    
        def move(axis1, axis2, button1, button2, acc, slow):
            if (abs(joystick.get_axis(axis1)) < 0.1 and abs(joystick.get_axis(axis2)) < 0.1) and \
               not joystick.get_button(button2) and not joystick.get_button(button1):
                res = 0
            if joystick.get_button(button1):
                res = -10
            if joystick.get_button(button2):
                res = 10
            if (abs(joystick.get_axis(axis2)) >= 0.1):
                res = 15*joystick.get_axis(axis2)
            if (abs(joystick.get_axis(axis1)) >= 0.1):
                res = 30*joystick.get_axis(axis1)
            if joystick.get_button(acc):
                res *= 3
            if joystick.get_button(slow):
                res /= 3
                
            return res;

        xspeed = move(2, 0, 7, 5, 12, 15)
        yspeed = move(3, 1, 4, 6, 12, 15)
            
        if (xspeed > 0 and yspeed > 0):
            xspeed = max(xspeed, yspeed)
            yspeed = xspeed
            
        device.emit(uinput.REL_X, int(xspeed))
        device.emit(uinput.REL_Y, int(yspeed))

        if ((joystick.get_button(14) or joystick.get_button(10)) and (not left)):
            device.emit(uinput.BTN_LEFT, 1);
            left = True
        if (not joystick.get_button(14) and not joystick.get_button(10) and left):
            device.emit(uinput.BTN_LEFT, 0);
            left = False
        if ((joystick.get_button(13) or joystick.get_button(8))and (not right)):
            device.emit(uinput.BTN_RIGHT, 1);
            right = True
        if (not joystick.get_button(13) and not joystick.get_button(8) and right):
            device.emit(uinput.BTN_RIGHT, 0);
            right = False
        time.sleep(interval)
