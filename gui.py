from tkinter import *

root = Tk()
root.title("Tk Example")
root.minsize(200, 200)  # width, height
root.geometry("300x300+50+50")

# Create Label in our window
text = Label(root, text="Nothing will work unless you do.")
text.pack()
text2 = Label(root, text="- Maya Angelou")
text2.pack()
root.mainloop()