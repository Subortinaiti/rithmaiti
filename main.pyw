import pygame as pg
import random
import math
import json
import time
import os
import tkinter as tk
from tkinter import ttk
#from tkinter import messagebox
#import ctypes as ct



pg.init()
try:
    pg.mixer.init()
    sound = True
except:
    sound = False



keybinds = {
    "left":             pg.K_z,
    "down":             pg.K_x,
    "up":               pg.K_KP2,
    "right":            pg.K_KP3,
    "toggle debug":     pg.K_g,
    "toggle botplay":   pg.K_b
    }
keybindsALT = {
    "left":             pg.K_LEFT,
    "down":             pg.K_DOWN,
    "up":               pg.K_UP,
    "right":            pg.K_RIGHT,

    }


# low level settings

# if the game should show particles when hitting a "great!" note
permissive_particles = False
# if when pressing a key, only the first note in the chart sould be processed
only_one_note_per_keypress = True
# if the game should add score with hold segments
hold_segment_worthiness = False
# if the game should draw the volume indicator in the bottom left
draw_volume_indicator = True
# the length of the display window (scaled)
display_window_height = 10
# how wide should be the window for the death note removal function (scaled)
deathnote_edge = 5
# if the game should check for collision for each deathnote, slowing loading times
accurate_deathnote_removal = False




def string_to_tuple(s): #bygpt
    # Remove parentheses and split the string by commas
    values = s.strip('()').split(',')

    # Convert each value to its appropriate type (int, float, str, etc.)
    converted_values = []
    for val in values:
        val = val.strip()  # Remove extra spaces
        if val.isnumeric():
            converted_values.append(int(val))
        elif val.replace('.', '', 1).isdigit():  # Allowing for floats
            converted_values.append(float(val))
        else:
            converted_values.append(val)

    return tuple(converted_values)


selected_song_sus = ""
class SettingsWindow: #bygpt
    def __init__(self, root, settings):
        self.root = root
        self.root.title("Settings")

        self.settings = settings
        self.entry_widgets = {}
        self.selected_song = ""
        
        self.column_max = round(8)

        
        self.create_widgets()

    def create_widgets(self):
        for idx, (setting_name, setting_value) in enumerate(self.settings.items()):
            #idx = current row, probably means index fuck chatgpt
            current_col = math.floor(idx/self.column_max)*2
            while idx >= self.column_max:
                idx -= self.column_max
            display_name = setting_name.replace("_", " ").capitalize()
            label = ttk.Label(self.root, text=display_name)
            label.grid(row=idx, column=current_col, padx=10, pady=5, sticky="w")

            if isinstance(setting_value, bool):
                # Create a BooleanVar variable and set its initial value
                var = tk.BooleanVar(value=setting_value)
                checkbox = ttk.Checkbutton(self.root, variable=var)
                checkbox.grid(row=idx, column=current_col+1, padx=10, pady=5, sticky="e")
                # Store the BooleanVar variable in the settings dictionary
                self.settings[setting_name] = var
            else:
                entry = ttk.Entry(self.root)
                entry.insert(0, str(setting_value))
                entry.grid(row=idx, column=current_col+1, padx=10, pady=5, sticky="e")
                self.entry_widgets[setting_name] = entry

        label_selected_song = ttk.Label(self.root, text="Selected Song")
        label_selected_song.grid(row=len(self.settings), column=round(current_col/2), padx=10, pady=5, sticky="w")

        songs = os.listdir("songs/")
        selected_song_var = tk.StringVar(self.root)
        selected_song_var.set(songs[0])  # Set the default value to the first song
        dropdown_menu = ttk.Combobox(self.root, textvariable=selected_song_var, values=songs, height=15)
        dropdown_menu.grid(row=len(self.settings), column=round(current_col/2)+1, padx=10, pady=5, sticky="e")
        self.entry_widgets["selected_song"] = dropdown_menu
        done_button = ttk.Button(self.root, text="Done!", command=self.save_settings)
        done_button.grid(row=len(self.settings) + 2,column=round(current_col/2), columnspan=2, padx=10, pady=15)


        
    def save_settings(self):
        global selected_song_sus
        for setting_name, setting_value in self.settings.items():
            if isinstance(setting_value, tk.BooleanVar):
                self.settings[setting_name] = setting_value.get()
            else:
                entry = self.entry_widgets.get(setting_name)
                if entry:
                    self.settings[setting_name] = entry.get()

        selected_song_entry = self.entry_widgets.get("selected_song")
        if selected_song_entry:
            self.selected_song = selected_song_entry.get()
            

            # Check if the selected song is in the available songs list
            available_songs = os.listdir("songs/")
            if self.selected_song not in available_songs:
                print("invalid song selection, random choice enabled.")
                self.selected_song = random.choice(available_songs)
                print("Selected Song:", self.selected_song)
                selected_song_sus = self.selected_song
#                messagebox.showerror("Invalid Song", "The selected song is not present in the available songs.")
#                return  # Prevent saving settings if the song is invalid
            else:
                selected_song_sus = self.selected_song
                print("Selected Song:", self.selected_song)
        save_settings_to_file(self.settings)  # Save settings to the file
        self.root.quit()


def save_settings_to_file(settings):
#    del settings["selected_song"]

    settings["enable_particles"] = int(settings["enable_particles"])
    settings["debug"] = int(settings["debug"])
    settings["low_quality"] = int(settings["low_quality"])
    settings["downscroll"] = int(settings["downscroll"])
    settings["hitsounds"] = int(settings ["hitsounds"])
    settings["hq_notesplashes"] = int(settings ["hq_notesplashes"])
    settings["hitsounds_ignore_volume"] = int(settings ["hitsounds_ignore_volume"])
    settings["ignore_scrollspeed"] = int(settings["ignore_scrollspeed"])


    with open("data/settings.json", "w") as jsonfile:
        json.dump(settings, jsonfile, indent=4)

def main_settings(): #bygpt
    global settings_dict
    if os.path.exists("data/settings.json"):
        with open("data/settings.json", "r") as jsonfile:
            settings_dict = json.load(jsonfile)

            for key in ["enable_particles", "debug", "low_quality", "downscroll", "hitsounds","hq_notesplashes","hitsounds_ignore_volume","ignore_scrollspeed"]:
                    settings_dict[key] = bool(settings_dict[key])


    else:
        settings_dict = {
            "debug": 0,
            "low_quality": 0,
            "enable_particles": 1,
            "downscroll": 0,
            "hitsounds": 1,
            "hitsounds_ignore_volume": 1,
            "hq_notesplashes": 1,
            "ignore_scrollspeed": 1,
            "bad_window": "1.71",
            "good_window": "1.4",
            "great_window": "0.9",
            "awesome_window": "0.5",
            "particle_livetime": "200",
            "scale": "85",
            "fps_cap": "240",
            "offset": "0",
            "arrow_center_offset_scale": "0.9",
            "length_cutoff": "10",
            "score_color": "(255,255,255)",
            "score_livetime": "0",
            "visual_offset": "0.15",
            "scrollspeed_multiplier": "1",
            "deathnotes_frequency": "0",
            "current_volume": "0.4"
            }


    root = tk.Tk()
    app = SettingsWindow(root, settings_dict)
    root.mainloop()
    try:
        root.destroy()
    except:
        pass


print("available songs:")
for item in os.listdir("songs/"):
    print(">",item)


main_settings()




debug = bool(settings_dict["debug"])
low_quality = bool(settings_dict["low_quality"])
enable_particles = bool(settings_dict["enable_particles"])
downscroll = bool(settings_dict["downscroll"])
enable_hitsounds = bool(settings_dict["hitsounds"])
hitsounds_ignore_volume = bool(settings_dict["hitsounds_ignore_volume"])
hq_particles = bool(settings_dict["hq_notesplashes"])
ignore_scrollspeed = bool(settings_dict["ignore_scrollspeed"])

bad_window = float(settings_dict["bad_window"]) * float(settings_dict["scale"])
good_window = float(settings_dict["good_window"]) * float(settings_dict["scale"])
great_window = float(settings_dict["great_window"]) * float(settings_dict["scale"])
awesome_window = float(settings_dict["awesome_window"]) * float(settings_dict["scale"])

particle_livetime = float(settings_dict["particle_livetime"])
scale = float(settings_dict["scale"])
fps_cap = float(settings_dict["fps_cap"])
offset = float(settings_dict["offset"])
arrow_center_offset_scale = float(settings_dict["arrow_center_offset_scale"])
length_cutoff = float(settings_dict["length_cutoff"])
score_color = string_to_tuple(settings_dict["score_color"])
score_fadetime = float(settings_dict["score_livetime"])
visual_offset = float(settings_dict["visual_offset"])
scrollspeed_multiplier = abs(float(settings_dict["scrollspeed_multiplier"]))
current_volume = float(settings_dict["current_volume"])
deathnotes_frequency = float(settings_dict["deathnotes_frequency"])
deathnote_edge = deathnote_edge * scale





if not sound:
    enable_hitsounds = False

if low_quality:
    enable_particles = False
    score_livetime = 0


if score_fadetime > 0:
    print("score particles enabled!")
displaysize = (scale*5.25,scale*display_window_height)
display = pg.display.set_mode(displaysize)
font = pg.font.Font("data/MinecraftRegular-Bmg3.otf",round(scale/3))
bad_rect = pg.Rect(0, arrow_center_offset_scale * scale - bad_window + (visual_offset*scale), displaysize[1], bad_window * 2)
good_rect = pg.Rect(0, arrow_center_offset_scale * scale - good_window + (visual_offset*scale), displaysize[1], good_window * 2)
great_rect = pg.Rect(0, arrow_center_offset_scale * scale - great_window + (visual_offset*scale), displaysize[1], great_window * 2)
awesome_rect = pg.Rect(0, arrow_center_offset_scale * scale - awesome_window + (visual_offset*scale), displaysize[1], awesome_window * 2)
selected_song = selected_song_sus
pg.display.set_caption(selected_song)
pg.mouse.set_visible(False)
botplay = False
blatantbotplay = True
scoregravity = 0.2
missnotehits = 0







print("loading images...")
loadingstart = pg.time.get_ticks()
background_img = pg.transform.scale(pg.image.load("images/background.png"),displaysize)
#background_img = pg.transform.scale(pg.image.load("images/background.png"), displaysize)
if not low_quality:
    arrow_img = {
        "left_base": pg.transform.scale(pg.image.load("images/left0.png"), (scale, scale)),
        "left_press": pg.transform.scale(pg.image.load("images/left1.png"), (scale, scale)),
        "left2_press": pg.transform.scale(pg.image.load("images/left2.png"), (scale, scale)),

        "up_base": pg.transform.scale(pg.image.load("images/up0.png"), (scale, scale)),
        "up_press": pg.transform.scale(pg.image.load("images/up1.png"), (scale, scale)),
        "up2_press": pg.transform.scale(pg.image.load("images/up2.png"), (scale, scale)),

        "down_base": pg.transform.scale(pg.image.load("images/down0.png"), (scale, scale)),
        "down_press": pg.transform.scale(pg.image.load("images/down1.png"), (scale, scale)),
        "down2_press": pg.transform.scale(pg.image.load("images/down2.png"), (scale, scale)),

        "right_base": pg.transform.scale(pg.image.load("images/right0.png"), (scale, scale)),
        "right_press": pg.transform.scale(pg.image.load("images/right1.png"), (scale, scale)),
        "right2_press": pg.transform.scale(pg.image.load("images/right2.png"), (scale, scale))

    }
else:
        arrow_img = {
        "left_base": pg.transform.scale(pg.image.load("images_lq/left0.png"), (scale, scale)),
        "left_press": pg.transform.scale(pg.image.load("images_lq/left1.png"), (scale, scale)),
        "left2_press": pg.transform.scale(pg.image.load("images_lq/left2.png"), (scale, scale)),

        "up_base": pg.transform.scale(pg.image.load("images_lq/up0.png"), (scale, scale)),
        "up_press": pg.transform.scale(pg.image.load("images_lq/up1.png"), (scale, scale)),
        "up2_press": pg.transform.scale(pg.image.load("images_lq/up2.png"), (scale, scale)),

        "down_base": pg.transform.scale(pg.image.load("images_lq/down0.png"), (scale, scale)),
        "down_press": pg.transform.scale(pg.image.load("images_lq/down1.png"), (scale, scale)),
        "down2_press": pg.transform.scale(pg.image.load("images_lq/down2.png"), (scale, scale)),

        "right_base": pg.transform.scale(pg.image.load("images_lq/right0.png"), (scale, scale)),
        "right_press": pg.transform.scale(pg.image.load("images_lq/right1.png"), (scale, scale)),
        "right2_press": pg.transform.scale(pg.image.load("images_lq/right2.png"), (scale, scale))

    }

arrow_img["death_note"] = pg.transform.scale(pg.image.load("images/deathnote.png"), (scale, scale))

if enable_particles:
    if not hq_particles:
    
        particles_img = [
            [
                pg.transform.scale(pg.image.load("images/particles/left/0.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/left/1.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/left/2.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/left/3.png"), (2*scale, 2*scale))
            ],
            [
                pg.transform.scale(pg.image.load("images/particles/down/0.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/down/1.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/down/2.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/down/3.png"), (2*scale, 2*scale))
            ],
            [
                pg.transform.scale(pg.image.load("images/particles/up/0.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/up/1.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/up/2.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/up/3.png"), (2*scale, 2*scale))
            ],
            [
                pg.transform.scale(pg.image.load("images/particles/right/0.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/right/1.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/right/2.png"), (2*scale, 2*scale)),
                pg.transform.scale(pg.image.load("images/particles/right/3.png"), (2*scale, 2*scale))
            ]
        ]


    else:
        hd_splashes_img = pg.image.load("images/particles/notesplashes.png")

        sizes = [
            [623, 646, 194, 186],
            [822, 646, 220, 218],
            [1047, 646, 284, 293],
            [1336, 646, 291, 303],

##            [1632, 646, 202, 211],
##            [0, 972, 235, 240],
##            [240, 972, 298, 315],
##            [543, 972, 315, 321],

            [0, 0, 194, 186],
            [199, 0, 220, 218],
            [424, 0, 284, 293],
            [713, 0, 291, 303],

##            [1009, 0, 202, 211],
##            [1216, 0, 235, 240],
##            [1456, 0, 298, 315],
##            [0, 320, 315, 321],

            [320, 320, 194, 186],
            [519, 320, 220, 218],
            [744, 320, 284, 293],
            [1033, 320, 291, 303],

##            [1329, 320, 202, 211],
##            [1536, 320, 235, 240],
##            [0, 646, 298, 315],
##            [303, 646, 315, 321],

            [863, 972, 194, 186],
            [1062, 972, 220, 218],
            [1287, 972, 284, 293],
            [1576, 972, 291, 303],

##            [0, 1298, 202, 211],
##            [207, 1298, 235, 240],
##            [447, 1298, 298, 315],
##            [750, 1298, 315, 321]
        ]

        
        particles_img = []
        for direction in range(4):
            particles_img.append([])
            for index in range(4):
                x,y,width,height = sizes.pop(0)
                cropped_segment = hd_splashes_img.subsurface(pg.Rect(x, y, width, height))
                scaled_segment = pg.transform.scale(cropped_segment, (2 * scale, 2 * scale))

                particles_img[direction].append(scaled_segment)
            
        


if score_fadetime > 0:
    scores_img = [
        pg.transform.scale(pg.image.load("images/scores/bad.png"),(4*scale,2*scale)),
        pg.transform.scale(pg.image.load("images/scores/good.png"),(4*scale,2*scale)),
        pg.transform.scale(pg.image.load("images/scores/great.png"),(4*scale,2*scale)),
        pg.transform.scale(pg.image.load("images/scores/awesome.png"),(4*scale,2*scale))
        ]




print("Done!("+str(pg.time.get_ticks()-loadingstart)+"ms)")

def Mbox(title, text, style=4):
    result =  ct.windll.user32.MessageBoxW(0, text, title, style)
    if result == 6:  # 6 corresponds to "Yes" button click
        return True
    return False

def rotate_image(image, N):
    if N < 0 or N > 3:
        raise ValueError("N should be between 0 and 3")

    rotated_image = image.copy()

    for _ in range(N):
        rotated_image = pg.transform.rotate(rotated_image, -90)

    return rotated_image


class particle_class:
    def __init__(self,col,livetime,score):
        self.col = col
        self.livetime = [0,livetime]
        self.score = score
        self.pos = (self.col*scale*1.25+scale*0.25-scale/2,scale * arrow_center_offset_scale - scale / 2-scale/2)
        if self.score == "Awesome" or self.score == "Great":
            self.sprites = particles_img[self.col]
        else:
            self.sprites = particles_img[self.col]
        self.start = pg.time.get_ticks()


    def draw_self(self):
        global particles
        if self.livetime[0] < self.livetime[1]:
            self.livetime[0] = pg.time.get_ticks() - self.start
            animstep = min(int((self.livetime[0] / self.livetime[1]) * len(self.sprites)), len(self.sprites)-1)

            display.blit(self.sprites[animstep],self.pos)
        else:
            particles.pop(particles.index(self))
        


def draw_particles():
    for particle in particles:
        particle.draw_self()

class arrow_class:
    def __init__(self,col,time,is_deathnote=False):
        self.col = int(col)
        self.passed = False
        self.keybind = list(keybinds.values())[self.col]
        self.keybindALT = list(keybindsALT.values())[self.col]
        self.is_deathnote = is_deathnote

        
        if not is_deathnote:
            if col == 0:
                self.sprite = arrow_img["left_press"]
            elif col == 1:
                self.sprite = arrow_img["down_press"]
            elif col == 2:
                self.sprite = arrow_img["up_press"]
            elif col == 3:
                self.sprite = arrow_img["right_press"]
        else:            

            if col == 0:
                self.sprite = rotate_image(arrow_img["death_note"],0)
            elif col == 1:
                self.sprite = rotate_image(arrow_img["death_note"],3)
            elif col == 2:
                self.sprite = rotate_image(arrow_img["death_note"],1)
            elif col == 3:
                self.sprite = rotate_image(arrow_img["death_note"],2)

            

        self.time = time
        self.start = self.time * scrollspeed
        self.position = self.start
        self.visible = True

    def draw_self(self):

        self.position = self.start - gametime*scrollspeed+arrow_center_offset_scale*scale-scale/2
        self.pos = (self.col*scale*1.25+scale*0.75,self.position+scale/2)


        if self.position < displaysize[1]+scale and self.visible and self.position > -scale-arrow_center_offset_scale*scale:
            display.blit(self.sprite,(self.col*scale*1.25+scale*0.25,self.position))

        if debug and self.visible:
            pg.draw.circle(display,(255,255,255),self.pos,scale/10)

                

    def collide_self(self, event):
        global score,misses,score_particles,last_score,missnotehits,max_score

        arrow_center = self.pos

        if not self.passed and self.position < -scale-arrow_center_offset_scale*scale and self.visible:
            self.passed = True
            misses += 1   # unused


        if not self.is_deathnote:
            if (event.key == self.keybind or event.key == self.keybindALT) and self.visible:
                outcome = 0
                if awesome_rect.collidepoint(arrow_center):
                    self.visible = False
                    score += 350
                    max_score += 350
                    last_score = "AWESOME! (350)"
                    if enable_particles:
                        particles.append(particle_class(self.col,particle_livetime,"Awesome"))

                    if score_fadetime > 0:
                        score_particles.append(score_particle_class(3))
                    
                    outcome = 1
                elif great_rect.collidepoint(arrow_center):
                    self.visible = False
                    score += 200
                    max_score += 350
                    last_score = "GREAT! (200)"
                    if enable_particles and permissive_particles:
                        particles.append(particle_class(self.col,particle_livetime,"Great"))

                    if score_fadetime > 0:
                        score_particles.append(score_particle_class(2))

                    outcome = 1
                elif good_rect.collidepoint(arrow_center):
                    self.visible = False
                    last_score = "GOOD! (100)"
                    score += 100
                    max_score += 350
                    if score_fadetime > 0:
                        score_particles.append(score_particle_class(1))

                    outcome = 1
                elif bad_rect.collidepoint(arrow_center):
                    self.visible = False
                    last_score = "BAD. (50)"
                    score += 50
                    max_score += 350
                    if score_fadetime > 0:
                        score_particles.append(score_particle_class(0))

                    outcome = 1
                return outcome
        
        else:
            if (event.key == self.keybind or event.key == self.keybindALT) and self.visible:
                outcome=0
                if good_rect.collidepoint(arrow_center):
                    self.visible = False
                    score -= 1000
                    last_score = "FAIL! (-1000)"
                    missnotehits += 1
               

class hold_segment:
    def __init__(self,col,time):
        self.col = int(col)
        self.keybind = list(keybinds.values())[self.col]
        self.keybindALT = list(keybindsALT.values())[self.col]
        self.sprite = pg.transform.scale(pg.image.load("images/hold_section.png"), (scale, scale))
        self.time = time
        self.start = self.time * scrollspeed
        self.position = self.start
        self.visible = True


    def draw_self(self):
        self.position = self.start - gametime*scrollspeed+arrow_center_offset_scale*scale-scale/4
        self.pos = (self.col*scale*1.25+scale*0.75,self.position+scale/4)


        if self.position < displaysize[1]+scale and self.visible and self.position > -scale-arrow_center_offset_scale*scale:
            display.blit(self.sprite,(self.col*scale*1.25+scale*0.25,self.position))
            self.collide_self()


    def collide_self(self):
        global score,max_score
        if awesome_rect.collidepoint(self.pos) and self.visible and (keystate[self.keybind] or keystate[self.keybindALT]):
            self.visible = False
            if hold_segment_worthiness:
                score += 1
                max_score += 1


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pg.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(1)        
    target.blit(temp, location)


class score_particle_class:
    def __init__(self,scoretype):
        self.fadetime = score_fadetime
        self.sprite = scores_img[scoretype]
        self.xvel = random.randint(-2,2)
        self.yvel = random.randint(-5,0)
        self.start_time = pg.time.get_ticks()
        self.pos = [displaysize[0]/2-2*scale,displaysize[1]/2+scale]
    def draw_self(self):
        global score_particles
        self.livetime = pg.time.get_ticks() - self.start_time
        if self.fadetime >= self.livetime and self.pos[1] < displaysize[1]:

            self.pos[0] += self.xvel
            self.yvel += scoregravity
            self.pos[1] += self.yvel

            
#            self.opacity = 255-(255*self.livetime)/self.fadetime
#            blit_alpha(display,self.sprite,self.pos,self.opacity) 
            display.blit(self.sprite,self.pos)
            
        else:
            score_particles.pop(score_particles.index(self))



def load_chart():
    global scrollspeed, chart_file, max_score
    loadingstart = pg.time.get_ticks()
    deathnotes = []
    print("loading chart...")
    chart_file = json.load(open("songs/" + selected_song + "/chart.json"))
    if not ignore_scrollspeed:
        scrollspeed = (chart_file["metadata"]["scrollspeed"] / 4) * scrollspeed_multiplier * (scale/90)
    else:
        scrollspeed = scrollspeed_multiplier / 4  * (scale/90)
    print("detected scrollspeed:",scrollspeed)
    notes = []
    base_offset = chart_file["metadata"]["baseoffset"]

    for note in chart_file["notes"]:
        if note["type"] == "arrow":
            notes.append(arrow_class(note["column"], note["time"] + offset + base_offset + countdown_length))

            if deathnotes_frequency > 0 and random.random() <= deathnotes_frequency:
                rancol = random.randint(0,3)
                while rancol == note["column"]:
                   rancol = random.randint(0,3) 
                deathnotes.append(arrow_class(rancol, note["time"] + offset + base_offset + countdown_length,True))

            
        elif note["type"] == "hold":
            start_time = note["time"] + offset + base_offset + countdown_length
            notes.append(arrow_class(note["column"], start_time))
            
            hold_duration = note["length"]
            segment_duration = scale / 4  # Duration of each segment
            num_segments = int(hold_duration / segment_duration)  # Calculate the number of segments
            
            for i in range(1, num_segments + 1):
                segment_time = start_time + i * segment_duration  # Calculate segment time
                if i%2==0:
                    notes.append(hold_segment(note["column"], segment_time))



    try:
        if deathnotes_frequency > 0:

            for Dnote in deathnotes:
                for note in notes:
                    if Dnote.time <= note.time+deathnote_edge and  Dnote.time >= note.time-deathnote_edge and note.col == Dnote.col:
                        try:
                            deathnotes.pop(deathnotes.index(Dnote))
                        except:
                            None

                    if accurate_deathnote_removal:
                        Dnotepos = (Dnote.col*scale*1.25+scale*0.75,Dnote.position+scale/2)
                        Dnoterect = pg.Rect(Dnotepos,(scale,scale))
                        
                        notepos = (note.col*scale*1.25+scale*0.75,note.position+scale/2-deathnote_edge)
                        noterect = pg.Rect(Dnotepos,(scale,scale+2*deathnote_edge))

                        if Dnoterect.colliderect(noterect):
                            try:
                                deathnotes.pop(deathnotes.index(Dnote))
                            except:
                                None
                            

                            

    except:
        print("error while inserting deathnotes, defaulting to 0 notes")
        deathnotes = []

    
        

        
    notes.extend(deathnotes)



    max_score = 0
##    for note in notes:
##        if type(note) == arrow_class:
##            max_score += 350
##        elif hold_segment_worthiness and type(note) == hold_class:
##            max_score += 10
                
    print("Done!("+str(pg.time.get_ticks()-loadingstart)+"ms)")

    return notes

def draw_countdown():
    current_elapsed = gametime
    count = 3
    while current_elapsed > countdown_length/4:
        count -= 1
        current_elapsed -= countdown_length/4

    if count <= 0:           #had to use <= because if i used == if would show -1 for a split second
        count = "GO!"
    countdown_font = pg.font.Font(None, round(scale * 2))
    countdown_text = countdown_font.render(str(count), True, score_color)
    countdown_rect = countdown_text.get_rect(center=(displaysize[0] / 2, displaysize[1] / 2))
    display.blit(countdown_text, countdown_rect)

def draw_text_centered(text,font,color,center_x,center_y):
    n_text = font.render(str(text), True, color)
    n_rect = n_text.get_rect(center=(center_x, center_y))
    display.blit(n_text, n_rect)




def draw_base():
    display.blit(background_img, (0, 0))

    if debug:
        pg.draw.rect(display,(255,100,100),bad_rect)
        pg.draw.rect(display,(100,255,100),good_rect)
        pg.draw.rect(display,(100,100,255),great_rect)
        pg.draw.rect(display,(255,100,255),awesome_rect)

    if not keystate[keybinds["left"]] and not keystate[keybindsALT["left"]]:
        display.blit(arrow_img["left_base"], (0.25 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["left2_press"], (0.25 * scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["down"]] and not keystate[keybindsALT["down"]]:
        display.blit(arrow_img["down_base"], (0.5 * scale + scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["down2_press"], (0.5 * scale + scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["up"]] and not keystate[keybindsALT["up"]]:
        display.blit(arrow_img["up_base"], (0.75 * scale + 2 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["up2_press"], (0.75 * scale + 2 * scale, scale * arrow_center_offset_scale - scale / 2))

    if not keystate[keybinds["right"]] and not keystate[keybindsALT["right"]]:
        display.blit(arrow_img["right_base"], (4 * scale, scale * arrow_center_offset_scale - scale / 2))
    else:
        display.blit(arrow_img["right2_press"], (4 * scale, scale * arrow_center_offset_scale - scale / 2))


def do_chart():
    for note in chart:
        note.draw_self()

def calculate_score_percentage(score):
    try:
        n = (score/max_score)*100
        return str(round(n,2))+"%"
    except:
        return str("N/A")
    

def draw_overlay():
    overlay_items = []
    overlay_items.append([font.render("SCORE: "+str(score),True,score_color),True])
    overlay_items.append([font.render("FPS: "+str(round(clock.get_fps())),True,score_color),True])
    try:
        overlay_items.append([font.render("TIME: "+str((round(pg.mixer.music.get_pos()/1000,1))),True,score_color),sound and amogus])
    except:
        None
    overlay_items.append([font.render(str(last_score),True,score_color),True])
    overlay_items.append([font.render("VOL: "+str(round(current_volume*100))+"%",True,score_color),draw_volume_indicator])
    overlay_items.append([font.render("ACC: ("+calculate_score_percentage(score)+")",True,score_color),True])
    overlay_items.append([font.render("BOTPLAY",True,score_color),botplay and blatantbotplay])
    overlay_items.append([font.render("CB: "+str(missnotehits),True,score_color),deathnotes_frequency > 0 and missnotehits > 0])



       





     


    pos = [104,displaysize[1]] # bottom left

    for item in overlay_items:

        #if last pos was left
        if pos[0] == scale*0.1:
            pos[0] = displaysize[0]-scale*0.1-item[0].get_rect().width
        else:
            pos[0] = scale*0.1
            pos[1] -= 0.4*scale
        
        if item[1]:
            try:
                display.blit(item[0],pos)
            except:
                None


        




def draw_score_particles():

    for score in score_particles:
        score.draw_self()



def main():
    global started,dead,clock,gametime,chart,keystate,score,debug,particles,current_volume,misses,botplay
    global amogus,countdown_length,score_particles,last_score,hitsound_snd,enable_hitsounds,blatantbotplay
    global pausedtime,max_score
    
    if sound:
        hitsound_snd = pg.mixer.Sound("data/hitsound.mp3")
        countdown_snd = pg.mixer.Sound("data/countdown.mp3")
    countdown_length = 1400 #ms
    chart = load_chart()
    last_score = "None"
    if enable_particles:
        particles = []

    score_particles = []
    clock = pg.time.Clock()
    score = 0
    misses = 0
    pausedtime = 0
    started = False
    dead = False
    amogus = False
    display.blit(font.render("PRESS SPACE TO START!",True,score_color),(scale*0.1,displaysize[1]-scale*0.4))
    draw_text_centered("SPACE!",pg.font.Font(None, round(scale * 2)),score_color,displaysize[0]/2,displaysize[1]/2)
    pg.display.flip()
    while not started:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                dead = True
                started = True
                amogus = True
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                started = True



            
    if sound:
        if not hitsounds_ignore_volume:
            hitsound_snd.set_volume(current_volume)    
        countdown_snd.set_volume(current_volume)  
        countdown_snd.play()

    start_time = pg.time.get_ticks()
    while not amogus:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                dead = True
                started = True
                amogus = True



        runtime = pg.time.get_ticks()
        gametime = runtime-start_time

        if gametime >= countdown_length:
            amogus = True
        



        keystate = pg.key.get_pressed()
        draw_base()
        do_chart()
        draw_overlay()
        draw_countdown()
        pg.display.flip()



    if sound:
        try:
            pg.mixer.music.load("songs/"+selected_song+"/music.mp3")
        except:
            try:
                pg.mixer.music.load("songs/"+selected_song+"/song.mp3")
            except:
                try:
                    pg.mixer.music.load("songs/"+selected_song+"/song.ogg")
                except:
                    pg.mixer.music.load("songs/"+selected_song+"/music.ogg")
        pg.mixer.music.play()
        pg.mixer.music.set_volume(current_volume)
        
    runtime = pg.time.get_ticks()
    gametime = runtime-start_time




    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                dead = True
                
            if event.type == pg.KEYDOWN and ((event.key in keybinds.values()) or (event.key in keybindsALT.values())):
                if event.key == keybinds["toggle debug"]:
                    debug = not debug
                    print("debug:",debug)
                elif event.key == keybinds["toggle botplay"]:
                    botplay = not botplay
                    if blatantbotplay:
                        print("botplay:",botplay)
                else:
                    for note in chart:
                        if note.visible and type(note) == arrow_class and not botplay:
                            if note.collide_self(event):
                                chart.pop(chart.index(note))
                                if enable_hitsounds:
                                    hitsound_snd.play()
                                if only_one_note_per_keypress:
                                    break
                            
            if event.type == pg.KEYDOWN and event.key == pg.K_KP_PLUS and sound:
                current_volume = min(1.0, current_volume + 0.1)
                pg.mixer.music.set_volume(current_volume)
                if enable_hitsounds and not hitsounds_ignore_volume:
                    hitsound_snd.set_volume(current_volume)
                
            if event.type == pg.KEYDOWN and event.key == pg.K_KP_MINUS and sound:
                current_volume = max(0.0, current_volume - 0.1)
                pg.mixer.music.set_volume(current_volume)                
                if enable_hitsounds and not hitsounds_ignore_volume:
                    hitsound_snd.set_volume(current_volume)            


            if event.type == pg.KEYDOWN and event.key == pg.K_h and sound:
                enable_hitsounds = not enable_hitsounds
                print("hitsounds:",enable_hitsounds)

            if event.type == pg.KEYDOWN and event.key == pg.K_KP0:
                blatantbotplay = not blatantbotplay


            if event.type == pg.KEYDOWN and event.key in [pg.K_RETURN,pg.K_SPACE,pg.K_KP_ENTER]:
                pausedstart = pg.time.get_ticks()
                paused_ = True
                if sound:
                    pg.mixer.music.pause()
                pg.display.set_caption(selected_song + " (paused)")
                while paused_:
                    for event in pg.event.get():
                        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            paused_ = False
                            dead = True
                        if event.type == pg.KEYDOWN and event.key in [pg.K_RETURN,pg.K_SPACE,pg.K_KP_ENTER]:
                            paused_=False
                            pausedtime += (pg.time.get_ticks()-pausedstart)
                            if sound:
                                pg.mixer.music.unpause()
                            pg.display.set_caption(selected_song)
                    draw_text_centered("PAUSED",pg.font.Font("data/MinecraftRegular-Bmg3.otf",round(scale)),score_color,displaysize[0]/2,displaysize[1]/2)
                    pg.display.flip()


        draw_base()

        if botplay:
            for note in chart:
                if awesome_rect.collidepoint(note.pos) and note.visible and ((type(note) == arrow_class and not note.is_deathnote) or type(note) == hold_segment):
                    note.visible = False
                    if not blatantbotplay:
                        if type(note) == arrow_class:
                            score += 350
                            max_score += 350
                            last_score = "AWESOME! (350)"
                            if score_fadetime > 0:
                                score_particles.append(score_particle_class(3))

                            if enable_hitsounds:
                                hitsound_snd.play()
                                

                        elif type(note) == hold_segment:
                            if hold_segment_worthiness:
                                score += 1
                        
                    if enable_particles and type(note) == arrow_class:
                        particles.append(particle_class(note.col,particle_livetime,"Awesome"))
                        
                    if type(note) == hold_segment:
                        if note.col == 0:
                            display.blit(arrow_img["left2_press"], (0.25 * scale, scale * arrow_center_offset_scale - scale / 2))
                        elif note.col == 1:
                            display.blit(arrow_img["down2_press"], (0.5 * scale + scale, scale * arrow_center_offset_scale - scale / 2))
                        elif note.col == 2:
                            display.blit(arrow_img["up2_press"], (0.75 * scale + 2 * scale, scale * arrow_center_offset_scale - scale / 2))
                        elif note.col == 3:
                            display.blit(arrow_img["right2_press"], (4 * scale, scale * arrow_center_offset_scale - scale / 2))
                            
        do_chart()
        runtime = pg.time.get_ticks()
        gametime = runtime-start_time-pausedtime
        keystate = pg.key.get_pressed()

        

        if enable_particles:
            draw_particles()
            if score_fadetime > 0:
                draw_score_particles()
        draw_overlay()
        clock.tick(fps_cap)
        pg.display.flip()


main()
pg.quit()
quit()
