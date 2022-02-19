from tkinter import Tk, Canvas, PhotoImage, Button
from random import randint as rnd

def generate(update):
	g = Canvas(root, width=X, height=Y, bg="#ffffff")
	g.pack()
	img = PhotoImage(width=X, height=Y)
	g.create_image((X, Y), image=img, state="normal")
	Button(root, text="Update", command=update).pack()
	root.mainloop()

def just_render():
	old = [[grid[y][x] for x in range(X)] for y in range(X)]
	for y in range(Y):
		for x in range(X):
			if (old[y][x] > 3):
				grid[y][x] -= 3
				if x != 0: grid[y][x-1] += 1
				if x != len(grid[0])-1: grid[y][x+1] += 1
				if y != 0: grid[y-1][x] += 1
				if y != len(grid)-1: grid[y+1][x] += 1
  for y in range(Y):for x in range(X):img.put(f"#{grid[y][x]*2}00000", (x,y))

global grid, X, Y, root
root = Tk()
X = 100
Y = 101
grid = [[rnd(0, 3) for _ in range(X)] for _ in range(Y)]
generate(just_render)
