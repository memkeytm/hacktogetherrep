import voice_recognition as vr
import adb
from callinfo import CallInfo
from memory import CommandQueue
from time import sleep
import itertools, glob
import winsound, sys
from system_tray_lib import *
import Tkinter
import sys
from Tkinter import *
from PIL import Image, ImageTk
import urllib
import adb
import requests
import threading
import tkFont
import tkMessageBox
from multiprocessing import Process

def respondCall():
	call = CallInfo()
	number = call.get_caller_number()
	caller = call.get_caller_name()

	global win
	win = Tkinter.Tk()
	win.overrideredirect(1)
	win.title("Incoming Call")
	
	width = 370
	height = 100
	win.resizable(width=FALSE, height=FALSE)
	ws = win.winfo_screenwidth() # width of the screen
	hs = win.winfo_screenheight() # height of the screen
	x = (ws/1.2) - (width/2)
	y = (hs/1.3) - (height/2)
	win.geometry('%dx%d+%d+%d' % (width, height, x, y))
	win.configure(background='white')
	
	message = '{} ({})\n is calling'.format(caller, number)
	Label(win, text=message, background="white", font=tkFont.Font(family="Helvetica", size=15)).pack()

	photoImage_accept = ImageTk.PhotoImage(file="images/accept.png")
	photoImage_reject = ImageTk.PhotoImage(file="images/reject.png")

	button_accept = Button(win, image=photoImage_accept, command=acceptCall, bd = 0, background="white").pack(side=LEFT)
	button_reject = Button(win, image=photoImage_reject, command=rejectCall, bd = 0, background="white").pack(side=RIGHT)

	global play_sound_thread
	play_sound_thread = Process(target=playSound)
	play_sound_thread.start()

	win.mainloop()

def acceptCall():
	call = CallInfo()
	call.accept_call()
	play_sound_thread.terminate()
	win.destroy()
	main()

def rejectCall():
	call = CallInfo()
	call.decline_call()
	play_sound_thread.terminate()
	win.destroy()
	main()

def playSound():
	while(1):
		winsound.PlaySound('recordings/phone_ring.wav', winsound.SND_FILENAME)

def main():
	call = CallInfo()
	check_call = False
	while(not check_call):
		check_call = call.check_if_calling()
		if(check_call == True):
			respondCall()

if __name__ == '__main__':
	main()