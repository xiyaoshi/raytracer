"""
University of Illinois/NCSA Open Source License>
Copyright (c) 2016 University of Illinois
All rights reserved.
Developed by: 		Eric Shaffer
                  Department of Computer Science
                  University of Illinois at Urbana Champaign
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal with the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimers.Redistributions in binary form must reproduce the above copyright notice, this list
of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
Neither the names of <Name of Development Group, Name of Institution>, nor the names of its contributors may be
used to endorse or promote products derived from this Software without specific prior written permission.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS WITH THE SOFTWARE.
""" 

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
from ObjReader import objRead 
from Octree import Onode, Octree
from SoftShading import SoftShading
from Trans import Transparency
from glossy import Glossy

#create a viewport and image
v = ViewPort(np.array([0.0,0.0,0.0]), np.array([0.0,0.0,-10.0]), np.array([0.0,1.0,0.0]), 5.0, 10.0, 500)
im = Image.new("RGB",(v.w, v.h))
pix = im.load()

tree = Octree()

#define a point light 
light = SoftShading(np.array([-1.0, 10.0, 0.0]), np.array([1.0, 10.0, 0.0]), np.array([-1.0, 12.0, 0.0]), np.array([1.0,12.0,0.0]), np.array([1.0,1.0,1.0]),0.8)

#define a sphere
radius = 1.0
#materialS = np.array([1.0,0.0,0.0])
#for j in range(-5, 5, 5):
#    for i in range(-5, 5, 5):
#        center = np.array([-5 + i ,-3.0 - j, -20.0])
#        s = Sphere(radius,center,materialS, 1.0,1.0,1.0,4, 0.0 )
#	materialS = np.copy(materialS)
#	materialS[2] += 0.25
#	materialS[0] -= 0.25
#        tree.insert(s)
#        objarr1.append(s)
#point = np.array([0.0,-10.0,-13.0])
#normal = np.array([0.0,-1.0,0.0])
#p = Plane(point, normal, np.array([0.0,1.0,0.0]),1.0 ,1.0,0.05,150, 0.6)
#p1 = np.array([-15.0,-10.0,-250.0])
#p2 = np.array([15.0,-10.0,-250.0])
#p3 = np.array([-15.0,-10.0,-10.0])
#tri = Triangle(p1, p2, p3, np.array([1.0,1.0,1.0]),0.8,0.75,0.05,100, 0.6, "tri1", texture = "triangle1.jpg", noiseTexture = False) 
#tree.insert(tri)
#
#
p3 = np.array([-10.0,10.0,-20.0])
p2 = np.array([10.0,-10.0,-20.0])
p1 = np.array([-10.0,-10.0,-20.0])
tri = Triangle(p1, p2, p3, np.array([1.0,1.0,1.0]),0.8,0.75,0.05,100, 0.6, "tri1", texture = "triangle1.jpg", noiseTexture = False, hori = np.array([20.0,0.0,0.0]), verti = np.array([0.0,-20.0,0.0]), origin = 2) 

p1 = np.array([10.0,10.0,-20.0])
p2 = np.array([-10.0,10.0,-20.0])
p3 = np.array([10.0,-10.0,-20.0])
tri1 = Triangle(p1, p2, p3, np.array([1.0,1.0,1.0]),0.8,0.75,0.05,100, 0.6, "tri2", texture = "triangle1.jpg", origin = 1 , hori = np.array([20.0,0.0,0.0]), verti = np.array([0.0,-20.0,0.0])) 
tree.insert(tri)
tree.insert(tri1)
ray = Ray(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,-1.0]))

point = np.array([0.0,-10.0 ,0.0])
normal = np.array([0.0,-1.0,0.0])
p = Plane(point, normal, np.array([1.0,1.0,1.0]),1.0 ,1.0,0.05,150, 0.6, "plane1")
tree.insert(p)
radius = 3
center = np.array([-10.0, -7.0, -17.0])
s = Sphere(radius, center, np.array([0.289, 0.2845, 0.3779]), 1.0, 1.0, 1.0, 4, 0.0, "sphere1", noise = True, priori1 = np.array([0.8, 0.6, 1.0]), priori2 = np.array([1.0, 1.0, 1.0]), noisyText = "noisetext.png")
tree.insert(s)

center = np.array([3.0, -7.0, -17.0])
s1 = Sphere(radius, center, np.array([0.289, 0.2845, 0.3779]), 1.0, 1.0, 1.0, 4, 0.0, "sphere2", noise = False, priori1 = np.array([0.8, 0.6, 1.0]), priori2 = np.array([1.0, 1.0, 1.0]), trans = 1.31, transDeg = 1.0)
tree.insert(s1)
p1 = np.array([-15.0,-9.99,-20.0])
p2 = np.array([-15.0,-9.99,-10.0])
p3 = np.array([20.0,-9.99,-10.0])
tri1 = Triangle(p1, p3, p2, np.array([1.0,1.0,1.0]),0.8,0.75,0.05,100, 0.6, "tri2", glossy = 0.8) 
print tri1.getNormal(np.array([4,4,4]))
print p.getNormal(np.array([3,3,3]))
print 
tree.insert(tri1)

transp = Transparency(tree, light, v.e)
glossy = Glossy(tree, light, v.e, transp)

def normalize(v):
    def magnitude(v):
        return sqrt(sum(v[i]*v[i] for i in range(len(v))))
    vmag = magnitude(v)
    return np.array([ v[i]/vmag  for i in range(len(v)) ])

print v.center
print v.e
print v.c1
print v.c2
print v.c3
print v.c4
print np.dot(v.l, v.c3 - v.c1)
print np.dot(v.c2 - v.c1 , v.c3 -  v.c1)
print np.dot(v.c4 - v.c2 , v.c4 -  v.c3)

def normColor(temp):
    temp[0] = 1.0 if temp[0] > 1.0 else temp[0]
    temp[0] = 0 if temp[0] < 0 else temp[0]
    temp[1] = 1.0 if temp[1] > 1.0 else temp[1]
    temp[1] = 0 if temp[1] < 0 else temp[1]
    temp[2] = 1.0 if temp[2] > 1.0 else temp[2]
    temp[2] = 0 if temp[2] < 0 else temp[2]
    temp[0] = int(temp[0] * 255)
    temp[1] = int(temp[1] * 255)
    temp[2] = int(temp[2] * 255)
    return temp


#if multijittered is on which is very expensive
multijittered = 0

for col in range(v.w):
    if col % 10 == 0:       print col
    for row in range(v.h):
            if multijittered == 0:
                ray.o = v.getPixelCenter(row, col)
#                print ray.o
                ray.d = ray.o - v.e
                ray.d = normalize(ray.d)
#                ray.d = np.array([0.0,0.0,-1.0])
                ls = []
                objarr = tree.get(ray)
                for item in objarr :
                    t = item.intersectRay(ray)
                    if t != None :
                        xp = ray.getPoint(t)
#                        ls.append((t, item.k, item.color, item.mat, item.getNormal(xp), xp, v.e))
                        ls.append((t, item, xp))
                try : 
                    #if len(ls) == 1:
                    #    pix[col, (v.h - 1) - row] = ls[0][1]
                    temp = (min(ls, key = lambda t : t[0]))
		except : 
                    pix[col, (v.h - 1) - row] = (0,0,0)
                    continue
                if temp[1].trans == None and temp[1].glossy == None:
                    temp = light.simpleRender(temp[1].ka, temp[1].kd, temp[1].ks, temp[1].getColor(temp[2]),temp[1].mat,temp[1].getNormal(temp[2]), temp[2], v.e)
                elif temp[1].glossy == None:
                    temp = transp.render(ray, 1, temp[1], temp[2], inObj = False)
                else :
                    temp = glossy.render(ray, 1, temp[1], temp[2])

                temp = normColor(temp)
                pix[col, (v.h - 1) - row] = (int(temp[0]), int(temp[1]), int(temp[2]))
#                    temp = transparency.trans(ray, 1, light, temp[1], temp[2], False)
#                    in_shade = 0
#                    xp = temp[2]
#		    rayo = np.copy(ray.o)
#		    rayd = np.copy(ray.d)
#		    ray1 = Ray(rayo, rayd)
#                    ray.o = xp
#		    try :
#                        objarr = tree.get(ray)
#		    except : 
#			objarr = None
#                    darr = light.getSampleArr()
#		    if objarr != None:
#                        for dtemp in darr:
#                            ray.d = dtemp - xp
#                            ray.d = normalize(ray.d)
#                            for item in objarr :
#                                if item == temp[1] : continue
#                                t = item.intersectRay(ray)
#                                if t != None and t > 0.01: 
#                                    in_shade += 1
#                                    break
#                    temp1 = light.ambientRender(temp[1].ka, temp[1].color)
#                    temp1 = normColor(temp1)
#                    temp1 *= in_shade
#		    temp2 = reflect.ref(ray1, 1, light)
#                    temp = normColor(temp2)
#                    temp *= (16 - in_shade)
#                    temp += temp1
#                    temp /= 16
#		    print temp

#                    maxn =  np.amax(temp)
#                    minn = np.amin(temp)
#                    temp = temp + minn
##                    print maxn, temp
#                    temp = temp / maxn * 255
#                    print " after ",
#                    print maxn, temp
#                        print "aaaaaaaaa"
#                    print (int(temp[0]), int(temp[1]), int(temp[2]))
                    

#multijittered sampling for each pixel 16 samples and take box filter
#            tempArr = v.getMultiJitteredArray(row, col) 
#            colorTemp = (0,0,0)
#            for item in tempArr:
#                ray.o = item
#                ray.d = ray.o - v.e
#                ray.d = normalize(ray.d)
#                t = s.intersectRay(ray)
#                tp = p.intersectRay(ray)
#                tt = tri.intersectRay(ray)
#                ls = []
#                if t != None :
#                    xp = ray.getPoint(t)
#                    ls.append((t, phongDiffuse(xp, s.getNormal(xp), s.material)))
#                if tp != None :
#                    xp = ray.getPoint(tp)
#                    ls.append((tp, phongDiffuse(xp, p.getNormal(), p.c)))
##                    ls.append((tp, (0,255,0)))
#                if tt != None :
#                    xp = ray.getPoint(tt)
#                    ls.append((tt, phongDiffuse(xp, tri.getNormal(), tri.c)))
##                    print  phongDiffuse(xp, tri.getNormal(), tri.c)
##                    ls.append((tt, (0,0,255)))
#                try :
##                    print (min(ls, key = lambda t : t[0]))[1]
#                    colorTemp1 = (min(ls, key=lambda t : t[0]))[1]
#                    colorTemp = (colorTemp[0] + colorTemp1[0], colorTemp[1] + colorTemp1[1], colorTemp[2] + colorTemp1[2])
##                    if tt != None : print colorTemp1
#                except :
#                    print "fuck"
#                    colorTemp = (0,0,0)
#            colorTemp = (colorTemp[0] / 16.0, colorTemp[1] / 16.0, colorTemp[2] / 16.0)
#            if tt != None : print colorTemp
#
#
#            pix[col, (v.h -1) -row] = (int(colorTemp[0]), int(colorTemp[1]), int(colorTemp[2]))
#            ray.o = v.getPixelCenter(col,row)
#            ray.d = ray.o - v.e
#            ray.d = normalize(ray.d)

#            print ray.d
#            print ray.o



#            if tt != None and  
#            elif (t != None and (tp < 0 or t < tp)):
#                xp = ray.getPoint(t) 
#                pix[col,(v.h-1)-row] = phongDiffuse(xp,s.getNormal(xp),s.material)
#            elif (tp != None and tp > 0 ):
#                pix[col,(v.h-1)-row] = getPlaneColor(p.c)

# Show the image in a window
                
im.show()
im.save("img2.png")
