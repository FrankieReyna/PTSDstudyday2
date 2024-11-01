#Basically just want it to take 2 images from foil and real. The two options will be randomly placed on the screen (Migh have to make foil)

#Must check that foil # is matched with main #

#Ask andrea and Ariel if we need photo transformations for this? Prob not as we want to show main image

    #Particiapnt able to interact, and choose one of the images that they remember seeing 

        #Partipant Answers Correclty! Yippee

            #participant#, correct, mainImgName, mainImgPath, foilImgName, foilImgPath

        #Partipant Answers incorreclty! GRRRR >:()

            #participant, correct, mainImgName, mainImgPath, foilImgName, foilImgPath

    #repeat above until all images are ran though

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

PRACMODE = False

mainPath = Path(r"PracSource")
foilPath = Path(r"PracFoil")

result_export_dir = "results"

mainpres = []

breaks = 1

imgSize = (300, 300)

for imgp in os.listdir(mainPath):
    img = Image.open(os.path.join(mainPath, imgp))
    img = img.resize(imgSize)
    mainpres.append([img, 1, imgp])

for imgp in os.listdir(foilPath):
    img = Image.open(os.path.join(foilPath, imgp))
    img = img.resize(imgSize)
    mainpres.append([img, 9, imgp])

random.shuffle(mainpres)

df = pd.DataFrame()

correct = False

c = Clock()

participant = {"Participant #": ""}
pnum = psygui.DlgFromDict(participant)
partnum = participant['Participant #']


win = visual.Window(fullscr=True, units="pix", color="white")
present_instruction(win, r"Ver2__PTSD_pilot_text\begininstr1.jpg")
present_instruction(win, r"Ver2__PTSD_pilot_text\begininstr2.jpg")

img_count = 0

for imgpair in mainpres:

    if img_count == len(mainpres) / (breaks + 1):
        present_instruction(win, r"Ver2__PTSD_pilot_text\break.jpg")

    mainimg = imgpair[0]
    imgtype = imgpair[1]

    # Set up the window
    

    # Load the images
    text = visual.TextStim(win, "Have you been presented this image before?", pos=(0, 400), color="black", font='arial')
    image1 = visual.ImageStim(win, image=mainimg, pos=(0, 0))
    text1 = visual.TextStim(win, "Yes (1)", pos=(-400, -400), color="black", font='arial')
    text2 = visual.TextStim(win, "No (9)", pos=(400, -400), color="black", font='arial')

    text.draw()
    image1.draw()
    text1.draw()
    text2.draw()
    win.flip()

    # Wait for user response
    c.reset()
    
    while True:

        intrusionnum = "0"
        endt = c.getTime()
        keys = event.waitKeys()[0]
        
        rt = c.getTime()

        if 'escape' in keys or 'close' in keys:
            core.quit()

        if keys == '1' or keys == '9':  # User chooses the first image
            correct = f"{imgtype}" == keys[0]
            if keys == '1':

                text3 = visual.TextStim(win, "How many times have you thought about the image presented? (0 to 9)", pos=(0, 400), color="black", font='arial')
                text3.draw()
                image1.draw()
                win.flip()

                while True:

                    intrusionnum = event.waitKeys()[0]

                    if 'escape' in intrusionnum or 'close' in intrusionnum:
                        core.quit()
                            
                    try:
                        if int(intrusionnum) in range(1, 10):
                            intrusionnum = int(intrusionnum)
                            break
                    except:
                        text3.draw()
                        image1.draw()
                        visual.TextStim(win, text="Please enter a value from 0-9", pos=(0, -400), color="red").draw()

                        if(PRACMODE):
                            PRACMODE = visual.TextStim(win, text="PRACMODE", pos=(-800, 0)
                                            ,color="black", font='arial')
                            PRACMODE.draw()
                        win.flip()
        
            break
        else:
            visual.TextStim(win, text="Please enter a value of 1 (yes) or 9 (no)", pos=(0, -500), color="red").draw()
            text.draw()
            image1.draw()
            text1.draw()
            text2.draw()
            win.flip()
            
    df = pd.concat([df, pd.DataFrame({"participant": partnum, "img":imgpair[2], "resp":keys, "correct":correct,"rt":rt, "intrusions":intrusionnum
                                      ,"date" : datetime.datetime.now()}, index=[0])], ignore_index=True)

ppath = os.path.join(result_export_dir, f"P{partnum}")
print(ppath)

if not os.path.exists(ppath):
    os.mkdir(ppath)

if(not PRACMODE):
    df.to_csv(os.path.join(ppath, "day2"))


# Clean up
win.close()
core.quit()



