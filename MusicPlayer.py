import os
import time
import threading
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from pygame import mixer
from mutagen.mp3 import MP3 as mp3
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk

mixer.init()

# root = Tk()
root = ThemedTk(theme="arc")
root.title("Music Player - [YYScoop.com]")
root.iconbitmap("images/favicon.ico")
root.geometry("620x380")

menubar = Menu(root, bg="#ccba41")
root.config(menu=menubar, bg="#141f30")

# current_music = ""
current_music_path = "sample/Sample Song mp3.mp3"
pause_status = False
stop_status = False
mute_status = False
tread_status = False
reset_tread = False
audio_length = 0.0
time_tread = threading.Thread()
time_counter = "unactive"
playlist_count=1
playlist = []

def browse_file():
    global current_music_path
    global pause_status
    global reset_tread
    global time_counter
    global playlist_count
    global playlist

    current_music_path = filedialog.askopenfilename()
    current_music = os.path.basename(current_music_path)
    playlist_lbox.insert(playlist_count, current_music)
    playlist.insert(playlist_count, current_music_path)
    playlist_count += 1
    pause_status = False

    if time_counter == "active":
        reset_tread = True
    time.sleep(1)
    # play_music()


def aboutus():
    messagebox.showinfo("Music Player - [YYScoop.com]", "This is a Music Player created by the volunteers of YYScoop.com")

def credit():
    messagebox.showinfo("Music Player - [YYScoop.com]","Credit : App Icon made by Freepik from www.flaticon.com")

def play_music():
    global current_music_path
    global pause_status
    global stop_status
    global playlist

    selected_music =  playlist_lbox.curselection()
    current_music_path = playlist[int(selected_music[0])]


    if pause_status== False:

        stop_status = False
        if current_music_path != "":
            mixer.music.load(current_music_path)
            mixer.music.play()
            statusLabel["text"] = "Playing Music" + " - " + os.path.basename(current_music_path)
            dispaly_music()
        else:
            messagebox.showerror("File not found", "No file selected. Please check again")

    elif pause_status == True and stop_status == True:
        stop_status = False
        pause_status = False
        mixer.music.play()
        statusLabel["text"] = "Music restarted"


    else:
        mixer.music.unpause()
        statusLabel["text"] = "Music Resumed"
        stop_status = False
        pause_status = False


def stop_music():
    mixer.music.stop()
    statusLabel["text"] = "Music Stopped"
    global stop_status
    stop_status = True
    global pause_status
    pause_status = False
    global reset_tread
    global time_counter
    if time_counter == "active":
        reset_tread = True
    # reset_tread = True


def pause_music():
    # print(current_music)
    global pause_status
    mixer.music.pause()
    statusLabel["text"] = "Music Paused"
    pause_status = True



def adjust_vol(value):

    value=round(float(value))
    value=str(value)

    value=int(value)
    vol_value = int(value) / 100
    mixer.music.set_volume(vol_value)

def rewind_music():
    global stop_status
    global pause_status
    global reset_tread
    global time_counter
    pause_status = False
    stop_status = False

    if time_counter == "active":
        reset_tread = True
    time.sleep(2)
    play_music()
    statusLabel["text"] = "Music Rewinded"


def mute_music():
    global mute_status

    if mute_status == False:
        # vol_value=0
        volScale.set(0)
        mute_status = True
        # volumeBtn.configure(images=mutephoto)
        volumeBtn["image"] = mutephoto
        statusLabel["text"] = "Music Muted"
    else:
        volScale.set(70)
        mute_status = False
        volumeBtn.configure(image=volumephoto)
        statusLabel["text"] = "Music unMuted"
    # mixer.music.set_volume(vol_value)



def dispaly_music():
    global audio_length
    global time_tread
    musiclabel["text"]="Playing - "+os.path.basename(current_music_path)
    file_ext = os.path.splitext(current_music_path)[1]

    if file_ext == ".wav":
        audio = mixer.Sound(current_music_path)
        audio_length=audio.get_length()
    else:
        audio_metadata = mp3(current_music_path)
        audio_length = audio_metadata.info.length

    s_min,s_sec = divmod(audio_length,60)
    format_length = "{:02d}:{:02d}".format(round(s_min),round(s_sec))
    lengthlabel["text"] = "Total length - "+ format_length

    time_tread = threading.Thread(target=count_duration, args=(audio_length,))
    time_tread.start()


def count_duration(s_time):

    global time_counter
    time_counter = "active"
    global reset_tread

    while s_time != 0:
        if reset_tread == True:
            reset_tread = False
            break

        if pause_status == True:
            continue
        else:
            s_min, s_sec = divmod(s_time, 60)
            format_length = "{:02d}:{:02d}".format(round(s_min), round(s_sec))
            cur_lengthlabel["text"] = "Current length - "+ format_length
            time.sleep(1)
            s_time -= 1

def del_playlist():
    selected_music = playlist_lbox.curselection()
    playlist_lbox.delete(selected_music)
    playlist.pop(selected_music[0])


def on_closing():
    stop_music()
    root.destroy()


## GUI Section -------------------------------------

submenu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="Open", command=browse_file)
submenu1.add_command(label="Exit", command=root.destroy)


submenu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu2)
submenu2.add_command(label="About", command=aboutus)
submenu2.add_command(label="Credit", command=credit)

statusLabel = Label(root, text="Click on [+Add] Song to Play Music", bg="#e3c85b",relief=SUNKEN, anchor=W)
statusLabel.pack(side=BOTTOM, fill=X)


mainFrame = Frame(root, bg="#141f30",highlightbackground="white",highlightthickness=1)
mainFrame.pack(side=LEFT,padx=15)

## Left Frame --------------------------------------

leftFrame = Frame(mainFrame, bg="#141f30")
leftFrame.grid(row=0,column=0,padx=5,pady=5)

## Top Frame (inside Left Frame) -------------------

topFrame = Frame(leftFrame, bg="#141f30")
topFrame.pack(padx=10)

sampleimage_photo = PhotoImage(file="images/sample.png")
sampleimagelabel = Label(topFrame, image=sampleimage_photo,width=100,height=100)
sampleimagelabel.grid(rowspan=3,column=0,padx=5,pady=5,sticky=W+N)

musiclabel = ttk.Label(topFrame, text="Playing - No Music file selected", width=30)
musiclabel.grid(row=0,column=1,padx=5,pady=5)

lengthlabel = ttk.Label(topFrame,text="Total length - --:--")
lengthlabel.grid(row=1,column=1,padx=5,pady=5)


cur_lengthlabel = ttk.Label (topFrame,text="Current length - --:--", relief=GROOVE)
cur_lengthlabel.grid(row=2,column=1,padx=5,pady=5)



## Mid Frame (inside Left Frame) -------------------

midFrame = Frame(leftFrame, bg="#141f30")
midFrame.pack(padx=10, pady=10)

playphoto = PhotoImage(file="images/play64.png")
playBtn = Button(midFrame, image=playphoto, command=play_music, bg="#141f30",borderwidth=0)
playBtn.grid(row=0,column=0,padx=5,pady=5)

stopphoto = PhotoImage(file="images/stop64.png")
stopBtn = Button(midFrame, image=stopphoto, command=stop_music, bg="#141f30",borderwidth=0)
stopBtn.grid(row=0,column=1,padx=5,pady=5)

pausephoto = PhotoImage(file="images/fwd64.png")
pauseBtn = Button(midFrame, image=pausephoto, command=pause_music, bg="#141f30",borderwidth=0)
pauseBtn.grid(row=0,column=2,padx=5,pady=5)

## Bottom Frame (inside Left Frame) -------------------

bottomFrame = Frame(leftFrame, bg="#141f30")
bottomFrame.pack(padx=10, pady=5)

rewindphoto = PhotoImage(file="images/rewind32.png")
rewindBtn = Button(bottomFrame, image=rewindphoto, command=rewind_music, bg="#141f30",borderwidth=0)
rewindBtn.grid(row=0,column=0,padx=5,pady=5)

mutephoto = PhotoImage(file="images/mute32.png")
volumephoto = PhotoImage(file="images/volume32.png")
volumeBtn = Button(bottomFrame, image=volumephoto, command=mute_music, bg="#141f30",borderwidth=0)
volumeBtn.grid(row=0,column=1,padx=5,pady=5)


volScale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=adjust_vol)
default = 70
volScale.set(default)
mixer.music.set_volume(default / 100)
volScale.grid(row=0,column=2,padx=5,pady=5)

## Right Frame ------------------------------------------

rightFrame = Frame(mainFrame, bg="#141f30")
rightFrame.grid(row=0,column=1,padx=5,pady=5)


add= ttk.Label(rightFrame,text="Add Songs to Playlist",font=("Helvetica",15,"bold"))
add.pack()

playlist_lbox = Listbox(rightFrame, bd=1, width=35,height=12)
current_music = os.path.basename(current_music_path)
playlist_lbox.insert(playlist_count, current_music)
playlist.insert(playlist_count, current_music_path)
playlist_lbox.selection_set(0)
playlist_lbox.pack(padx=15,pady=5)

addBtn = ttk.Button(rightFrame, text="+ ADD Song", command=browse_file)
addBtn.pack(side=LEFT,padx=15)

delBtn = ttk.Button(rightFrame, text="- DELETE Song", command=del_playlist)
delBtn.pack()

## -----------------------------------------------------------

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
