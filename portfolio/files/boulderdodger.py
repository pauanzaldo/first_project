import Tkinter
import random
import math
import time
HEIGHT = 500
WIDTH = 800
game = True
root = Tkinter.Tk()
root.wm_title('Boulder Dodger')
canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
#need to do in beginning of each canvas, implements above on to the actual window 
canvas.pack()
#creates shape x1 y1 x2 y2 
obj_id = canvas.create_polygon(4,26,15,0,26,26,fill='red')
obj_id2 = canvas.create_oval(0,0,30,30,outline='red')
SHIP_RADIUS = 15
#text in the center, ship in the center, whatever 
MID_X = WIDTH/2
MID_Y = HEIGHT/2
#moving the object to the bottom 
canvas.move(obj_id, MID_X, 400)
canvas.move(obj_id2, MID_X, 400)
#how far you want the ship to go everytime you press a key
SHIP_SPEED = 10

#function to move the ship
def move_obj(key):
    if key.keysym == 'Left':
        canvas.move(obj_id,-SHIP_SPEED,0)
        canvas.move(obj_id2,-SHIP_SPEED,0)
    elif key.keysym == 'Right':
        canvas.move(obj_id,SHIP_SPEED,0)
        canvas.move(obj_id2,SHIP_SPEED,0)


'''Creating lists for blocks(they will be circles, since it is easier to detect 
collision with circles); essential to keep track of each block
'''
block_id = [] #to identify each one of the blocks
block_radius = []
block_speed = []
#fixed variables for minimum/maximum radius & maximum speed
MIN_BLOCK_RADIUS = 30
MAX_BLOCK_RADIUS = 50
MAX_BLOCK_SPEED = 3

#function to create blocks
def create_block():
    x = random.randint(0, WIDTH)
    y = -100
    r = random.randint(MIN_BLOCK_RADIUS, MAX_BLOCK_RADIUS)
    id1 = canvas.create_oval(x-r, y-r, x+r, y+r, fill='blue') #each object in tkinter needs to be set to an id so we can delete it, otherwise we dont know which one to delete 
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
not being stored in the list and are not on the GUI
'''
def clean_up_blocks():
    for id in range(len(block_id)-1,-1,-1):
        x,y = get_coords(block_id[id])
        if y > HEIGHT+100:
            del_block(id)
        for id in range(len(block_id)-1,-1,-1):
          x,y = get_coords(block_id[id])
          if game == False:
            del_block(id)

#This function will find distance between the ship and the block
def distance(id1,id2):
    # this cal all be done more clearly with a tuple, but won't
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return math.sqrt((x2-x1)**2+(y2-y1)**2)
#detects if actually collides
def collision():
    game = True
    for id in range(len(block_id)-1,-1,-1):
        d = distance(obj_id2, block_id[id])
        b = SHIP_RADIUS + block_radius[id]
        if d < b: #if distance is less than combined radii, then die
            game = False
    return game  #used so that we can call later in main loop
#scores at the top
score_text1 = canvas.create_text(((WIDTH/2)+50),30,text='SCORE',fill='white')
score_text = canvas.create_text(((WIDTH/2)+50),50,fill='white')
#level at the top 
level_text1 = canvas.create_text(((WIDTH/2)-50),30,text='LEVEL',fill='white')
level_text = canvas.create_text(((WIDTH/2)-50),50,fill='white')

#function to show score on screen
def show_score(score):
    canvas.itemconfig(score_text,text=str(score))
    
#function to show level on screen
def show_level(level):
    canvas.itemconfig(level_text,text=str(level))

    
instruction_text = canvas.create_text(MID_X,100,fill='white', font=('Helvetica', 30))
instructions = canvas.create_text(MID_X,175,fill='white', font=('Helvetica', 15))

time_start = 5
time1_text = canvas.create_text(MID_X,MID_Y,fill='white', font=('Helvetica', 100))



#MAIN LOOP
canvas.itemconfig(instruction_text, text='Boulder Dodger Instructions')
canvas.itemconfig(instructions, text='1. You are the red ship.\n2. Control the ship with your right and left keys.\n3. Your goal is to avoid the big blue boulders.\n4. The game gets progressively harder, so Good Luck!')
canvas.update() #calls on the instructions first, waits 5 seconds, and then initializes game
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
while game != False:
    #to make sure not too many blocks are being created
    canvas.bind_all('<Key>',move_obj) #allows key to move 
    if random.randint(0, BLOCK_CHANCE) == 0:
        create_block()
    if collision() == False:
        canvas.delete(score_text, score_text1, level_text, level_text1)
        break
    move_blocks()
    clean_up_blocks()
    show_score(int(score))
    
    #if function for levels
    if int(score) % 150 == 0 and int(score) != 0: # moves to next level 
        level += 1
        show_level(level)
        level_text2 = canvas.create_text(MID_X,MID_Y,fill='white', font=('Helvetica', 30))
        canvas.itemconfig(level_text2, text='Level ' + str(level))
        canvas.update()
        time.sleep(1.00)
        canvas.delete(level_text2)
        BLOCK_CHANCE -= 5
        if BLOCK_CHANCE < 10:
            BLOCK_CHANCE = 10
        score = 0
        
    
    #how score is recorded
    for i in range(10):
        score += 0.01
    
    canvas.update()
    time.sleep(0.01)
    

canvas.create_text(MID_X, MID_Y, text='GAME OVER', fill='white',
        font=('Helvetica', 30))
canvas.create_text(MID_X, MID_Y + 30, text='Level: ' + str(level),
        fill='white')
canvas.create_text(MID_X, MID_Y + 50, text='Score: ' + str(int(score)),
        fill='white')
canvas.create_text(MID_X, MID_Y + 70, text='Total Score: ' + str(int(score) + (150 * (level-1))),
        fill='white')
canvas.delete(score_text, score_text1, level_text, level_text1)


canvas.update()
root.mainloop()