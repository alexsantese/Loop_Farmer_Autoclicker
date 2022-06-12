import time
import keyboard
from directKeys import click
from PIL import ImageGrab
import numpy as np
from pyautogui import position, mouseDown, mouseUp, moveTo



green = (0, 199, 0) # upgrade is available color

middle = (856, 655) # where to click if not doing anything else

talents = (1490, 640) # values used to upgrade talents, including opening the menu, upgrading, and closing the menu again
talent_upgrade = (1435, 900)
x_button = (1685, 307)

upgrades = [1441, 400, 1693, 523] # location of the upgrades box on screen

talent_counter = 0 # counters used to determine if we need to upgrade talents
reset_counter = 0 # after we upgrade the talents 5 times, we'll reset the game and start from the beginning

prestige = [1554, 812]
reset_button = [1044, 897]


def talent_up(): # this function is called when we need to upgrade our talents, for now we'll only upgrade the power of our clicks
    
    global talent_counter, reset_counter
    
    click(*talents)
    time.sleep(2)
    for i in range(20):
        click(*talent_upgrade)
        time.sleep(0.5)
    
    moveTo(*x_button)
    mouseDown()
    time.sleep(0.5)
    mouseUp()
    
    talent_counter = 0
    reset_counter += 1
    
def reset(): # when called, this function will reset the game with our new bonuses
    
    global reset_counter
    
    click(*prestige)
    time.sleep(1)
    moveTo(*reset_button)
    mouseDown()
    time.sleep(5)
    mouseUp()


def main(): # main fucntion which clicks on the middle button and upgrades our skills
    
    global talent_counter, reset_counter
    start_time = time.time()
    
    upgrade = False
    
    if reset_counter >= 3:
        reset()
        time.sleep(3)
        reset_counter = 0
    
    if talent_counter > 10**5:
        talent_up()
        time.sleep(3)
        reset_counter += 1

        
    img = np.array(ImageGrab.grab(bbox=upgrades)) # PIL grabs a screenshot of the upgrade box and turns it into a numpy array which we can then loop through to look for green pixels
    
 
    for y in range(0, len(img), 25):
        for x in range(0, len(img[y]), 25):
            if img[y][x][1] == 199: # if we find any green pixels that match the upgrade color we'll get their xy coordinates and click on them.
                upgrade = True
                while upgrade:
                    actual_x = x + upgrades[0]
                    actual_y = y + upgrades[1]
                    click(actual_x, actual_y)
                    upgrade = False
            else: # if there are no upgrades available we'll click on the middle button
                click(*middle)
                talent_counter += 1

    end_time = time.time()
    
    print(f"loop time = {end_time - start_time}", end='||', flush=True)
    print(f"talent counter: {talent_counter}", end='||', flush=True)
    print(f"reset counter: {reset_counter}", end='\r', flush=True)
    
    
    
while True:

    if keyboard.is_pressed('q'): # we can press 'q' at any time to break out of our loop and end the program
        break

    main()
    #talent_up()
    #reset()
    # print(position())
    # time.sleep(1)