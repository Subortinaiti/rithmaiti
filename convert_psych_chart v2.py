import json
import sys

chart_name = input("write the name of the chart file (whitout .json) > ")
allowed_notetypes = ["Slash Note","Bullet_Note","Bullet Note","GF Sing",0,"Alt Animation"]
include_special_notes = False
##try:
##    chart_name = sys.argv[1]
##except Exception as E:
##    print(E)
##    input()

with open(chart_name+".json","r") as file:
    psych = json.load(file)

#print(psych)



new = {}
try:
    new["metadata"] = {
                "title": psych["song"]["song"],
                "artist": "Psych converter",
                "scrollspeed": psych["song"]["speed"]+2,
                "baseoffset": 0
        }

except:
    print("error while loading metadata, setting default values...")
    new["metadata"] = {
                "title": "Error",
                "artist": "Error",
                "scrollspeed": 4,
                "baseoffset": 0
        }
    
new["notes"] = []
new["ALTnotes"] = []

for sec in psych["song"]["notes"]:
    if sec["mustHitSection"]:
        for note in sec["sectionNotes"]:
#            print(note)
            if len(note) == 3 or (len(note) == 4 and note[3] in allowed_notetypes) or include_special_notes:
                if  type(note[2]) != str and note[1] <= 3 and note[1] >= 0:

                    if note[2] <= 0.0:
                        new["notes"].append({

                            "time": note[0],
                            "type": "arrow",
                            "column": note[1]
                            })
                    else:
                        new["notes"].append({

                            "time": note[0],
                            "type": "hold",
                            "column": note[1],
                            "length": note[2]
                            })
            
    else:
        for note in sec["sectionNotes"]:
            if len(note) == 3 or (len(note) == 4 and note[3] in allowed_notetypes) or include_special_notes:
                if type(note[2]) != str and note[1] > 3 and note[1]<=7:
                    note[1] = note[1]-4               
                    if note[2] <= 0.0:
                        new["notes"].append({

                            "time": note[0],
                            "type": "arrow",
                            "column": note[1]
                            })
                    else:
                        new["notes"].append({

                            "time": note[0],
                            "type": "hold",
                            "column": note[1],
                            "length": note[2]
                            })        


#saving opponent notes
for sec in psych["song"]["notes"]:
    if not sec["mustHitSection"]:
        for note in sec["sectionNotes"]:
#            print(note)
            if len(note) == 3 or (len(note) == 4 and note[3] in allowed_notetypes) or include_special_notes:
                if  type(note[2]) != str and note[1] <= 3 and note[1] >= 0:

                    if note[2] <= 0.0:
                        new["ALTnotes"].append({

                            "time": note[0],
                            "type": "arrow",
                            "column": note[1]
                            })
                    else:
                        new["ALTnotes"].append({

                            "time": note[0],
                            "type": "hold",
                            "column": note[1],
                            "length": note[2]
                            })
            
    else:
        for note in sec["sectionNotes"]:
            if len(note) == 3 or (len(note) == 4 and note[3] in allowed_notetypes) or include_special_notes:
                if type(note[2]) != str and note[1] > 3 and note[1]<=7:
                    note[1] = note[1]-4               
                    if note[2] <= 0.0:
                        new["ALTnotes"].append({

                            "time": note[0],
                            "type": "arrow",
                            "column": note[1]
                            })
                    else:
                        new["ALTnotes"].append({

                            "time": note[0],
                            "type": "hold",
                            "column": note[1],
                            "length": note[2]
                            })        


#print(new)

print("done!")
with open("chart.json","w") as file:
    json.dump(new,file,indent=6)


























