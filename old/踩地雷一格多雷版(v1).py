import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
import time

size_x = 9
size_y = 9
mine_number = 10
unclicked_cell = 0
mine_count = 0

root = tk.Tk()
root.title('Minesweeper MMPC')
root.geometry('390x410')
root.resizable(False, False)
root.iconbitmap('icon.ico')
title_1 = ttk.Label(
    root,
    text='Minesweeper MMPC',
    font=("Arial",15)
    )
title_1.pack(side = "top")

new_width = tk.StringVar()
new_width.set('9')
new_height = tk.StringVar()
new_height.set('9')
new_mine_number = tk.StringVar()
new_mine_number.set('10')

#------------Menubar-----------------------
def easy_setup():
    new_width.set('9')
    new_height.set('9')
    new_mine_number.set('10')
    set_new_grid()

def interm_setup():
    new_width.set('16')
    new_height.set('16')
    new_mine_number.set('40')
    set_new_grid()

def expert_setup():
    new_width.set('30')
    new_height.set('16')
    new_mine_number.set('99')
    set_new_grid()

# create main menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the game menu
game_menu = Menu(menubar, tearoff = False)

# create the help menu
help_menu = Menu(menubar, tearoff = False)

# add "easy" option to Game menu
game_menu.add_command(
    label='Easy',
    command=easy_setup
)

# add "intermediate" option to Game menu
game_menu.add_command(
    label='Intermediate',
    command=interm_setup
)

# add "expert" option to Game menu
game_menu.add_command(
    label='Expert',
    command=expert_setup
)

# add "about" option to Help menu
help_menu.add_command(
    label='About',
    command = lambda: messagebox.showinfo('About', "Creator: Lin Wei-Hsu 2022\n\nA classic Minesweeper replica except that it has up to 10 mines per cell.\n\nAll operations identical to the original Minesweeper.\n\nCycle flag #1~#10 by right-clicking mouse repetitively on same cell.")
)

# add the Game menu to the menubar
menubar.add_cascade(
    label="Game",
    menu=game_menu
)

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)



face_smile = tk.PhotoImage(file='face_smile.png')
face_dead = tk.PhotoImage(file='face_dead.png')
face_glasses = tk.PhotoImage(file='face_glasses.png')

gray_square = ImageTk.PhotoImage(Image.open('gray_square.png').resize((16,16)))   #transparent square as background for cell, to prevent row or column collapse.
flag_1 = ImageTk.PhotoImage(Image.open('flag_1.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_2 = ImageTk.PhotoImage(Image.open('flag_2.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_3 = ImageTk.PhotoImage(Image.open('flag_3.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_4 = ImageTk.PhotoImage(Image.open('flag_4.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_5 = ImageTk.PhotoImage(Image.open('flag_5.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_6 = ImageTk.PhotoImage(Image.open('flag_6.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_7 = ImageTk.PhotoImage(Image.open('flag_7.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_8 = ImageTk.PhotoImage(Image.open('flag_8.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_9 = ImageTk.PhotoImage(Image.open('flag_9.png').resize((16,16)))   #resize the flags from 30x30 to 16x16
flag_10 = ImageTk.PhotoImage(Image.open('flag_10.png').resize((16,16))) #resize the flags from 30x30 to 16x16

mine_image = ImageTk.PhotoImage(Image.open('mine.png').resize((16,16))) #resize mine PNG to 16x16
clicked_mine_image = ImageTk.PhotoImage(Image.open('clicked_mine.png').resize((16,16))) #resize clicked_mine PNG to 16x16

#------------Display Panel-----------------------
display_frame = ttk.Frame(  #display frmae
    root,
    height = 50,
    width = 300,
    borderwidth = 3,
    relief = "sunken",
    )
display_frame.pack(side = "top", padx = 10, pady = 10)
display_frame.grid_propagate(0)

face = tk.Button(   #經典笑臉(中間)
    display_frame,
    borderwidth = 3,
    relief = "raised",
    image = face_smile
    )

def face_func(self):
    face.config(image = face_smile)
    init_all()
    
face.place(x = 127, y = 3)    #tested center position
face.bind("<Button-1>", face_func)

mine_counter = tk.Label(   #地雷計數器(左)
    display_frame,
    borderwidth = 3,
    relief = "sunken",
    text = '010',
    font=("Consolas",18),
    bg = "black",
    fg = "red",
    )
mine_counter.place(x = 5, y = 4) #tested left position

second = 0

timer = tk.Label(   #計時器(右)
    display_frame,
    borderwidth = 3,
    relief = "sunken",
    text = '000',
    font=("Consolas",18),
    bg = "black",
    fg = "red",
    )
timer.place(x = 243, y = 4) #tested right position

def start_timer():       #計時器啟動
    global second
    second = time.time()
    print("start timer ",second)

def stop_timer():        #計時器停止並顯示
    global second
    second = time.time()-second
    print("stop timer ",second)
    if second > 999 and second < 1000000: #really over 999 seconds
        second = 999
    if second > 1000000: #hit a mine on first click, so no start() before stop(), second = time.time()
        second = 0
    timer.config(text = str(round(second)).zfill(3))
    second = 0
    
def reset_timer():       #計時器重置
    global second
    second = 0
    timer.config(text = str(second).zfill(3))

#------------Display Panel-----------------------

main_frame = ttk.Frame(  #主Frame
    root,
    height = 400,
    width = 600,
    borderwidth = 3,
    relief = "sunken"
    )
main_frame.pack()

#------------Control Panel-----------------------
def set_new_grid():
    global cells
    global board_data
    global mine_data
    global flag_data
    global size_x
    global size_y
    global mine_number
    global unclicked_cell
    global new_width
    global new_height
    global new_mine_number

    for i in range(size_y):    #刪除舊陣列
        for j in range(size_x):
            cells[i][j].destroy()
    
    size_x = int(new_width.get())  #get parameter from control panel
    size_y = int(new_height.get())
    mine_number = int(new_mine_number.get())
    if mine_number > size_x*size_y:  #correction for too many mines
        mine_number = size_x*size_y
    if size_x == 0: #correction for impossible size_x
        size_x = 1
    if size_y == 0: #correction for impossible size_y
        size_y = 1

    new_win_w = 390 #determine new window size
    new_win_h = 410

    #window resize for the new grid----------------------
    print("sizex ",size_x)
    print("sizey ",size_y)
    if size_x <= 15:  #default 380x380 window just happens to house a w = 15, h = 9 grid, everything larger than that needs a window resize
        new_win_w = 390
    elif size_x > 15:
        new_win_w = 390+25*(size_x-15) #I tested that for every new row/column, roughly 25 pixels of space is needed
    if size_y <= 9:
        new_win_h = 390  #the 410 declared originally is actually 390, 20 goes to the menubar
    elif size_y > 9:
        new_win_h = 390+25*(size_y-9)
    cmd = str(new_win_w)+"x"+str(new_win_h)
    print(cmd)
    root.geometry(cmd)
    #window resize for the new grid----------------------

    
    cells = [[tk.Label(   #重新宣告cell陣列
    main_frame,
    text = " ",
    width = 16,
    height = 16,
    borderwidth = 3,
    relief = "raised",
    image = gray_square,
    compound='center',
    font=("Arial",10)
    ) for j in range(size_x)] for i in range(size_y)]

    for i in range(size_y):     #place the cells into a grid
    	for j in range(size_x):
    		cells[i][j].grid(column=j, row=i)

    board_data = [[0 for x in range(size_x)] for y in range(size_y)]  #重製資料陣列
    mine_data = [[0 for x in range(size_x)] for y in range(size_y)]  #重製地雷陣列
    flag_data = [[0 for x in range(size_x)] for y in range(size_y)]  #重製旗幟陣列

    init_all()


    

def validate1(P):   #width and height condition: only numbers <99 are allowed
    if len(P) == 0:
        return True
    elif len(P) == 1 and P.isdigit():
        return True
    elif len(P) == 2 and P.isdigit():
        return True
    else:
        return False

def validate2(P):   #mine_number condition: same as validate1 but the number can be three digits long
    if len(P) == 0:
        return True
    elif len(P) <= 3 and P.isdigit():
        return True
    else:
        return False

vcmd1 = (root.register(validate1), '%P')
vcmd2 = (root.register(validate2), '%P')

control_frame = ttk.Frame(  #control frame
    root,
    height = 50,
    width = 320,
    borderwidth = 3,
    relief = "sunken",
    padding = 5
    )
control_frame.pack(side = "bottom", padx = 10, pady = 10)
control_frame.grid_propagate(0)

ctrl_L1 = tk.Label(control_frame,text='Width: ',font=("Arial",11))
ctrl_L1.grid(column=0, row=0)

width_input = tk.Entry(control_frame, width = 2, text = '9', textvariable = new_width, font=("Arial",11), validate='key', validatecommand=vcmd1)
width_input.grid(column=1, row=0)

ctrl_L2 = tk.Label(control_frame,text=' Height: ',font=("Arial",11))
ctrl_L2.grid(column=2, row=0)

height_input = tk.Entry(control_frame, width = 2, text = '9', textvariable = new_height, font=("Arial",11), validate='key', validatecommand=vcmd1)
height_input.grid(column=3, row=0)

ctrl_L3 = tk.Label(control_frame,text=' Mine cell: ',font=("Arial",11))
ctrl_L3.grid(column=4, row=0)

height_input = tk.Entry(control_frame, width = 3, text = '10', textvariable = new_mine_number, font=("Arial",11), validate='key', validatecommand=vcmd2)
height_input.grid(column=5, row=0)

set_button = tk.Button(control_frame,borderwidth = 3,relief = "raised",text = "Set", font=("Arial",11), command = set_new_grid)
set_button.grid(column=6, row=0, padx = 10)

#------------Control Panel-----------------------
def win():
    print("win")
    face.config(image=face_glasses)  #show glasses face
    for i in range(size_y):
        for j in range(size_x):
            cells[i][j].unbind("<Button-1>") #make the cells unclickable
            cells[i][j].unbind("<Button-2>") #make the cells unclickable
            cells[i][j].unbind("<Button-3>") #make the cells unclickable

def rndInt(s,m):
    return random.randint(s,m)

def cell_clicked_left(x,y):
    global unclicked_cell
    global size_x
    global size_y
    global unclicked_cell
    if(x >= 0 and x<= size_x-1 and y >=0 and y<= size_y-1):
        x = x
        y = y
        #print('left click at cell (%s , %s)' % (x,y))
        if board_data[y][x] ==-1:    #中雷
            mine_exploded(x,y)
        elif board_data[y][x] == 0: #自動開相連空白
            cells[y][x].config(relief = "flat")
            cells[y][x].config(text=" ")
            board_data[y][x] = 100 # 100 indicates a 0 that has been opened
            if unclicked_cell == size_x*size_y-mine_number:  # first click, start timer
                start_timer()
            unclicked_cell -= 1
            #print('cells left: ',unclicked_cell)
            if unclicked_cell == 0:
                stop_timer()
                win()
            cell_clicked_left(x-1,y-1)
            cell_clicked_left(x,y-1)
            cell_clicked_left(x+1,y-1)
            cell_clicked_left(x-1,y)
            cell_clicked_left(x+1,y)
            cell_clicked_left(x-1,y+1)
            cell_clicked_left(x,y+1)
            cell_clicked_left(x+1,y+1)
        elif board_data[y][x] <= 80: # a normal unopened, unflagged tile
            cells[y][x].config(text=board_data[y][x])
            cells[y][x].config(relief = "flat")
            board_data[y][x] = 100+board_data[y][x] # num+100 indicates an opened number
            if unclicked_cell == size_x*size_y-mine_number:  # first click, start timer
                start_timer()
            unclicked_cell -= 1
            #print('cells left: ',unclicked_cell)
            if unclicked_cell == 0:
                win()
                stop_timer()
                return 0
    #else:
        #print("autoclear out of bound, nothing is done")

def cell_clicked_right(x,y):
    global mine_count
    #print('right click at cell (%s , %s)' % (x,y))
    print(board_data[y][x])
    if board_data[y][x] <= 80:                                     #any unopened, unflagged cell     +200 indicates it has some sort of flag, and prevents other functions from opening it
        cells[y][x].config(image = flag_1, width = 16, height = 16)
        board_data[y][x] += 200
        flag_data[y][x] += 1
        mine_count -= 1
        mine_counter.config(text = str(mine_count).zfill(3))
    elif board_data[y][x] >= 199:                                  #flagged before, go into cycle now
        if flag_data[y][x] == 1:
            cells[y][x].config(image=flag_2, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 2:
            cells[y][x].config(image=flag_3, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 3:
            cells[y][x].config(image=flag_4, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 4:
            cells[y][x].config(image=flag_5, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 5:
            cells[y][x].config(image=flag_6, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 6:
            cells[y][x].config(image=flag_7, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 7:
            cells[y][x].config(image=flag_8, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 8:
            cells[y][x].config(image=flag_9, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 9:
            cells[y][x].config(image=flag_10, width = 16, height = 16)
            flag_data[y][x] += 1
        elif flag_data[y][x] == 10:
            cells[y][x].config(image = gray_square, width = 16, height = 16) # cycle complete and unflag
            flag_data[y][x] = 0
            board_data[y][x] -= 200
            mine_count += 1
            mine_counter.config(text = str(mine_count).zfill(3))
    
def mine_exploded(x,y):
    global size_x
    global size_y
    print('mine exploded at (%s , %s)' % (x,y))
    face.config(image=face_dead)  #show dead face
    stop_timer()
    for i in range(size_y):
        for j in range(size_x):
            cells[i][j].unbind("<Button-1>") #make the cells unclickable
            cells[i][j].unbind("<Button-2>") #make the cells unclickable
            cells[i][j].unbind("<Button-3>") #make the cells unclickable
            if mine_data[i][j] != 0 and board_data[i][j] < 199: #if there is a mine that has not been flagged yet, show it
                if i == y and j == x:   #this is the clicked mine, so it has red background
                    cells[i][j].config(image=clicked_mine_image, width = 16, height = 16)
                else:
                    cells[i][j].config(image=mine_image, width = 16, height = 16) #other mines
    
    
cells = [[tk.Label(   #建立cell陣列
    main_frame,
    text = " ",
    width = 16,
    height = 16,
    borderwidth = 3,
    relief = "raised",
    image = gray_square,
    compound='center',
    font=("Arial",10)
    ) for j in range(size_x)] for i in range(size_y)]

for i in range(size_y):     #place the cells into a grid
    for j in range(size_x):
        cells[i][j].grid(column=j, row=i)


board_data = [[0 for x in range(size_x)] for y in range(size_y)]  #資料陣列

mine_data = [[0 for x in range(size_x)] for y in range(size_y)]  #地雷陣列

flag_data = [[0 for x in range(size_x)] for y in range(size_y)]  #旗幟陣列

def print_mine_data():     #for debug purposes
    global size_x
    global size_y
    for i in range(size_y):
        for j in range(size_x):
            print(mine_data[i][j], end = '')
            print(" ", end = '')
        print("\n")

def print_board_data():    #for debug purposes
    global size_x
    global size_y
    for i in range(size_y):
        for j in range(size_x):
            print(board_data[i][j], end = '')
            print(" ", end = '')
        print("\n")

def mines_around_me(x,y):     #counts the mine around a non-mine cell
    global size_x
    global size_y
    out = 0
    if(x == 0 or x == size_x-1 or y == 0 or y == size_y-1):    #only edge cells need extra precaution
        if(x-1 >= 0 and y-1 >= 0):       #top left available
            out+=mine_data[y-1][x-1]
        if(y-1 >= 0):                   #top available
            out+=mine_data[y-1][x]
        if(x+1 <= size_x-1 and y-1 >= 0):      #top right available
            out+=mine_data[y-1][x+1]
        if(x-1 >= 0):                   #left available
            out+=mine_data[y][x-1]
        if(x+1 <= size_x-1):                  #right available
            out+=mine_data[y][x+1]
        if(x-1 >= 0 and y+1 <= size_y-1):      #bottom left available
            out+=mine_data[y+1][x-1]
        if(y+1 <= size_y-1):                  #bottom available
            out+=mine_data[y+1][x]
        if(x+1 <= size_x-1 and y+1 <= size_y-1):     #bottom right available
            out+=mine_data[y+1][x+1]

    else:                             #normal cells
        out+=mine_data[y-1][x-1]
        out+=mine_data[y-1][x]
        out+=mine_data[y-1][x+1]
        out+=mine_data[y][x-1]
        out+=mine_data[y][x+1]
        out+=mine_data[y+1][x-1]
        out+=mine_data[y+1][x]
        out+=mine_data[y+1][x+1]
        
    return out

def init_all():     
    global size_x
    global size_y
    global mine_number
    global mine_count
    global unclicked_cell      

    for i in range(size_y):     #enable clicking of labels
        for j in range(size_x):
            cells[i][j].bind("<Button-1>", lambda event, i = i, j = j: cell_clicked_left(j,i))   #綁定左鍵
            cells[i][j].bind("<Button-2>", lambda event, i = i, j = j: cell_clicked_right(j,i))  #綁定右鍵(對應不同系統)
            cells[i][j].bind("<Button-3>", lambda event, i = i, j = j: cell_clicked_right(j,i))  #綁定右鍵(對應不同系統)
            cells[i][j].config(image = gray_square, width = 16, height = 16, text = " ", relief = "raised", borderwidth = 3)      #reset all attributes
    
    for i in range(size_y):
        for j in range(size_x):
            mine_data[i][j] = 0
            flag_data[i][j] = 0

    for i in range(mine_number): #(mine_number) mines(s) placed into the grid
        x = rndInt(0,size_x-1)
        y = rndInt(0,size_y-1)
        while mine_data[y][x] != 0: #make sure no cells is visited two times
            x = rndInt(0,size_x-1)
            y = rndInt(0,size_y-1)
        mine_data[y][x] = rndInt(1,10)

    for i in range(size_y):
        for j in range(size_x):
            if mine_data[i][j] == 0:
                board_data[i][j] = mines_around_me(j,i)
            else:
                board_data[i][j] = -1 # -1 indicates mine
                
    unclicked_cell = size_x*size_y-mine_number

    mine_count = mine_number
    
    mine_counter.config(text = str(mine_count).zfill(3))  #set mine counter

    reset_timer()
            

##------------------------------------------------------------------------------

unclicked_cell= 0  #count how many cells left needed to be open

init_all()

#print_mine_data()

#print("\n\n\n")

#print_board_data()

root.mainloop()
