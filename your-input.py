#!/usr/bin/python

import uinput

import pygame, sys, time
from pygame.locals import *

import config

active_config = config.TwoAxes;

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

def max_abs_axis(p_list):
    if len(p_list) == 0:
        return 0
    m = abs(joystick.get_axis(p_list[0]))
    for x in p_list:
        m = max(m, abs(joystick.get_axis(x)))
    return m

def max_axis(p_list):
    if len(p_list) == 0:
        return 0
    m = abs(joystick.get_axis(p_list[0]))
    s = 1 if joystick.get_axis(p_list[0]) >= 0 else -1
    for x in p_list:
        v = abs(joystick.get_axis(x))
        if v > m:
            m = v
            s = 1 if v >= 0 else -1
    return m*s

def or_button(p_list):
    if len(p_list) == 0:
        return False
    m = joystick.get_button(p_list[0])
    for x in p_list:
        m = m or joystick.get_button(x)
    return m

def move(axis1, axis2, button1, button2, acc, slow):
    if (max_abs_axis(axis1+axis2) < 0.1 and not or_button(button1+button2)):
        res = 0
    if or_button(button1):
        res = -10
    if or_button(button2):
        res = 10
    if (max_abs_axis(axis2) >= 0.1):
        res = 15*max_axis(axis2)
    if (max_abs_axis(axis1) >= 0.1):
        res = 30*max_axis(axis1)
    if or_button(acc):
        res *= 3
    if or_button(slow):
        res /= 3
    
    return res;

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
    
        xspeed = move(active_config.x_fast_axis, active_config.x_slow_axis,
                      active_config.x_left_button, active_config.x_right_button,
                      active_config.acc_button, active_config.slow_button)

        yspeed = move(active_config.y_fast_axis, active_config.y_slow_axis,
                      active_config.y_top_button, active_config.y_bottom_button,
                      active_config.acc_button, active_config.slow_button)
        
        if (xspeed > 0 and yspeed > 0):
            xspeed = max(xspeed, yspeed)
            yspeed = xspeed
            
        device.emit(uinput.REL_X, int(xspeed))
        device.emit(uinput.REL_Y, int(yspeed))

        if (or_button(active_config.left_buttons) and (not left)):
            device.emit(uinput.BTN_LEFT, 1);
            left = True
        if (not or_button(active_config.left_buttons) and left):
            device.emit(uinput.BTN_LEFT, 0);
            left = False
        if (or_button(active_config.right_buttons) and (not right)):
            device.emit(uinput.BTN_RIGHT, 1);
            right = True
        if (or_button(active_config.right_buttons) and right):
            device.emit(uinput.BTN_RIGHT, 0);
            right = False
        time.sleep(interval)
