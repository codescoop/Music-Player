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
current_music = "downloads/dj.mp3"
pause_status = False
stop_status = False
mute_status = False
tread_status = False
reset_tread = False
audio_length = 0.0
time_tread=threading.Thread()
time_counter="unactive"

def browse_file():
    global current_music
    global pause_status

    current_music = filedialog.askopenfilename()
    # print(current_music)
    pause_status = False
    # mixer.music.stop()
    global reset_tread
    global time_counter

    print("browse--------",reset_tread)
    if time_counter == "active":
        reset_tread = True
    time.sleep(4)
    # reset_tread = False
    print(reset_tread)
    play_music()


def aboutus():
    messagebox.showinfo("Music Player - [YYScoop.com]", "This is a Music Player created by the volunteers of YYScoop.com")


def play_music():
    global current_music
    global pause_status
    global stop_status

    if pause_status== False:

        stop_status = False
        if current_music != "":
            print("1111111111111111111111")
            mixer.music.load(current_music)
            mixer.music.play()
            statusLabel["text"] = "Playing Music" + " - " + os.path.basename(current_music)
            dispaly_music()
        else:
            messagebox.showerror("File not found", "No file selected. Please check again")

    elif pause_status == True and stop_status == True:
        print("2222222222222222222")
        mixer.music.play()
        statusLabel["text"] = "Music restarted"
        stop_status = False
        pause_status = False

    else:
        print("33333333333333333")
        mixer.music.unpause()
        statusLabel["text"] = "Music Resumed"
        stop_status = False
        pause_status = False

    # global count
    # global tread_status
    # if tread_status == False:
    #     count += 1
    #     print(count)
    # dispaly_music()
        # tread_status = True


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
    stop_status = False
    global pause_status
    pause_status = False
    global reset_tread
    global time_counter

    print("rewind",reset_tread)
    if time_counter == "active":
        reset_tread = True
    # reset_tread = True
    time.sleep(2)

    print(reset_tread)
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
    musiclabel["text"]="Playing - "+os.path.basename(current_music)

    file_ext = os.path.splitext(current_music)[1]

    if file_ext == ".wav":
        audio = mixer.Sound(current_music)
        audio_length=audio.get_length()
    else:
        audio_metadata = mp3(current_music)
        audio_length = audio_metadata.info.length

    s_min,s_sec = divmod(audio_length,60)
    format_length = "{:02d}:{:02d}".format(round(s_min),round(s_sec))
    lengthlabel["text"] = "Total length - "+ format_length
    global time_tread
    time_tread = threading.Thread(target=count_duration, args=(audio_length,))
    time_tread.start()
    # start_tread()
    print("leaving dispaly")


def count_duration(s_time):
    global time_counter
    time_counter = "active"

    # time.sleep(2)
    print("entered count_duration \n")
    original_t = s_time
    print(original_t)
    global reset_tread
    print(reset_tread)
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
            print("exit entered ")
    print("exit count_duration \n")


# def start_tread():
#     global time_tread
#     global audio_length
#     global reset_tread
#     time_tread = threading.Thread(target=count_duration, args=(audio_length,))
#     if reset_tread == False:
#         print("Entered start tread \n")
#         time_tread.start()
#         # reset_tread = True
#         print("Tread Started \n")
#     else:
    #     # print("Tread Killed \n")
    #     # time_tread.join()
    #
    #     print("-----------")
    #     reset_tread = False
    #     start_tread()


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


musiclabel = Label(root, text="No Music file selected")
musiclabel.pack(padx=10,pady=10)

lengthlabel = Label (root,text="Total length - --:--")
lengthlabel.pack(padx=10,pady=15)

cur_lengthlabel = Label (root,text="Current length - --:--", relief=GROOVE)
cur_lengthlabel.pack(padx=10,pady=15)

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

statusLabel = Label(root, text="Welcome to YY Music Player", bg="#e3c85b",relief=SUNKEN, anchor=W)
statusLabel.pack(side=BOTTOM, fill=X)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
