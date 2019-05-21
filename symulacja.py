import tkinter
import random


class Point:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius


def loop():
    global p
    p.x += random.randint(-3, 3)
    p.y += random.randint(-3, 3)
    simulation_window.delete(tkinter.ALL)
    simulation_window.create_oval(p.x - p.radius, p.y - p.radius, p.x + p.radius, p.y + p.radius, fill=('#%02x%02x%02x' % (150, 150, 150)))
    main_window.after(10, loop)


main_window = tkinter.Tk()

simulation_window = tkinter.Canvas(main_window, width=1000, height=1000, bg="Black")
simulation_window.pack()

p = Point(500, 500, 10)

loop()

main_window.mainloop()
