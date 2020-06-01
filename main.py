import os
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from pygame import mixer

mixer.init()

root = Tk()
root.title("Music Player - [YYScoop.com]")
root.iconbitmap("downloads/favicon.ico")
root.geometry("350x250")

menubar = Menu(root, bg="#ccba41")
root.config(menu=menubar, bg="#141f30")

current_music = "downloads/dj.mp3"
pause_status = False
stop_status = False
mute_status = False

def browse_file():
    global current_music
    global pause_status

    current_music = filedialog.askopenfilename()
    # print(current_music)
    pause_status = False
    play_music()


def aboutus():
    messagebox.showinfo("Music Player - [YYScoop.com]", "This is a Music Player created by the volunteers of YYScoop.com")


def play_music():
    global current_music
    global pause_status
    global stop_status

    if pause_status== False:

        stop_status = False
        if current_music != " ":
            mixer.music.load(current_music)
            mixer.music.play()
            statusLabel["text"] = "Playing Music" + " - " + os.path.basename(current_music)
        else:
            messagebox.showerror("File not found", "No file selected. Please check again")

    elif pause_status == True and stop_status == True:
        mixer.music.play()
        statusLabel["text"] = "Music restarted"
        stop_status = False

    else:
        mixer.music.unpause()
        statusLabel["text"] = "Music Resumed"
        pause_status == False


def stop_music():
    mixer.music.stop()
    statusLabel["text"] = "Music Stopped"
    global stop_status
    stop_status = True
    global pause_status
    pause_status = False


def pause_music():
    print(current_music)
    global pause_status
    mixer.music.pause()
    statusLabel["text"] = "Music Paused"
    pause_status = True


def adjust_vol(value):
    vol_value = int(value) / 100
    mixer.music.set_volume(vol_value)

def rewind_music():
    global stop_status
    stop_status = False
    global pause_status
    pause_status = False
    play_music()
    statusLabel["text"] = "Music Rewinded"



def mute_music():
    global mute_status

    if mute_status == False:
        # vol_value=0
        volScale.set(0)
        mute_status = True
        # volumeBtn.configure(image=mutephoto)
        volumeBtn["image"] = mutephoto
        statusLabel["text"] = "Music Muted"
    else:
        volScale.set(70)
        mute_status = False
        volumeBtn.configure(image=volumephoto)
        statusLabel["text"] = "Music unMuted"
    # mixer.music.set_volume(vol_value)


## GUI Section -------------------------------------

submenu1 = Menu(menubar, tearoff=0,bg="#de841d")
menubar.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="Open", command=browse_file)
submenu1.add_command(label="Exit", command=root.destroy)


submenu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu2)
submenu2.add_command(label="About", command=aboutus)


label = Label(root, text="Lets rock")
label.pack(padx=10,pady=10)

midFrame = Frame(root)
midFrame.pack(padx=10)

playphoto = PhotoImage(file="downloads/play64.png")
playBtn = Button(midFrame, image=playphoto, command=play_music)
playBtn.grid(row=0,column=0,padx=5,pady=5)

stopphoto = PhotoImage(file="downloads/stop64.png")
stopBtn = Button(midFrame, image=stopphoto,bg="#446496", command=stop_music)
stopBtn.grid(row=0,column=1,padx=5,pady=5)

pausephoto = PhotoImage(file="downloads/fwd64.png")
pauseBtn = Button(midFrame, image=pausephoto, command=pause_music)
pauseBtn.grid(row=0,column=2,padx=5,pady=5)

othFrame = Frame(root)
othFrame.pack(padx=10, pady=15)

rewindphoto = PhotoImage(file="downloads/fwd32.png")
rewindBtn = Button(othFrame, image=rewindphoto, command=rewind_music)
rewindBtn.grid(row=0,column=0,padx=5,pady=5)

mutephoto = PhotoImage(file="downloads/mute32.png")
volumephoto = PhotoImage(file="downloads/volume32.png")
volumeBtn = Button(othFrame, image=volumephoto, command=mute_music)
volumeBtn.grid(row=0,column=1,padx=40,pady=5)


volScale = Scale(othFrame, from_=0, to=100, orient=HORIZONTAL, command=adjust_vol)
default = 70
volScale.set(default)
mixer.music.set_volume(default / 100)
volScale.grid(row=0,column=2,padx=5,pady=5)
# volScale.pack(padx=10,pady=10)


statusLabel = Label(root, text="Welcome to YY Music Player", bg="#e3c85b",relief=SUNKEN, anchor=W)
statusLabel.pack(side=BOTTOM, fill=X)

root.mainloop()
