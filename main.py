from tkinter import *

mixer.init()

root = Tk()
root.title("YY MusicPlayer")
root.iconbitmap("YYmusicplayer.ico")
# root.geometry("500x500")

menubar = Menu(root,bg="#ccba41")
root.config(menu=menubar, bg="#141f30")

music_file = "default.mp3"
pause_status = False