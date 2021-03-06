import numpy as np
from BoundBox import BoundBox

class Plane:
    
    kEpsilon = 0.0000001 #not using this now

    def __init__(self, p, n, color, ka, kd, ks, mat, ref, name, trans = None, transDeg = 0.0, glossy = None): #p is the point on the plane and n is the normal 
        self.glossy = glossy
        self.trans = trans
        self.transDeg = transDeg
        self.name = name
        self.n = n
        self.p = p
	self.ref = ref
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.mat = mat
        self.box = BoundBox(100.0,-100.0,100.0,-100.0,100.0,-100.0)

    def intersectRay(self, ray):
        
        temp = ray.d
        t = np.dot(temp, self.n)
        if t == 0 : return None
        temp = self.p - ray.o
        temp = np.dot(temp, self.n)
        t = temp / t
        if t <= 0 : return None
        return t

    def getNormal(self, xp):
        return self.n

    def getColor(self, xp):
        return self.color
