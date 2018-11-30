from tkinter import *


my_window = Tk()
screen_width = my_window.winfo_screenwidth()
screen_height = my_window.winfo_screenheight()
window_width = 400
window_height = 200
width = int(screen_width/2 - window_width/2)
height = int(screen_height/2 - window_height/2)

position = str(window_width) + 'x' + str(window_height) + '+' + str(width) + '+' + str(height)

my_window.geometry(position)

my_window.mainloop()