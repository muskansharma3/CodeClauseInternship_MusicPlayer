import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import filedialog, PhotoImage
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from pygame import mixer
from dark_title_bar import *

class MusicPlayer(tb.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.main = main
        self.pack()
        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.body()
        self.controller()
        self.songlist_area()

        self.main.bind('<Left>', self.previous_song)
        self.main.bind('<space>', self.playPauseSong)
        self.main.bind('<Right>', self.next_song)

    # Structure of Music player
    def body(self):
        self.song = tb.Label(self, font=("Times New Roman", 20, "bold"), justify="center")
        self.song['text'] = "Song Track"
        self.song.grid(row=0, column=0, pady=15)

        self.songcover = tb.Label(self, bootstyle="danger", borderwidth=5, image=coverImage, justify="center")
        self.songcover.grid(row=2, column=0, pady=5, padx=40)

        self.controls = tb.Frame(self)
        self.controls.config(width=470, height=90)
        self.controls.grid(row=3, column=0, pady=10)

        self.songlist = tb.LabelFrame(self, text=f'Playlist - {str(len(self.playlist))}', border=5)
        self.songlist.config(width=470)
        self.songlist.grid(row=5, column=0, pady=10)

    def controller(self):

        def volume_slider():
            def scaler(event):
                    if int(self.volume_scale.get()) == 0:
                        self.volume.config(image=muteImage)
                        mixer.music.set_volume(0)
                    elif 0 < int(self.volume_scale.get()) <= 40:
                        self.volume.config(image=lowsoundImage)
                        mixer.music.set_volume(self.volume_scale.get()/100)
                    else:
                        self.volume.config(image=soundImage)
                        mixer.music.set_volume(self.volume_scale.get()/100)

                    self.volume_value.config(text=f'{int(self.volume_scale.get())}')
                    mixer.music.set_volume(self.volume_scale.get()/100)

            self.volume_scale = tb.Scale(self, bootstyle="light", length=170,orient="vertical", from_=100, to=0, command=scaler)
            self.volume_scale.set(60)
            mixer.music.set_volume(0.6)
            self.volume_scale.grid(row=2, column=0, sticky="sw")

            self.volume_value = tb.Label(self, font=("Arial", 12), bootstyle="light")
            self.volume_value.config(text=f'{int(self.volume_scale.get())}')
            self.volume_value.grid(row=3, column=0, sticky="nw", pady=10)

            self.main.after(20000, self.volume_scale.grid_remove)
            self.main.after(20000, self.volume_value.grid_remove)

        self.volume = tb.Button(self.controls, image=soundImage, bootstyle="dark-link", command=volume_slider)
        self.volume.grid(row=0, column=0)

        self.previous = tb.Button(self.controls, image=previousImage, bootstyle="dark-link", command=self.previous_song)
        self.previous.grid(row=0, column=1)

        self.playPause = tb.Button(self.controls, image=playImage, bootstyle="dark-link", command=self.pause_song)
        self.playPause.grid(row=0, column=2)

        self.next = tb.Button(self.controls, image=nextImage, bootstyle="dark-link", command=self.next_song)
        self.next.grid(row=0, column=3)

        self.loadSong = tb.Button(self.controls, image=loadFileImage, bootstyle="dark-link", command=self.retrieve_song)
        self.loadSong.grid(row=0, column=4)

    def songlist_area(self):
        self.scroll = tb.Scrollbar(self.songlist, orient="vertical", bootstyle="light-round")
        self.scroll.grid(row=0, column=1, rowspan=5, sticky="ns")

        self.list = Listbox(self.songlist, selectmode="single", yscrollcommand=self.scroll.set, width=40, font=("Arial", 11))

        self.enumerate_song()
        self.list.bind('<Double-1>', self.play_song)

        self.scroll.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def enumerate_song(self):
        if self.playlist:
            for index, song in enumerate(self.playlist):
                self.list.insert(index, os.path.basename(song))
        else:
            self.list.insert(0, "Please! Load your Audio files.")

    def retrieve_song(self):
        self.tracklist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.tracklist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.tracklist, f)

        self.playlist = self.tracklist
        self.songlist['text'] = f'Playlist - {str(len(self.playlist))}'
        self.list.delete(0, END)
        self.enumerate_song()

    def playPauseSong(self, event):
        if self.paused:
            self.play_song()
        else:
            self.pause_song()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for num in range(len(self.playlist)):
                self.list.itemconfigure(num)

        mixer.music.load(self.playlist[self.current])

        self.playPause['image'] = pauseImage
        self.paused = False
        self.played = True
        self.song['text'] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, background='#002b36')
        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.playPause['image'] = playImage

        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.playPause['image'] = pauseImage

    def previous_song(self, event=None):
        self.main.focus_set()
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, background='#073642')
        self.play_song()

    def next_song(self, event=None):
        self.main.focus_set()
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = len(self.playlist)
            self.play_song()
        self.list.itemconfigure(self.current -1, background='#073642')
        self.play_song()


window = tb.Window(themename="solar")
window.title("Music Player")
window.geometry("485x850+700+40")
window.resizable(False, False)
dark_title_bar(window)

coverImage = PhotoImage(file="C:\\Users\\91958\\Music Player Python\\static\\images\\cover.png")
previousImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\previous.png")
playImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\play.png")
pauseImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\pause.png")
nextImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\next.png")
soundImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\sound.png")
lowsoundImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\lowsound.png")
muteImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\mute.png")
loadFileImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\loadFile.png")

iconImage = PhotoImage(file = "C:\\Users\\91958\\Music Player Python\\static\\images\\logo.png")
window.iconphoto(False, iconImage)

app = MusicPlayer(main=window)

app.mainloop()
