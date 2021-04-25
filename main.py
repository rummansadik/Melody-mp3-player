import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
import time
import threading

#root = Tk()
root = tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")

statusbar = ttk.Label(root, text = "Welcome to Melody", relief = SUNKEN, anchor = W, font = "Times 10 italic")
statusbar.pack(side = BOTTOM, fill = X)

#Create the menubar
menubar = Menu(root)
root.config(menu = menubar)

playlist = []

def browse_file():
	global filename_path
	filename_path = filedialog.askopenfilename()
	add_to_playlist(filename_path)
	
def add_to_playlist(filename):
	filename = os.path.basename(filename)
	index = 0
	playListBox.insert(index, filename)
	playlist.insert(index, filename_path)
	index += 1
	
#Create the submenu
subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label = "Open", command = browse_file)
subMenu.add_command(label = "Exit", command = root.destroy)

def about_us():
	tkinter.messagebox.showinfo("About Melody", "This software is built by Rumman Sadik.")

#Create the submenu
subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = subMenu)
subMenu.add_command(label = "About Us", command = about_us)

mixer.init()

root.title("Melody")
root.iconbitmap(r"Images/melody.ico")

#Root window - Statusbar, Leftframe, Rightframe
#Leftframe - The Listbox (playlist)
#Rightframe - Topframe, Middleframe and Bottomframe

Leftframe = Frame(root)
Leftframe.pack(side = LEFT, padx = 30)

playListBox = Listbox(Leftframe)
playListBox.pack()

addBtn = ttk.Button(Leftframe, text = "+ Add", command = browse_file)
addBtn.pack(side = LEFT)

def del_song():
	selected_song = playListBox.curselection()
	selected_song = int(selected_song[0])
	playListBox.delete(selected_song)
	playlist.pop(selected_song)	
	
delBtn = ttk.Button(Leftframe, text = "- Delete", command = del_song)
delBtn.pack(side = LEFT)

Rightframe = Frame(root)
Rightframe.pack(padx = 30)

Topframe = Frame(Rightframe)
Topframe.pack()

lengthlabel = ttk.Label(Topframe, text = "Total Length - --:--")
lengthlabel.pack(pady = 5)

currenttimelabel = ttk.Label(Topframe, text = "Current Time - --:--", relief = GROOVE)
currenttimelabel.pack()

def show_details(play_song):
	file_data = os.path.splitext(play_song)
	
	if file_data[1] == ".mp3":
		audio = MP3(play_song)
		total_length = audio.info.length
	else:
		a = mixer.Sound(play_song)
		total_length = a.get_length()
		
	mins, secs = divmod(total_length, 60)
	mins = round(mins)
	secs = round(secs)
	timeformat = "{:02d}:{:02d}".format(mins, secs)
	lengthlabel["text"] = "Total Length - " + timeformat
	
	tl = threading.Thread(target = start_count, args = (total_length,))
	tl.start()
	
def start_count(t):
	global paused
	current_time = 0
	while current_time <= t and mixer.music.get_busy():
		if 	paused:
			continue
		mins, secs = divmod(current_time, 60)
		mins = round(mins)
		secs = round(secs)
		timeformat = "{:02d}:{:02d}".format(mins, secs)
		currenttimelabel["text"] = "Current Time - " + timeformat
		time.sleep(1)
		current_time += 1
		
def play_music():	
	global paused
	if paused:
		mixer.music.unpause()
		statusbar["text"] = "Music Resumed"
		paused = False
	else:
		try:
			stop_music()
			time.sleep(1)
			selected_song = playListBox.curselection()
			selected_song = int(selected_song[0])
			play_it = playlist[selected_song]
			mixer.music.load(play_it)
			mixer.music.play()
			statusbar["text"] = "Playing " + os.path.basename(play_it)
			show_details(play_it)
			
		except:
			tkinter.messagebox.showerror("File not found", "Melody could not find the file. Please check again.")

		
paused = False
	
def pause_music():
	global paused
	paused = True
	mixer.music.pause()
	statusbar["text"] = "Music Paused"

def stop_music():
	mixer.music.stop()
	statusbar["text"] = "Music Stopped"
	
def rewind_music():
	play_music()
	statusbar["text"] = "Music Rewinded"

muted = False

def volume_music():
	global muted
	
	if muted:
		mixer.music.set_volume(0.7)
		volumeBtn.configure(image = volumePhoto)
		scale.set(70)
		muted = False
	else:
		mixer.music.set_volume(0)
		volumeBtn.configure(image = mutePhoto)
		scale.set(0)
		muted = True
		
def set_vol(val):
	volume = float(val) / 100
	mixer.music.set_volume(volume)

middleframe = Frame(Rightframe)
middleframe.pack(pady = 10)
	
playPhoto = PhotoImage(file = "Images/play.png")
playBtn = ttk.Button(middleframe, image = playPhoto, command = play_music)
playBtn.grid(row = 0, column = 0, padx = 10)


stopPhoto = PhotoImage(file = "Images/stop.png")
stopBtn = ttk.Button(middleframe, image = stopPhoto, command = stop_music)
stopBtn.grid(row = 0, column = 1, padx = 10)

pausePhoto = PhotoImage(file = "Images/pause.png")
pauseBtn = ttk.Button(middleframe, image = pausePhoto, command = pause_music)
pauseBtn.grid(row = 0, column = 2, padx = 10)

bottomframe = Frame(Rightframe)
bottomframe.pack(pady = 15)

rewindPhoto = PhotoImage(file = "Images/rewind.png")
rewindBtn = ttk.Button(bottomframe, image = rewindPhoto, command = rewind_music)
rewindBtn.grid(row = 0, column = 0)

mutePhoto = PhotoImage(file = "Images/mute.png")
volumePhoto = PhotoImage(file = "Images/volume.png")
volumeBtn = ttk.Button(bottomframe, image = volumePhoto, command = volume_music)
volumeBtn.grid(row = 0, column = 1)

scale = ttk.Scale(bottomframe, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row = 0, column = 2, pady = 15, padx = 50)


def on_closing():
	stop_music()
	root.destroy()
	
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()









