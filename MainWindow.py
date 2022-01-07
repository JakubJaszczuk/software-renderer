import tkinter as tk
from tkinter import filedialog as fdial
import numpy as np
from Scene import Scene
import time

class MainWindow(tk.Tk):

	def __init__(self):
		super().__init__()
		self.title("Rendering 3D")
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)

		self.var1 = tk.DoubleVar()
		self.var2 = tk.DoubleVar()
		self.var3 = tk.DoubleVar()
		self.var4 = tk.DoubleVar()
		self.var5 = tk.DoubleVar()
		self.var6 = tk.DoubleVar()
		
		# Widoki -> 4 Canvasy
		self.view1 = tk.Canvas(self, bg="black")
		self.view1.grid(row=0, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.view2 = tk.Canvas(self, bg="black")
		self.view2.grid(row=0, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		self.view3 = tk.Canvas(self, bg="black")
		self.view3.grid(row=1, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.viewPersp = tk.Canvas(self, bg="black")
		self.viewPersp.grid(row=1, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		# Panel kontrolii
		self.controlFrame = tk.Frame()
		self.controlFrame.grid(row=2, column=0)
		self.loadBtn = tk.Button(self.controlFrame, text="Wczytaj", command=self.load)
		self.loadBtn.grid(row=0, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.saveBtn = tk.Button(self.controlFrame, text="Zapisz")
		self.saveBtn.grid(row=0, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		self.fovSlider = tk.Scale(self.controlFrame, from_=0, to=99, tickinterval=9, orient=tk.HORIZONTAL, length=300, command=self.sliderEvt)
		self.fovSlider.grid(row=1, columnspan=2)
		# Panel pozycji punktów
		self.posFrame = tk.Frame()
		self.posFrame.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputOX = tk.Entry(self.posFrame, textvariable=self.var1)
		self.inputOX.grid(row=0, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputOY = tk.Entry(self.posFrame, textvariable=self.var2)
		self.inputOY.grid(row=1, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputOZ = tk.Entry(self.posFrame, textvariable=self.var3)
		self.inputOZ.grid(row=2, column = 0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputPX = tk.Entry(self.posFrame, textvariable=self.var4)
		self.inputPX.grid(row=0, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputPY = tk.Entry(self.posFrame, textvariable=self.var5)
		self.inputPY.grid(row=1, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		self.inputPZ = tk.Entry(self.posFrame, textvariable=self.var6)
		self.inputPZ.grid(row=2, column = 1, sticky=tk.N+tk.S+tk.E+tk.W)
		# Właściwe dane
		self.scene = Scene()
		self.margin = 20
		# Inne operacje
		self.bind("<Configure>", self.on_resize)
		self.last_callback_time = time.time()
		# Obsługa myszy
		self.dragged = 0;
		self.view1.bind("<Button-1>", self. mv1)
		self.view1.bind("<ButtonRelease-1>", self. mv1r)
		self.view2.bind("<Button-1>", self. mv2)
		self.view2.bind("<ButtonRelease-1>", self. mv2r)
		self.view3.bind("<Button-1>", self. mv3)
		self.view3.bind("<ButtonRelease-1>", self. mv3r)


	def mv1(self, e):
		self.update()
		w = self.view1.winfo_width()
		h = self.view1.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[2] - min[2]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[2] * scale);
		x = self.scene.camera.target[0] * scale + transX
		y = h - (self.scene.camera.target[2] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 2
		self.update()
		w = self.view1.winfo_width()
		h = self.view1.winfo_height()
		x = self.scene.camera.origin[0] * scale + transX
		y = h - (self.scene.camera.origin[2] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 1


	def mv1r(self, e):
		self.update()
		w = self.view1.winfo_width()
		h = self.view1.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[2] - min[2]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[2] * scale);
		#x = self.scene.camera.target[0] * scale + transX
		#y = h - (self.scene.camera.target[2] * scale + transZ)
		print(self.dragged)
		if self.dragged == 1:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var1.set(ex)
			self.var3.set(ey)
		if self.dragged == 2:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var4.set(ex)
			self.var6.set(ey)
		self.dragged = 0

	
	def mv2(self, e):
		self.update()
		w = self.view2.winfo_width()
		h = self.view2.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[1] * scale);
		x = self.scene.camera.target[0] * scale + transX
		y = h - (self.scene.camera.target[1] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 2
		x = self.scene.camera.origin[0] * scale + transX
		y = h - (self.scene.camera.origin[1] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 1


	def mv2r(self, e):
		self.update()
		w = self.view2.winfo_width()
		h = self.view2.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[1] * scale);
		#x = self.scene.camera.target[0] * scale + transX
		#y = h - (self.scene.camera.target[2] * scale + transZ)
		if self.dragged == 1:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var1.set(ex)
			self.var2.set(ey)
		if self.dragged == 2:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var4.set(ex)
			self.var5.set(ey)
		self.dragged = 0


	
	def mv3(self, e):
		self.update()
		w = self.view3.winfo_width()
		h = self.view3.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[2] - min[2]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[2] * scale);
		transZ = self.margin - (min[1] * scale);
		x = self.scene.camera.target[2] * scale + transX
		y = h - (self.scene.camera.target[1] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 2
		x = self.scene.camera.origin[2] * scale + transX
		y = h - (self.scene.camera.origin[1] * scale + transZ)
		if(np.abs(x - e.x) + np.abs(y - e.y) < 10 ):
			self.dragged = 1


	def mv3r(self, e):
		self.update()
		w = self.view3.winfo_width()
		h = self.view3.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[2] - min[2]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[2] * scale);
		transZ = self.margin - (min[1] * scale);
		#x = self.scene.camera.target[0] * scale + transX
		#y = h - (self.scene.camera.target[2] * scale + transZ)
		if self.dragged == 1:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var3.set(ex)
			self.var2.set(ey)
		if self.dragged == 2:
			ex = (e.x - transX) / scale
			ey = (h - e.y - transZ) / scale
			self.var6.set(ex)
			self.var5.set(ey)
		self.dragged = 0


	def setVars(self):
		self.var1.trace("w", self.updateCameraPos)
		self.var2.trace("w", self.updateCameraPos)
		self.var3.trace("w", self.updateCameraPos)
		self.var4.trace("w", self.updateCameraPos)
		self.var5.trace("w", self.updateCameraPos)
		self.var6.trace("w", self.updateCameraPos)


	def setInitial(self):
		self.fovSlider.set(self.scene.camera.fov)
		self.var1.set(self.scene.camera.origin[0])
		self.var2.set(self.scene.camera.origin[1])
		self.var3.set(self.scene.camera.origin[2])
		self.var4.set(self.scene.camera.target[0])
		self.var5.set(self.scene.camera.target[1])
		self.var6.set(self.scene.camera.target[2])
		#self.inputOX.delete(0, tk.END)
		#self.inputOX.insert(0, self.scene.camera.origin[0])
		self.inputOY.delete(0, tk.END)
		self.inputOY.insert(0, self.scene.camera.origin[1])
		self.inputOZ.delete(0, tk.END)
		self.inputOZ.insert(0, self.scene.camera.origin[2])

		self.inputPX.delete(0, tk.END)
		self.inputPX.insert(0, self.scene.camera.target[0])
		self.inputPY.delete(0, tk.END)
		self.inputPY.insert(0, self.scene.camera.target[1])
		self.inputPZ.delete(0, tk.END)
		self.inputPZ.insert(0, self.scene.camera.target[2])


	def sliderEvt(self, value):
		self.scene.camera.fov = float(value)
		self.drawViewPersp()


	def updateCameraPos(self, x, y, z):
		if self.var1.get() != "":
			self.scene.camera.origin[0] = self.var1.get()
		if self.var2.get() != "":
			self.scene.camera.origin[1] = self.var2.get()
		if self.var3.get() != "":
			self.scene.camera.origin[2] = self.var3.get()
		if self.var4.get() != "":
			self.scene.camera.target[0] = self.var4.get()
		if self.var5.get() != "":
			self.scene.camera.target[1] = self.var5.get()
		if self.var6.get() != "":
			self.scene.camera.target[2] = self.var6.get()
		self.refresh()


	def load(self):
		print("Ładuję")
		# Daj ścieżkę do pliku
		file = fdial.askopenfilename()
		# Poustawiaj scenę
		if(file):
			self.scene = Scene()
			self.scene.path = file
			self.scene.load()
			self.setInitial()
			self.refresh()
		else:
			print("Nie wybrano pliku")
	

	def on_resize(self, event):
		cur_time = time.time()
		#print(cur_time - self.last_callback_time)
		if (cur_time - self.last_callback_time) > 0.3:
			self.refresh()
		self.last_callback_time = time.time()


	def refresh(self):
		self.update()
		self.drawView1()
		self.drawView2()
		self.drawView3()
		self.drawViewPersp()


	def drawView1(self):
		self.update()
		self.view1.delete(tk.ALL)
		# Daj szerokość i wysokość canvasa
		w = self.view1.winfo_width()
		h = self.view1.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[2] - min[2]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[2] * scale);
		# Iteracja po trójkątach
		for triangle in self.scene.tris:
			v = self.scene.verts[triangle] * scale
			#v2 = np.array(v)
			v[:, 0] += transX
			v[:, 2] += transZ
			# Rysuj
			self.view1.create_line(v[0, 0], h - v[0, 2], v[1, 0], h - v[1, 2], fill='white')
			self.view1.create_line(v[0, 0], h - v[0, 2], v[2, 0], h - v[2, 2], fill='white')
			self.view1.create_line(v[1, 0], h - v[1, 2], v[2, 0], h - v[2, 2], fill='white')
		# Pozycja kamery
		self.view1.create_rectangle(self.scene.camera.origin[0] * scale + transX,
			h - (self.scene.camera.origin[2] * scale + transZ),
			self.scene.camera.origin[0] * scale + transX + 5,
			h - (self.scene.camera.origin[2] * scale + transZ + 5), fill='cyan')
		self.view1.create_rectangle(self.scene.camera.target[0] * scale + transX,
			h - (self.scene.camera.target[2] * scale + transZ),
			self.scene.camera.target[0] * scale + transX + 5,
			h - (self.scene.camera.target[2] * scale + transZ + 5), fill='red')
		

	def drawView2(self):
		self.view2.delete(tk.ALL)
		# Daj szerokość i wysokość canvasa
		w = self.view2.winfo_width()
		h = self.view2.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[0] - min[0]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[0] * scale);
		transZ = self.margin - (min[1] * scale);
		# Iteracja po trójkątach
		for triangle in self.scene.tris:
			v = self.scene.verts[triangle] * scale
			v[:, 0] += transX
			v[:, 1] += transZ
			# Rysuj
			self.view2.create_line(v[0, 0], h - v[0, 1], v[1, 0], h - v[1, 1], fill='white')
			self.view2.create_line(v[0, 0], h - v[0, 1], v[2, 0], h - v[2, 1], fill='white')
			self.view2.create_line(v[1, 0], h - v[1, 1], v[2, 0], h - v[2, 1], fill='white')
		# Pozycja kamery
		self.view2.create_rectangle(self.scene.camera.origin[0] * scale + transX,
			h - (self.scene.camera.origin[1] * scale + transZ),
			self.scene.camera.origin[0] * scale + transX + 8,
			h - (self.scene.camera.origin[1] * scale + transZ + 8), fill='cyan')
		self.view2.create_rectangle(self.scene.camera.target[0] * scale + transX,
			h - (self.scene.camera.target[1] * scale + transZ),
			self.scene.camera.target[0] * scale + transX + 5,
			h - (self.scene.camera.target[1] * scale + transZ + 5), fill='red')


	def drawView3(self):
		self.view3.delete(tk.ALL)
		# Daj szerokość i wysokość canvasa
		w = self.view3.winfo_width()
		h = self.view3.winfo_height()
		# Daj miny i maksy
		min = np.min(self.scene.verts, axis=0)
		max = np.max(self.scene.verts, axis=0)
		# Wyznacz współczynnik skalowania
		scale = ((w - self.margin) - (self.margin)) / (max[2] - min[2]);
		scale2 = ((h - self.margin) - (self.margin)) / (max[1] - min[1]);
		if scale2 < scale:
			scale = scale2
		transX = self.margin - (min[2] * scale);
		transZ = self.margin - (min[1] * scale);
		# Iteracja po trójkątach
		for triangle in self.scene.tris:
			v = self.scene.verts[triangle] * scale
			v[:, 2] += transX
			v[:, 1] += transZ
			# Rysuj
			self.view3.create_line(v[0, 2], h - v[0, 1], v[1, 2], h - v[1, 1], fill='white')
			self.view3.create_line(v[0, 2], h - v[0, 1], v[2, 2], h - v[2, 1], fill='white')
			self.view3.create_line(v[1, 2], h - v[1, 1], v[2, 2], h - v[2, 1], fill='white')
		# Pozycja kamery
		self.view3.create_rectangle(self.scene.camera.origin[2] * scale + transX,
			h - (self.scene.camera.origin[1] * scale + transZ),
			self.scene.camera.origin[2] * scale + transX + 8,
			h - (self.scene.camera.origin[1] * scale + transZ + 8), fill='cyan')
		self.view3.create_rectangle(self.scene.camera.target[2] * scale + transX,
			h - (self.scene.camera.target[1] * scale + transZ),
			self.scene.camera.target[2] * scale + transX + 5,
			h - (self.scene.camera.target[1] * scale + transZ + 5), fill='red')


	def drawViewPersp(self):
		self.viewPersp.delete(tk.ALL)
		# Daj szerokość i wysokość canvasa
		w = self.viewPersp.winfo_width()
		h = self.viewPersp.winfo_height()
		self.scene.transform(w, h);
		# Iteracja po trójkątach
		for triangle in self.scene.tris:
			v = self.scene.verts_t[triangle]
			v[:, 0] = (v[:, 0] + 1) / 2 * w
			v[:, 1] = (v[:, 1] + 1) / 2 * h
			# Rysuj
			if (v[0, 2] < 0 or v[1, 2] < 0):
				self.viewPersp.create_line(v[0, 0], h - v[0, 1], v[1, 0], h - v[1, 1], fill='white')
			if (v[0, 2] < 0 or v[2, 2]):
				self.viewPersp.create_line(v[0, 0], h - v[0, 1], v[2, 0], h - v[2, 1], fill='white')
			if (v[1, 2] < 0 or v[2, 2] < 0):
				self.viewPersp.create_line(v[1, 0], h - v[1, 1], v[2, 0], h - v[2, 1], fill='white')
			#self.viewPersp.create_line(v[0, 0], h - v[0, 1], v[1, 0], h - v[1, 1])
			#self.viewPersp.create_line(v[0, 0], h - v[0, 1], v[2, 0], h - v[2, 1])
			#self.viewPersp.create_line(v[1, 0], h - v[1, 1], v[2, 0], h - v[2, 1])



	


def main():
	mainWindow = MainWindow()
	mainWindow.scene.path = "/home/riper/Pulpit/5 semestr/Grafika/Laborki/Lista 4/room-v0.scn"
	mainWindow.scene.load()
	mainWindow.setInitial()
	mainWindow.setVars()
	mainWindow.refresh()
	mainWindow.mainloop()


if __name__ == "__main__":
	main()
