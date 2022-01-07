import numpy as np


class Camera:
	
	def __init__(self):
		self.origin = None
		self.target = None
		self.fov = 60
		self.far = 32
		self.near = 1
		self.rotation = 0
