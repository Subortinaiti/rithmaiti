import keyboard
import time
import pygame as pg
import os
import json

pg.mixer.init()

keybinds = ["z","x","2","3"]
hold_threshold = 150


roundto10 = True



print("available songs:")
for item in os.listdir("songs/"):
    print(">",item)
selected_song = input("song name > ")
superstarttime = int(time.time() * 1000)


def main():
    global start_time,sussus
    start_time = None
    key_states = {}  # Dictionary to track key states (pressed or not)
    log = []
    sussus = False  # Flag to indicate if recording has started

    def on_key_event(event):
        global start_time, sussus
        if start_time is None:
            start_time = int(time.time() * 1000)  # Convert seconds to milliseconds

        timestamp = int((time.time() * 1000) - start_time)

        key = event.name
        if event.event_type == keyboard.KEY_DOWN:
            if key == 'space':  # Check if the 'Space' key is pressed
                if not sussus:
                    sussus = True  # Set the flag to True when recording starts
                    pg.mixer.music.load("songs/"+selected_song+"/music.mp3")
                    pg.mixer.music.play()
##                    start_time = time.time() * 1000  # Convert seconds to milliseconds
                    print("the start time is",round(start_time),"ms")
                    
            if sussus:  # Only record key presses if recording has started
                key_states[key] = timestamp
                        
        elif event.event_type == keyboard.KEY_UP:
            if key in key_states:
                press_start = key_states.pop(key)
                press_duration = timestamp - press_start
                log.append([key, press_start, press_duration])
            
    keyboard.hook(on_key_event)

    try:
        print("Press 'Space' to start recording, and 'Esc' to stop.")
        keyboard.wait("space")  # Wait for the 'Space' key to be pressed

        print("Recording keypresses. Press 'Esc' to stop.")
        keyboard.wait("esc")  # Wait for the 'Esc' key to be pressed
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()

    if sussus:
#        print("\nRecorded keypresses:")
        for item in log:
            key, press_start, duration = item
#            print(f"Key: {key} | Time Start: {press_start} ms | Duration: {duration} ms")
    else:
        print("Recording didn't start.")
    return log


def save_dict_to_json(dictionary, filename):
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)



def generate_chart(keystrokes):
    new = {
        "metadata": {
            "title": str(selected_song),
            "artist": "Artist name",
            "scrollspeed": 4,
            "baseoffset": -(start_time - superstarttime)
        },
        "notes": []
    }

    for note in keystrokes:
        if note[0] in keybinds:
            column = keybinds.index(note[0])
            if roundto10:
                note[1] = round(note[1] / 10) * 10

            if note[2] >= hold_threshold:  # Consider entire key press duration for hold notes
                new["notes"].append({
                    "time": note[1],
                    "type": "hold",
                    "column": column,
                    "length": note[2]
                })
            else:
                new["notes"].append({
                    "time": note[1],
                    "type": "arrow",
                    "column": column
                })

    return new


keystrokes = main()
pg.quit()
chart = generate_chart(keystrokes)
save_dict_to_json(chart,"chart.json")
print(chart)















