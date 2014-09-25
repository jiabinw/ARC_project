#!/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time,pygame,sys,subprocess,os,random

#INITIALZING THE PYGAME
pygame.init()

#LOAD IN AUDIO AND PICTURE
size=width,height=640,480 #to set the size of the image 
black=0,0,0
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

#COUNT THE FILES IN THE LANGUAGES FOLDER
files=os.listdir("/home/pi/extinct_langs/")
audiofiles=[f for f in files if f.endswith(".wav")]# this defines the requirement of sound format 
purefiles=[]
for i in audiofiles:
    purefiles.append(i.replace(".wav",""))
print purefiles 
   

amount_of_files=len(purefiles)
amount=range(amount_of_files)

#LOAD IN THE IMAGES 
image={}
for i in purefiles:
    path="/home/pi/extinct_langs/"+i+".jpg"# this defines the requirement of image format
    picture=pygame.image.load(path)
    picture=pygame.transform.scale(picture,size)
    image[i]=picture

#PIR CONFIGURATION 
GPIO.setmode(GPIO.BOARD)
GPIO_PIR=11
GPIO.setup(GPIO_PIR,GPIO.IN)

#INITIALIZTION 
Current_State=0
#HERE TO CHANGE THE TIME OF HOW LONG TO SHUT OFF THE MONITOR 
shut_off_delay=10

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
            musicpath="/home/pi/extinct_langs/"+ran+".wav"
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
            
            pygame.time.delay(5000)#set the time length of showig image 
            screen.fill(black)
            pygame.display.flip() 
         
            print("entering gap")
            pygame.time.delay(3000)#set the time length of the gap between the current viewer and the coming viewer
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
