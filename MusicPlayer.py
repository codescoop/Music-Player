import os
import time
import threading
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from pygame import mixer
from mutagen.mp3 import MP3 as mp3

mixer.init()

root = Tk()
root.title("Music Player - [YYScoop.com]")
root.iconbitmap("downloads/favicon.ico")
root.geometry("500x400")

menubar = Menu(root, bg="#ccba41")
root.config(menu=menubar, bg="#141f30")

# current_music = ""
current_music_path = "downloads/dj.mp3"
pause_status = False
stop_status = False
mute_status = False
tread_status = False
reset_tread = False
audio_length = 0.0
time_tread = threading.Thread()
time_counter = "unactive"
playlist_count=0
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
            print("1111111111111111111111")
            mixer.music.load(current_music_path)
            mixer.music.play()
            statusLabel["text"] = "Playing Music" + " - " + os.path.basename(current_music_path)
            dispaly_music()
        else:
            messagebox.showerror("File not found", "No file selected. Please check again")

    elif pause_status == True and stop_status == True:
        print("2222222222222222222")
        stop_status = False
        pause_status = False
        mixer.music.play()
        statusLabel["text"] = "Music restarted"


    else:
        print("33333333333333333")
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
    vol_value = int(value) / 100
    mixer.music.set_volume(vol_value)

def rewind_music():
    global stop_status
    global pause_status
    global reset_tread
    global time_counter
    pause_status = False
    stop_status = False
    # print("rewind",reset_tread)
    if time_counter == "active":
        reset_tread = True
    # reset_tread = True
    time.sleep(2)
    # print(reset_tread)
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
    # start_tread()
    # print("leaving dispaly")


def count_duration(s_time):
    global time_counter
    time_counter = "active"

    # time.sleep(2)
    print("entered count_duration")
    original_t = s_time
    # print(original_t)
    global reset_tread
    print("Tread Status",reset_tread)
    while s_time:
        # print("in while")
        if reset_tread == True:
            reset_tread = False
            print("killed tread & reset_tread to FALSE \n")
            break

        if pause_status == True:
            print("in continue")
            continue
        else:
            print("entered else ")
            s_min, s_sec = divmod(s_time, 60)
            format_length = "{:02d}:{:02d}".format(round(s_min), round(s_sec))
            cur_lengthlabel["text"] = "Current length - "+ format_length
            time.sleep(1)
            s_time -= 1
            # print("exit entered ")
    print("exit count_duration \n")
    # time_counter = "unactive"

def del_playlist():
    print(playlist)
    selected_music = playlist_lbox.curselection()
    playlist_lbox.delete(selected_music)
    playlist.pop(selected_music[0])
    print(playlist)

def on_closing():
    stop_music()
    root.destroy()


## GUI Section -------------------------------------

submenu1 = Menu(menubar, tearoff=0,bg="#de841d")
menubar.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="Open", command=browse_file)
submenu1.add_command(label="Exit", command=root.destroy)


submenu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu2)
submenu2.add_command(label="About", command=aboutus)

statusLabel = Label(root, text="Welcome to YY Music Player", bg="#e3c85b",relief=SUNKEN, anchor=W)
statusLabel.pack(side=BOTTOM, fill=X)


mainFrame = Frame(root)
mainFrame.pack(side=LEFT)


leftFrame = Frame(mainFrame)
leftFrame.pack(side=LEFT)

musiclabel = Label(leftFrame, text="No Music file selected")
musiclabel.pack(padx=10,pady=10)

lengthlabel = Label (leftFrame,text="Total length - --:--")
lengthlabel.pack(padx=10,pady=15)

cur_lengthlabel = Label (leftFrame,text="Current length - --:--", relief=GROOVE)
cur_lengthlabel.pack(padx=10,pady=15)

midFrame = Frame(leftFrame)
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

othFrame = Frame(leftFrame)
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



rightFrame = Frame(mainFrame)
rightFrame.pack()

playlist_lbox=Listbox(rightFrame)
playlist_lbox.pack(padx=15,pady=5)

addBtn = Button(rightFrame, text="+ ADD", command=browse_file)
addBtn.pack(side=LEFT,padx=15)

delBtn = Button(rightFrame, text="+ DEL", command=del_playlist)
delBtn.pack()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
