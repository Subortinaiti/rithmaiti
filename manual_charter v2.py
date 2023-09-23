import pygame as pg
import random
import math
import json
import time
import os
import sys

pg.init()
try:
    pg.mixer.init()
    sound = True
except:
    sound = False


fps_cap = 100
scale = 60
roundto10 = True
hold_threshold = 150
arrow_center_offset_scale = 0.8
print("available songs:")
for item in os.listdir("songs/"):
    print(">",item)
selected_song = input("write the name of the song you want to load > ")

keybinds = {
    "left":             pg.K_z,
    "down":             pg.K_x,
    "up":               pg.K_KP2,
    "right":            pg.K_KP3
    }

displaysize = (scale*5.25,scale*14)
display = pg.display.set_mode(displaysize)

background_img = pg.transform.scale(pg.image.load("images/background.png"),displaysize)
arrow_img = {
    "left_base": pg.transform.scale(pg.image.load("images/left0.png"), (scale, scale)),
    "left_press": pg.transform.scale(pg.image.load("images/left1.png"), (scale, scale)),
    "up_base": pg.transform.scale(pg.image.load("images/up0.png"), (scale, scale)),
    "up_press": pg.transform.scale(pg.image.load("images/up1.png"), (scale, scale)),
    "down_base": pg.transform.scale(pg.image.load("images/down0.png"), (scale, scale)),
    "down_press": pg.transform.scale(pg.image.load("images/down1.png"), (scale, scale)),
    "right_base": pg.transform.scale(pg.image.load("images/right0.png"), (scale, scale)),
    "right_press": pg.transform.scale(pg.image.load("images/right1.png"), (scale, scale)),
}


def draw_base():
    display.blit(background_img, (0, 0))

    if not keystate[keybinds["left"]]:
        display.blit(arrow_img["left_base"], (0.25 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["left_press"], (0.25 * scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["down"]]:
        display.blit(arrow_img["down_base"], (0.5 * scale + scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["down_press"], (0.5 * scale + scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["up"]]:
        display.blit(arrow_img["up_base"], (0.75 * scale + 2 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["up_press"], (0.75 * scale + 2 * scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["right"]]:
        display.blit(arrow_img["right_base"], (4 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["right_press"], (4 * scale, scale * arrow_center_offset_scale - scale / 2))



def save_chart():
    new =   {
          "metadata": {
            "title": "Song Title",
            "artist": "Artist name",
            "scrollspeed": 4,
            "baseoffset":0
          },      
          "notes": []
          }


    for note in chart:

        if roundto10:
            note[1] = round(note[1]/10)*10





        
        if len(note)==2:
            noteform = {
                "time": note[1],
                "type": "arrow",
                "column": note[0]
                }


            
            new["notes"].append(noteform)
        else:
            noteform = {
                "time": note[1],
                "type": "hold",
                "column": note[0],
                "length":note[2]
                }


            
            new["notes"].append(noteform)            


    print(new)

    with open("chart.json","w") as file:
        json.dump(new,file,indent=6)

    

chart = []

started = False
dead = False
while not started:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            dead = True
            started = True
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            started = True




if sound:
    pg.mixer.music.load("songs/"+selected_song+"/music.mp3")
    pg.mixer.music.play()  

controls = [{"state":False,"start time":0 } for i in range(4)]
clock = pg.time.Clock()
start_time = pg.time.get_ticks()    
runtime = pg.time.get_ticks()
gametime = runtime-start_time
while not dead:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            dead = True
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            dead = True



        runtime = pg.time.get_ticks()
        gametime = runtime-start_time
        keystate = pg.key.get_pressed()



        if event.type == pg.KEYDOWN:
            if event.key in keybinds.values():
                key = event.key
                if key == keybinds["left"]:

                    controls[0] = {"state":True,"start time":gametime}


                elif key == keybinds["down"]:

                    controls[1] = {"state":True,"start time":gametime}


                elif key == keybinds["up"]:

                    controls[2] = {"state":True,"start time":gametime}


                elif key == keybinds["right"]:
                    controls[3] = {"state":True,"start time":gametime}



        if event.type == pg.KEYUP:
            if event.key in keybinds.values():
                key = event.key
                if key == keybinds["left"]:
                    if controls[0]["state"]:
                        controls[0]["state"] = False
                        hold_duration = gametime - controls[0]["start time"]
                        if hold_duration >= hold_threshold:
                            chart.append([0, controls[0]["start time"], hold_duration])
                        else:
                            chart.append([0, controls[0]["start time"]])




                elif key == keybinds["down"]:
                    if controls[1]["state"]:
                        controls[1]["state"] = False
                        hold_duration = gametime - controls[1]["start time"]
                        if hold_duration >= hold_threshold:
                            chart.append([1, controls[1]["start time"], hold_duration])
                        else:
                            chart.append([1, controls[1]["start time"]])
                elif key == keybinds["up"]:
                    if controls[2]["state"]:
                        controls[2]["state"] = False
                        hold_duration = gametime - controls[2]["start time"]
                        if hold_duration >= hold_threshold:
                            chart.append([2, controls[2]["start time"], hold_duration])
                        else:
                            chart.append([2, controls[2]["start time"]])
                elif key == keybinds["right"]:
                    if controls[3]["state"]:
                        controls[3]["state"] = False
                        hold_duration = gametime - controls[3]["start time"]
                        if hold_duration >= hold_threshold:
                            chart.append([3, controls[3]["start time"], hold_duration])
                        else:
                            chart.append([3, controls[3]["start time"]])
                                    





        draw_base()

        clock.tick(fps_cap)
        pg.display.update()





print(chart)
pg.quit()
save_chart()
quit()










            
