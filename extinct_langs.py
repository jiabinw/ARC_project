#!/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time,pygame,sys,subprocess,os,random

#INITIALZING THE PYGAME
pygame.init()

#THE INITIAL PARAMETERS
path="/home/pi/extinct_langs/"#path to the sound and image folder
image_format=".jpg" # image format
sound_format=".wav" # sound format
size=width,height=640,480 #to set the size of the image
show_image_time=5000 #milliseconds, the time length to show the image
gap_time=3000 # milliseconds, the gap time length between two viewers, so the sound will not be played too repeatedly
shut_off_delay=10 #seconds, the time length of how long to wait to turn off the monitor when there is nobody around


#LOAD IN AUDIO AND PICTURE
black=0,0,0
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

#COUNT THE FILES IN THE LANGUAGES FOLDER


files=os.listdir(path)
audiofiles=[f for f in files if f.endswith(sound_format)]# this defines the requirement of sound format
purefiles=[]
for i in audiofiles:
    purefiles.append(i.replace(sound_format,""))
print purefiles


amount_of_files=len(purefiles)
amount=range(amount_of_files)

#LOAD IN THE IMAGES
image={}
for i in purefiles:
    path=path+i+image_format# this defines the requirement of image format
    picture=pygame.image.load(path)
    picture=pygame.transform.scale(picture,size)
    image[i]=picture

#PIR CONFIGURATION
GPIO.setmode(GPIO.BOARD)
GPIO_PIR=11
GPIO.setup(GPIO_PIR,GPIO.IN)

#INITIALIZTION
Current_State=0

try:
    
    def turn_on():
        return 0
    #subprocess.call("sh /home/pi/monitor_on.sh", shell=True)
    
    
    
    def turn_off():
        return 0
    #subprocess.call("sh /home/pi/monitor_off.sh", shell=True)
    
    
    
    #hide the cursor
    pygame.mouse.set_visible(False)
    print("already hide the cursor")
    
    turned_off=False
    
    last_motion_time=time.time()
    
    while True:
        Current_State=GPIO.input(GPIO_PIR)
        # TO DETECT THE KEY PRESSING, RIGHT NOW "e" IS THE KEY TO EXIT
        for event in pygame.event.get():
            if event.type== pygame.QUIT: sys.exit()
            if event.type is pygame.KEYDOWN and event.key == pygame.K_e: sys.exit()
        
        
        if Current_State:
            print("got motion!")
            ran=random.choice(purefiles)
            musicpath=path+ran+sound_format
            pygame.mixer.music.load(musicpath)
            
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy()==True:
                continue
            
            
            if turned_off:
                turned_off=False
                
                turn_on()
                print("on!")
        
            screen.blit(image[ran],(0,0))
            pygame.display.flip()
            
            pygame.time.delay(show_image_time)#set the time length of showig image
            screen.fill(black)
            pygame.display.flip()
            
            print("entering gap")
            pygame.time.delay(gap_time)#set the time length of the gap between the current viewer and the coming viewer
            print("gap is over")

            #re-caculating the starting time
    last_motion_time=time.time()
        
        else:
            
            if not turned_off and (time.time()>last_motion_time+shut_off_delay):
                print("no motion for too long time")
                print(time.time()-(last_motion_time+shut_off_delay))
                turned_off=True
                turn_off()
                print("off!")






except KeyboardInterrupt:
    
    GPIO.cleanup()
    sys.exit()
