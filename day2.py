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
import shutil
import random
import numpy as np

mainPath = Path(r"PracSource")
foilPath = Path(r"PracFoil")

mainpres = []

imgSize = (300, 300)

for imgp in os.listdir(mainPath):
    img = Image.open(os.path.join(mainPath, imgp))
    img = img.resize(imgSize)
    mainpres.append([img, 1])

for imgp in os.listdir(foilPath):
    img = Image.open(os.path.join(foilPath, imgp))
    img = img.resize(imgSize)
    mainpres.append([img, 9])

random.shuffle(mainpres)

for imgpair in mainpres:

    mainimg = imgpair[0]
    print(mainimg)
    imgtype = imgpair[1]

    # Set up the window
    win = visual.Window(size=(800, 600), color=(1, 1, 1))

    # Load the images
    image1 = visual.ImageStim(win, image=mainimg, pos=(0, 0))
    text1 = visual.TextStim(win, "Yes (1)", pos=(-0.5, -0.75), color="black", font='arial')
    text2 = visual.TextStim(win, "No (9)", pos=(0.5, -0.75), color="black", font='arial')

    image1.draw()
    text1.draw()
    text2.draw()
    win.flip()

    # Wait for user response
    need_image = True
    while need_image:
        keys = event.waitKeys()
        if '1' or '9' in keys:  # User chooses the first image
            need_image = False
            correct = f"{imgtype}" == keys[0]

    print(correct)

            
# Clean up
win.close()
core.quit()



