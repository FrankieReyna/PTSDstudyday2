from pathlib import Path
import os
from psychopy import visual, event, core
from PIL import Image
import random
import pandas as pd
from psychopy.clock import Clock
from present import present_instruction
import psychopy.gui as psygui
import datetime

#TODO: add instrusion and distress question to practice!
#TODO: We also should add a final slide to indicate the end of the task

def pres_img(win, mainimg, imgtype):

    c = Clock()


    correct = 0
    rt = 0
    intrusionnum = 0

    text = visual.TextStim(win, "Do you recall being presented with this image the day before?", pos=(0, 400), color="black", font='arial', height=50, wrapWidth = 1200)
    image1 = visual.ImageStim(win, image=mainimg, pos=(0, 0))
    text1 = visual.TextStim(win, "Yes (1)", pos=(-400, -400), color="black", font='arial', height=35)
    text2 = visual.TextStim(win, "No (9)", pos=(400, -400), color="black", font='arial', height=35)

    text.draw()
    image1.draw()
    text1.draw()
    text2.draw()
    win.flip()

    # Wait for user response
    c.reset()
    
    while True:

        intrusionnum = "0"
        keys = event.waitKeys()[0]
        
        rt = c.getTime()

        #Buttons to quit
        if 'escape' in keys or 'close' in keys:
            core.quit()

        if keys == '1' or keys == '9':  # User decides on image
            correct = f"{imgtype}" == keys[0]
            #If yes ask intrusions
            if keys == '1':

                text3 = visual.TextStim(win, "In the past 24 hours, how frequently did you think of this image out of the blue? Please indicate the frequency from 1 (never) to 9 (all the time)", pos=(0, 400), color="black", font='arial', height=50, wrapWidth=1200)
                text3.draw()
                image1.draw()
                win.flip()

                #Wait for answer on intrusions
                while True:

                    intrusionnum = event.waitKeys()[0]

                    if 'escape' in intrusionnum or 'close' in intrusionnum:
                        core.quit()
                    #Try to take their response, if it isnt a number in range, except case and try again
                    try:
                        if int(intrusionnum) in range(1, 10):
                            intrusionnum = int(intrusionnum)
                            break
                    except:
                        text3.draw()
                        image1.draw()
                        visual.TextStim(win, text="Please enter a value to indicate frequency from 0-9", pos=(0, -400), color="red", height=35).draw()

                        if(PRACMODE):
                            PRACMODE = visual.TextStim(win, text="PRACMODE", pos=(-800, 0)
                                            ,color="black", font='arial')
                            PRACMODE.draw()
                        win.flip()
        
            break
        #They didnt give y or n answer, prompt and try again
        else:
            visual.TextStim(win, text="Please enter a value of 1 (yes) or 9 (no)", pos=(0, -400), color="red",  height=35).draw()
            text.draw()
            image1.draw()
            text1.draw()
            text2.draw()
            win.flip()
    return correct, rt, intrusionnum

PRACMODE = False

#Need to ask ariel how we want to format input of images so we can stay consistent for both day1 and day2

#give the name of the directory with all of the image directories

mainPath = Path(r"day2")

#List which images are the main images by inputing the main image directory 

mainimgdirs = ["negative", "neutral"]

#List which images are the foil images by inputing the foil image directory names

foilimgdirs = ["negative_foil", "neutral_foil"]

#Where do we want to output results
result_export_dir = "results"

mainpres = []

#How many breaks are in out study
breaks = 1

#Image size presented
imgSize = (600, 600)

#Get participant ID
participant = {"Participant #": ""}
pnum = psygui.DlgFromDict(participant)
partnum = participant['Participant #']

#Get previous presentation details
cur_path = os.path.dirname(__name__)

new_path = os.path.relpath(fr'..\PTSDstudyday1\results\P{partnum}\day1pres', cur_path)
day1pres = pd.read_csv(new_path)



#Normalizes and assigns images with proper identifiers
for imgdir in mainimgdirs:
    dirpath = os.path.join(mainPath, imgdir)
    for imgp in os.listdir(dirpath):
        if imgp != ".DS_Store": #this line filters out the DS_Store file
            img = Image.open(os.path.join(dirpath, imgp))
            img = img.resize(imgSize)
            imgp = os.path.splitext(imgp)[0]
            row =  day1pres.loc[day1pres['name']==imgp][['val', 'pres']].values[0]
            val = row[0]
            pres = row[1]
            mainpres.append([img, 1, imgp, val, pres])

#Same thing but with foil images
for imgdir in foilimgdirs: #TODO 
    dirpath = os.path.join(mainPath, imgdir)
    for imgp in os.listdir(dirpath):
        if imgp != ".DS_Store":
            img = Image.open(os.path.join(dirpath, imgp))
            img = img.resize(imgSize)
            val = imgdir[0:imgdir.index("_")] #TODO: If doesnt work ("negativ") play around with index
            mainpres.append([img, 9, imgp, "NA", "NA"])

#Shuffle for randomness
random.shuffle(mainpres)
#initializes rsults data
df = pd.DataFrame()

#Present instructions
win = visual.Window(fullscr=True, units="pix", color="white")
present_instruction(win, r"Ver2__PTSD_pilot_text\begininstr1.jpg")
present_instruction(win, r"Ver2__PTSD_pilot_text\begininstr2.jpg")

img_count = 0

for img in os.listdir("pracsource"):
    pres_img(win, os.path.join("pracsource", img), 1) #"img" should be replaced with image path, "evil" a placeholder for image valence

present_instruction(win, r"Ver2__PTSD_pilot_text\prac2.jpg") #r ignores slash; replace this with relative path

#Start presenting
for imgpair in mainpres:

    #Checks to see if we present break
    if img_count == int(len(mainpres) / (breaks + 1)) == 0:
        present_instruction(win, r"Ver2__PTSD_pilot_text\break.jpg")
        intcount = 0

    mainimg = imgpair[0]
    imgtype = imgpair[1]

    # Set up the window
    
    correct, rt, intrusionnum = pres_img(win, mainimg, imgtype)

    # Load the images
  
    #Save image response
    df = pd.concat([df, pd.DataFrame({"participant": partnum, "img":imgpair[2], "val":imgpair[3], "pres":imgpair[4], "correct":correct,"rt":rt, "intrusions":intrusionnum
                                      ,"date" : datetime.datetime.now()}, index=[0])], ignore_index=True)

#Save data
ppath = os.path.join(result_export_dir, f"P{partnum}")
print(ppath)

if not os.path.exists(ppath):
    os.mkdir(ppath)

if(not PRACMODE):
    df.to_csv(os.path.join(ppath, "day2"))


# Clean up
win.close()
core.quit()

