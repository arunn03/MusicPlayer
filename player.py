from mutagen.mp3 import MP3
from tkinter import *
from tkinter import ttk
from os import listdir, environ
from random import shuffle
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from threading import Thread

mixer.init()

def listSongs():
    global songs
    songs = listdir(path)
    shuffle(songs)
    for i in songs:
        if not i.endswith('.mp3'):
            songs.remove(i)
        else:
            listBox.insert(END, str(songs.index(i) + 1) + '. ' + i[:-4])
    listFrame['text'] = 'Playlist - ' + str(len(songs))

def riseVol(event=None):
    global volume

    if volume < 100:
        volume += 1

    mixer.music.set_volume(volume / 100)
    lblVol['text'] = 'Volume: ' + str(volume)

def decVol(event=None):
    global volume

    if volume > 0:
        volume -= 1

    mixer.music.set_volume(volume / 100)
    lblVol['text'] = 'Volume: ' + str(volume)

def timer():
    global seconds
    global minutes
    global songNo

    file = MP3(path + songs[songNo])

    totSec = int(file.info.length)
    totSec %= 3600
    minute = totSec // 60
    totSec %= 60

    time = mixer.music.get_pos() // 1000
    seconds = (time % 60)
    minutes = time // 60

    lblTime['text'] = "%02d:%02d" % (minutes, seconds) + ' - ' + "%02d:%02d" % (minute, totSec)

    if time + 1 == int(file.info.length):
        playNext()
        return

    lblTime.after(1000, timer)

def playPrev(event=None):
    global songNo
    global minutes

    if songNo in range(1, len(songs)+1):
        mixer.music.unload()
        songNo -= 1
        thread_play()
    else:
        return

def playNext(event=None):
    global songNo
    global minutes

    if songNo in range(len(songs)-1):
        mixer.music.unload()
        songNo += 1
        thread_play()
    else:
        return

def thread_play():
    Thread(target=play).start()

def play():
    global songs
    global paused

    paused = False
    btnPause['image'] = pauseImage
    btnPlay['image'] = rewindImage

    mixer.music.load(path + songs[songNo])
    curSong.set(str(songNo+1) + ". '" + songs[songNo][:-4] + "' - Playing")
    timer()
    mixer.music.play()

def thread_pause(event=None):
    Thread(target=pause).start()

def pause():
    global paused
    global path

    if paused:
        curSong.set(str(songNo+1) + ". '" + songs[songNo][:-4] + "' - Playing")

        if int(mixer.music.get_pos()) == -1:
            play()
        else:
            mixer.music.unpause()

        paused = False
        timer()
        btnPause['image'] = pauseImage
    else:
        curSong.set(str(songNo+1) + ". '" + songs[songNo][:-4] + "' - Paused")
        btnPlay['image'] = rewindImage
        btnPause['image'] = playImage
        mixer.music.pause()
        paused = True

root = Tk()
root.title("Music Player")
root.config(bg='white')
root.iconbitmap('./res/icon.ico')

paused = True
path = './songs/'
songs = []
songNo = 0
seconds = 0
minutes = 0
volume = 100
curSong = StringVar()
curSong.set('Click Play or press Space')
timeSet = StringVar()
timeSet.set('mm:ss')
musicImage = PhotoImage(file='./res/music.png')
backImage = PhotoImage(file='./res/back.png')
playImage = PhotoImage(file='./res/play.png')
pauseImage = PhotoImage(file='./res/pause.png')
rewindImage = PhotoImage(file='./res/rewind.png')
nextImage = PhotoImage(file='./res/next.png')

label = Label(root, image=musicImage, bg='white')
label.pack()

lblSong = Label(root, textvar=curSong, relief='solid', bg='gold', fg='black',
                width=50,
                font=('arial', 14, 'bold'))
lblSong.pack(padx=10, pady=20, expand='yes')

detFrame = Frame(root, bg='white')
detFrame.pack(padx=10, pady=5, expand='yes')

btnFrame = Frame(root, bg='white')
btnFrame.pack(padx=10, pady=5, expand='yes')

listFrame = LabelFrame(root, text='Playlist - 0', bg='white',
                       font=('arial', 15, 'bold'),
                       borderwidth=10)
listFrame.pack(padx=10, pady=10, expand='yes')

lblTime = Label(detFrame, text="00:00 - 00:00", bg='white', font=('arial', 14, 'bold'))
lblTime.grid(row=0, column=0, padx=20)

lblVol = Label(detFrame, text='Volume: 100', bg='white', font=('arial', 14, 'bold'))
lblVol.grid(row=0, column=1, padx=20)

btnPrev = Button(btnFrame, bg='white', image=backImage, command=playPrev, borderwidth=0)
btnPrev.grid(row=0, column=0, padx=20)
root.bind('<Shift-Left>', playPrev)

btnPlay = Button(btnFrame, bg='white', image=rewindImage, command=thread_play, borderwidth=0)
btnPlay.grid(row=0, column=1, padx=20)

btnPause = Button(btnFrame, bg='white', image=playImage, command=thread_pause, borderwidth=0)
btnPause.grid(row=0, column=2, padx=20)
root.bind('<space>', thread_pause)

btnNext = Button(btnFrame, bg='white', image=nextImage, command=playNext, borderwidth=0)
btnNext.grid(row=0, column=3, padx=20)
root.bind('<Shift-Right>', playNext)

root.bind('<Shift-Up>', riseVol)
root.bind('<Shift-Down>', decVol)

listBox = Listbox(listFrame, bg='white', fg='black', width=50, borderwidth=0,
                  font=('arial', 10, 'bold'))
listBox.pack(side=LEFT, fill='y')

yScroll = ttk.Scrollbar(listFrame, orient="vertical", command=listBox.yview)
listBox.configure(yscroll=yScroll.set)
yScroll.pack(side=RIGHT, fill='y')

listSongs()

root.mainloop()
