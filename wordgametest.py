import tkinter
from gc import disable
from tkinter import messagebox
import random
import nltk
import os
import mysql.connector
from nltk.corpus import wordnet
import subprocess

def rd():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="annire712S",
        database="wordfile"
    )
    mycursor=mydb.cursor()
    mycursor.execute("select word from words")
    words = mycursor.fetchall()
    rd1 = random.randint(0, len(words)-1)
    rdword=words[rd1][0]
    return rdword




# Ensure you have WordNet data
nltk.download('wordnet')

def reset():
    wordentry.delete(0, tkinter.END)

def restartgame():
    frame2.quit()
    result = subprocess.run(['python', 'wordgametest.py'], check=True, text=True, capture_output=True)

def on_key_pressed(event):
    press=event.keysym
    if press=='Return':
        reset()

def erase():
    frame2.destroy()
    frame2.quit()


rdword = rd()
g = 5
z=2
def wordcheck1(event=None):
    global g,z
    ans = a = b = 0
    c=d=''
    g1 = []
    startgame.config(state="disabled")
    word1=wordentry.get().lower()
    attempts_label.config(text=f"You have {g} attempts left.")
    if word1 != '' and len(word1) == 4 and word1.isalpha():
        if wordnet.synsets(word1):
            g1=word1
            for i in range(4):
                if g1[i] == rdword[i]:
                    a += 1
            for i in range(4):
                if g1[i] in rdword and g1[i] != rdword[i]:
                    b += 1

            c = str(b) + 'COW'
            d = str(a) + 'BULL'
            status_label.config(text="Valid word", fg="green")
            enteredword = tkinter.Label(frame2, text=word1.capitalize()+' '+c+' '+d)
            enteredword.grid(row=z, column=0)
            z+=1
            g -= 1
            window.bind("<Key>", on_key_pressed)

            if g > 0 :
                attempts_label.config(text=f"You have {g} attempts left.")
                if g1==rdword:
                    attempts_label.config(text='Game Over')
                    status_label.config(text="Congrats! You've won the game. The word is "+str(g1.upper()))
                    wordentry.config(state="disabled")
            else:
                attempts_label.config(text='Game Over')
                status_label.config(text="Sorry, Game Over")
                status_label.config(text="You've run out of attempts.The word is " + rdword.upper())
                wordentry.config(state="disabled")  # Disable input if no attempts left
        else:
            # Show a message if the input is invalid
            status_label.config(text="Invalid word. Please enter a valid 4-letter word.", fg="red")
            if g > 0:
                attempts_label.config(text=f"You have {g} attempts left.")
            else:
                attempts_label.config(text="No attempts left.")
                wordentry.config(state="disabled")
    else:
        status_label.config(text="Invalid input. Please enter a valid 4-letter word.", fg="red")

window=tkinter.Tk()
window.title('WORD GAME')# creating the window for the game

frame=tkinter.Frame(window) # creating the base frame
frame.grid()

frame1=tkinter.LabelFrame(frame)# creating frame1 in frame
frame1.grid(row=0,column=0)

#Creating the title and rules in frame1
Titlelabel=tkinter.Label(frame1,text='Welcome to the Word Game ***COW***BULL***"')
Titlelabel.grid(row=0,column=0)

Rulelabel=tkinter.Label(frame1,text="******RULES of the GAME******\n"
                                  "The game is played in turns by two opponents who aim to decipher the other's \n"
                                  "secret code by trial and error.One Player thinks of a four letter word and the \n"
                                  "other player tries to figure out the word by guessing any valid four letter word.\n"
                                  "The host responds with the number of cows and bulls for each guessed word. As with\n"
                                  "the digit version, 'cow' means a letter in the wrong position and 'bull' means a letter \n"
                                  "in the right position. For example, if the secret word is HEAT, a guess of COIN would \n"
                                  "result in '0 bulls, 0 cows'. Here the host who thinks of a four letter word is this PC,\n"
                                  "you can guess. You are given 5 Chances ", font=("times", 12),bg='bisque2',justify='center')
Rulelabel.grid(row=1,column=0)

def back_to_main_frame(frame2):
    frame2.grid(row=1, column=0, sticky='we')
    frame3.grid(row=5,column=0)
    resetbutton.grid(pady=10)
    Exitbutton.grid(pady=10)


#Creating a startgame button in frame1
#the method back_to_main_frame will make the frame2 appear when the button is clicked
startgame=tkinter.Button(frame1,text='Start Game',command=lambda: back_to_main_frame(frame2))
startgame.grid(row=2,columnspan=2)

#Creating frame2 in frame
frame2 = tkinter.LabelFrame(frame)
frame2.grid(row=1, column=0, sticky='we')
frame2.grid_forget()

#the method grid_forget() is used to remove a widget from the grid layout without actually destroying the widget. This method
#makes the widget disappear but retains its configuration, so it can be redisplayed later using the same grid configuration.

wordlabel = tkinter.Label(frame2, text='Enter a four letter word ')
wordlabel.grid(row=1, column=0)
#wordentry is the entry widget for the four letter word
wordentry = tkinter.Entry(frame2)
wordentry.grid(row=1, column=1)
wordentry.focus_set()
#bind an event to the wordentry widget. Specifically, it binds the KeyRelease event (when the user releases a key after
# pressing it) to the function wordcheck1.
wordentry.bind("<KeyRelease>",wordcheck1)

# Create a label to display the status of the input (valid/invalid)
status_label = tkinter.Label(frame2, text="", font=("Arial", 12))
status_label.grid(row=3, column=1, padx=10)

# Create a label to show the number of remaining attempts
attempts_label = tkinter.Label(frame2, text='', font=("Arial", 12))
attempts_label.grid(row=4, column=1, padx=10,pady=10)

frame3 = tkinter.LabelFrame(frame)
frame3.grid(row=2, column=0, sticky='we')
frame3.grid_forget()

resetbutton=tkinter.Button(frame3,text='Reset',command=reset)
resetbutton.grid(row=0, column=0, padx=10,pady=10)
#resetbutton.grid_forget()

Exitbutton=tkinter.Button(frame3,text='Exit',command=erase)
Exitbutton.grid(row=0, column=2, padx=10,pady=10)

restart=tkinter.Button(frame3,text='Restart',command=restartgame)
restart.grid(row=0, column=4, padx=10,pady=10)
#Exitbutton.grid_forget()

window.mainloop()
