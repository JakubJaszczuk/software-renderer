import numpy as np
from Camera import Camera


class Scene:
	
	def __init__(self):
		# Dane sceny
		self.verts = None
		self.tris = None
		self.camera = None
		self.verts_t = None
		# Dane do odczytu i zapisu		
		self.path = None
		self.lines = None
		

	def load(self):
		# Otwórz plik
		with open(self.path) as file:
			# Zrzuć wszystkie linie do list stringów
			self.lines = file.readlines()
			# Iteruj -> Dojdź najpierw do wierzchołków
			i = 0
			temp = "points_count"
			while self.lines[i][: len(temp)] != temp:
				i += 1
			# Utwórz tablicę na wierzchołki
			self.verts = np.empty((int(self.lines[i][len(temp):]), 3))
			# Ładuj wierzchołki
			for j in range(self.verts.shape[0]):
				i += 1
				self.verts[j] = np.fromstring(self.lines[i], sep=" ")
			
			# Idź dalej do trójkątów
			temp = "triangles_count"
			while self.lines[i][: len(temp)] != temp:
				i += 1
			# Utwórz tablicę na trójkąty
			self.tris = np.empty((int(self.lines[i][len(temp):]), 3), dtype=int)
			# Ładuj trójkąty
			for j in range(self.tris.shape[0]):
				i += 1
				self.tris[j] = np.fromstring(self.lines[i], sep=" ", dtype=int)
			
			# Idź dalej do kamery
			temp = "cam_name"
			while self.lines[i][: len(temp)] != temp:
				i += 1
			# Utwórz kamerę
			self.camera = Camera()
			self.camera.origin = np.fromstring(self.lines[i+2][4:], sep=" ")
			self.camera.target = np.fromstring(self.lines[i+3][7:], sep=" ")
			self.camera.fov= int(np.fromstring(self.lines[i+4][4:], sep=" "))
			self.camera.rotation = np.fromstring(self.lines[i+5][9:], sep=" ")


	def save(self):
		# Idź do kamery
		i = 0
		temp = "cam_name"
		while self.lines[i][: len(temp)] != temp:
			i += 1

		self.lines[i+2] = "pos " + np.array2string(self.camera.origin, separator=" ")[1:-1]
		self.lines[i+3] = "lookAt " + np.array2string(self.camera.target, separator=" ")[1:-1]
		self.lines[i+4] = "fov " + str(self.camera.fov)
		self.lines[i+5] = "rotation " + str(self.camera.rotation)
		# Zapisanie do pliku
		# TO DO


	def transform(self, w, h):
		# Przekopiuj wierzchołki do transformacji
		self.verts_t = np.array(self.verts)
		temp = np.ones((self.verts_t.shape[0], 1))
		self.verts_t = np.append(self.verts_t, temp, axis=1)

		# Policz macierz transformacji
		forward = self.camera.target - self.camera.origin
		forward = forward / np.linalg.norm(forward)
		#right = np.cross(np.array([0, 1, 0]), forward)
		right = np.cross(forward, np.array([0, 1, 0]))
		#up = np.cross(forward, right)
		up = np.cross(right, forward)
		
		forward = np.append(forward, 0)
		right = np.append(right, 0)
		up = np.append(up, 0)
		eye = np.append(self.camera.origin, 1)

		transformMatrix = np.eye(4)

		transformMatrix[0, :] = right
		transformMatrix[1, :] = up
		transformMatrix[2, :] = forward
		transformMatrix[3, :] = eye

		#print(transformMatrix)

		transformMatrix = np.linalg.inv(transformMatrix)
		
		# Macierz projekcji
		aspect = w / h
		ang = np.tan(np.radians(self.camera.fov / 2.))
		proj = np.eye(4)

		proj[0, 0] = 1. / (aspect * ang)
		proj[1, 1] = 1. / ang
		proj[2, 2] = -(self.camera.far + self.camera.near) / (self.camera.far - self.camera.near)
		proj[2, 3] = -1.
		proj[3, 2] = -(2. * self.camera.far * self.camera.near) / (self.camera.far - self.camera.near)
		proj[3, 3] = 0

		#transformMatrix =  transformMatrix @ proj @ np.eye(4)

		# Transformuj wierzchołki
		self.verts_t = self.verts_t @ (transformMatrix @ proj)
		self.verts_t = self.verts_t / -np.matrix(self.verts_t[:, 3]).T
		#print(self.verts_t)

		