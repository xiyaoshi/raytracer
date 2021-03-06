import numpy as np
import matplotlib.pyplot as pt
import random

from PIL import Image
from Sphere import Sphere
from Ray import Ray
from ViewPort import ViewPort
from Reflect import Reflect
from Plane import Plane
from Triangle import Triangle
from operator import itemgetter
from PhongShading import PhongShading
from math import *
from Octree import Onode, Octree
from SoftShading import SoftShading
from ObjReader import objRead



# we keep an acceleration data structure for each instance in the scene, so that we can do acceleration in time O(mlogn) where m is the number of instances and n is the complexity of each instance.
class Instance:
	def normalize(self, v):
		def magnitude(v):
			return sqrt(sum(v[i]*v[i] for i in range(len(v))))
		vmag = magnitude(v)
		return np.array([ v[i]/vmag  for i in range(len(v)) ])

	def __init__(self, mat, trans, obj):
		self.obj = obj
		self.mat = mat
		self.trans = trans
		self.inverse = []
		for item in trans:
			temp = np.linalg.inv(item)
			self.inverse.insert(0, temp)
		self.transNormal = []
		for item in self.inverse:
			temp = np.transpose(item)
			self.transNormal.insert(0,temp)
		print self.trans
		print self.inverse
		print self.transNormal

	#this is to do inverse transform to rays 
	def getTransformedRay(self, ray):
		tempo = np.array([ray.o[0], ray.o[1], ray.o[2], 1.0])
		tempd = np.array([ray.d[0], ray.d[1], ray.d[2], 1.0])
		for item in self.inverse:
			tempo = np.matmul(item, tempo)
#			tempd = np.matmul(item, tempd)
		tempo = np.array([tempo[0], tempo[1], tempo[2]]) / tempo[3]
		tempd = np.array([tempd[0], tempd[1], tempd[2]]) / tempd[3]
		tempd = self.normalize(tempd)
		ret = Ray(tempo, tempd)
		return ret

	#just use this method as you would to any primitive types, i.e. triangles , spheres
	def intersectRay(self, ray):
		ray1 = self.getTransformedRay(ray)
		ls = []
		objarr = self.obj.get(ray1)
		for item in objarr :
			t = item.intersectRay(ray1)
			if t != None :
				xp = ray1.getPoint(t)
				ls.append((t, item, xp))
		try : temp = (min(ls, key = lambda t : t[0]))
		except : return None
		xp = ray1.getPoint(temp[0])
		n = temp[1].getNormal(xp)
		n = np.array([n[0], n[1], n[2], 1.0])
		xp = np.array([temp[2][0], temp[2][1], temp[2][2], 1.0])
		for item in self.trans:
			xp = np.matmul(item, xp)
		for item in self.transNormal :
			n = np.matmul(item, n)
		xp = np.array([xp[0], xp[1], xp[2]]) / xp[3]
#		print xp
		n = np.array([n[0], n[1], n[2]]) / n[3]
		n = self.normalize(n)
		return (temp[0], temp[1], xp, n, self.mat)
