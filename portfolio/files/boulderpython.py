'''
*************************************
Project: Boulder Dodger
Name: Paulina Anzaldo and Ramakrishna Senthil
Category: Game
Description: Avoid the obstacles as long as you can
*************************************
'''


#importing necessary libraries
import Tkinter
import random
import math
import time
HEIGHT = 500
WIDTH = 800
root = Tkinter.Tk()
root.wm_title('Boulder Dodger')
canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')

#this function must be called in beginning of each program using Tkinter, implements above on to the actual window of the player
canvas.pack()

#creates shape of the player's arrow with coorsinates x1, y1, x2, y2 
obj_id = canvas.create_polygon(4,26,15,0,26,26,fill='red3')
obj_id2 = canvas.create_oval(0,0,30,30,outline='red3') #circle needed on outside to detect collision
SHIP_RADIUS = 15

#allows to put text in the center, ship in the center, whatever object we want in the middle 
MID_X = WIDTH/2
MID_Y = HEIGHT/2

#Setting the object (player's arrow) to the bottom of the screen
canvas.move(obj_id, MID_X, 400)
canvas.move(obj_id2, MID_X, 400)

#sets the speed of how far you want the ship to go everytime you press a key
SHIP_SPEED = 10

#function to move the ship left and right 
def move_obj(key):
    position = canvas.coords(obj_id2)
    x = (position[0] + position[2]) / 2
    if x > 790:    #used to make sure that the user does not go over the border limit 
        canvas.move(obj_id,-790,0)
        canvas.move(obj_id2,-790,0) 
    elif x < 10:
        canvas.move(obj_id,790,0)
        canvas.move(obj_id2,790,0)        
    if key.keysym == 'Left':
        canvas.move(obj_id,-SHIP_SPEED,0)
        canvas.move(obj_id2,-SHIP_SPEED,0)
    elif key.keysym == 'Right':
        canvas.move(obj_id,SHIP_SPEED,0)
        canvas.move(obj_id2,SHIP_SPEED,0)

#function to create blocks (obstacles); circles since you can detect collision easier
def create_block():
    x = random.randint(0, WIDTH)
    y = random.randint(-200,-100)
    r = random.randint(MIN_BLOCK_RADIUS, MAX_BLOCK_RADIUS)
    id1 = canvas.create_oval(x-r, y-r, x+r, y+r, fill='blue4') #each object in tkinter needs to be set to an id so we can delete it
    block_id.append(id1)
    block_radius.append(r)
    block_speed.append(random.randint(1, MAX_BLOCK_SPEED))

#function to move blocks
def move_blocks():
    for i in range(len(block_id)): #how many blocks there are 
        canvas.move(block_id[i], 0, block_speed[i]) #only moving in y direction

#function to get coodinates of the blocks, so that we can detect collision
def get_coords(id):
    pos = canvas.coords(id)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y
    


#function to delete blocks
def del_block(id):
    del block_radius[id]
    del block_speed[id]    
    canvas.delete(block_id[id])
    del block_id[id]

'''function to delete the blocks once they are off the screen, so that they are
not being stored in the list and are not on the GUI. This allows the game to be 
as fast as possible.
'''
def clean_up_blocks():
    for id in range(len(block_id)-1,-1,-1):
        x,y = get_coords(block_id[id])
        if y > HEIGHT+100:
            del_block(id)
        for id in range(len(block_id)-1,-1,-1):
          if game == False:
            del_block(id)
            time.sleep(0.01)

#This function will find distance between the ship and the block
def distance(id1,id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return math.sqrt((x2-x1)**2+(y2-y1)**2)# distance formula

#detects if actually collides, so that we can determine whether the game is over
def collision(num_of_lives):
    game = True
    for id in range(len(block_id)-1,-1,-1): #reads list backwards, so it crashes less
        if num_of_lives < 1: #When the number of lives is less than 1, then that means the game is over
            game = False
        else:
            d = distance(obj_id2, block_id[id-1])
            r = SHIP_RADIUS + block_radius[id-1]
            if d < r: #if distance is less than combined radii, then subtract one life.
                num_of_lives -= 1
                lives_text2 = canvas.create_text(MID_X,MID_Y,fill='white', font=('Helvetica', 30))
                if num_of_lives > 0:
                    canvas.itemconfig(lives_text2, text='LIVES LEFT: ' + str(num_of_lives))
                else:
                    canvas.itemconfig(lives_text2, text='YOU LOST')
                canvas.update()
                for item in range(len(block_id)-1, -1, -1):
                    time.sleep(0.01)
                    del_block(item) #deletes all blocks from the screen
                time.sleep(1.00)
                canvas.delete(lives_text2)
                for i in range(10):
                    create_block()
                
    return game,num_of_lives #used so that we can call later in main loop 

#function to show score on screen
def show_score(score):
    canvas.itemconfig(score_text,text=str(score))
    
#function to show level on screen
def show_level(level):
    canvas.itemconfig(level_text,text=str(level))

def show_lives(lives):
    canvas.itemconfig(lives_text, text=str(lives))



'''
******************
MAIN
******************
'''


#font style for instructions     
instruction_text = canvas.create_text(MID_X,100,fill='white', font=('Helvetica', 30))
instructions = canvas.create_text(MID_X,175,fill='white', font=('Helvetica', 15))
#countdown to start game, beings counting down at 5 seconds
time_start = 5
time1_text = canvas.create_text(MID_X,MID_Y,fill='white', font=('Helvetica', 100))

#scores at the top
score_text1 = canvas.create_text(((WIDTH/2)+50),30,text='SCORE',fill='white')
score_text = canvas.create_text(((WIDTH/2)+50),50,fill='white')
#level at the top 
level_text1 = canvas.create_text(((WIDTH/2)),30,text='LEVEL',fill='white')
level_text = canvas.create_text(((WIDTH/2)),50,fill='white')
#lives at the top
lives_text1 = canvas.create_text(((WIDTH/2)-50),30,text='LIVES',fill='white')
lives_text = canvas.create_text(((WIDTH/2)-50),50,fill='white')




#Creating lists for blocks; essential to keep track of each block

block_id = [] #We put each one of the blocks in an empty list so we can identify them individually if there is a collision
block_radius = []
block_speed = []

#fixed variables for minimum/maximum radius & maximum speed
MIN_BLOCK_RADIUS = 30
MAX_BLOCK_RADIUS = 50
MAX_BLOCK_SPEED = 1




#sets value of game to True. When game is False, it is lost
game = True
#sets number of lives to 3 
num_of_lives = 3

root.attributes("-topmost", True) # brings window to the front
canvas.itemconfig(instruction_text, text='Boulder Dodger Instructions') #main  text, sets instructions for the game 
canvas.itemconfig(instructions, text='\n1. You are the red ship.\n2. Control the ship with your right and left keys.\n3. Your goal is to avoid the big blue boulders.\n4. You have 3 lives to start with.\n5. The game gets progressively harder, so Good Luck!')
canvas.update() #shows the instructions first, waits 5 seconds, and then starts game
time.sleep(5.00)
canvas.delete(instruction_text, instructions)
canvas.update()
for time1 in range(5):
    canvas.itemconfig(time1_text, text=str(time_start))
    canvas.update()
    time.sleep(1.00)
    time_start -= 1
canvas.itemconfig(time1_text, text='Start!')
canvas.update()
time.sleep(1.00)
canvas.delete(time1_text)
canvas.update()
# 1 in 50 chances of creating a block at the beginning of the game
BLOCK_CHANCE = 50
score = 0


level = 1
show_level(level)



#MAIN GAME LOOP
while game != False:
    #to make sure not too many blocks are being created
    canvas.bind_all('<Key>',move_obj) #allows key to move 
    if random.randint(0, BLOCK_CHANCE) == 0: #game starts off with 1 in 50 chance
        create_block()
    game, num_of_lives = collision(num_of_lives)
    if game == False:
        canvas.delete(score_text, score_text1, level_text, level_text1)
        break
    move_blocks()
    clean_up_blocks()
    show_score(int(score))
    show_lives(num_of_lives)
    
    #Records levels
    if int(score) % 150 == 0 and int(score) != 0: # moves to next level 
        level += 1
        show_level(level)
        level_text2 = canvas.create_text(MID_X,MID_Y,fill='white', font=('Helvetica', 30))
        canvas.itemconfig(level_text2, text='LEVEL ' + str(level))
        canvas.update()        
        for item in range(len(block_id)-1, -1, -1):
                    time.sleep(0.01)
                    del_block(item) #deletes all blocks from the screen
        time.sleep(1.00)
        for i in range(10):
                    create_block()
        canvas.delete(level_text2)
        BLOCK_CHANCE -= 5 #as the denominator gets smaller, the chance of creating a block should get larger, making more blocks
        if BLOCK_CHANCE < 10: #to make sure that the chance of creating a block does not get larger than 10%
            BLOCK_CHANCE = 10
        score = 0
        MAX_BLOCK_SPEED += 1
        if MAX_BLOCK_SPEED > 7:
            MAX_BLOCK_SPEED = 7
        
    
    #how score is recorded
    for i in range(10):
        score += 0.01
    
    canvas.update()
    time.sleep(0.01)
    
#game over text 
canvas.create_text(MID_X, MID_Y, text='GAME OVER', fill='white',
        font=('Helvetica', 30))
canvas.create_text(MID_X, MID_Y + 30, text='Level: ' + str(level),
        fill='white')
canvas.create_text(MID_X, MID_Y + 50, text='Score: ' + str(int(score)),
        fill='white')
canvas.create_text(MID_X, MID_Y + 70, text='Total Score: ' + str(int(score) + (150 * (level-1))),
        fill='white')
canvas.delete(score_text, score_text1, level_text, level_text1, lives_text, lives_text1)


canvas.update()
root.mainloop()