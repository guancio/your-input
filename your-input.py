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
            if event.type == QUIT:
                loopQuit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loopQuit = True

        # other event tests, but polling seems to work better in main loop
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
    
        # pygame.display.update()
        if (joystick.get_button(4)):
            device.emit(uinput.REL_Y, -5)
        if (joystick.get_button(5)):
            device.emit(uinput.REL_X, 5)
        if (joystick.get_button(6)):
            device.emit(uinput.REL_Y, 5)
        if (joystick.get_button(7)):
            device.emit(uinput.REL_X, -5)
        device.emit(uinput.REL_X, int(joystick.get_axis(0)*15))
        device.emit(uinput.REL_Y, int(joystick.get_axis(1)*15))
        if (joystick.get_button(12) and (not left)):
            device.emit(uinput.BTN_LEFT, 1);
            left = True
        if (not joystick.get_button(12) and left):
            device.emit(uinput.BTN_LEFT, 0);
            left = False
        if (joystick.get_button(15) and (not left)):
            device.emit(uinput.BTN_RIGHT, 1);
            right = True
        if (not joystick.get_button(15) and left):
            device.emit(uinput.BTN_RIGHT, 0);
            right = False
        time.sleep(interval)
