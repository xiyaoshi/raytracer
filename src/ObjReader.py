import numpy as np
from Triangle import Triangle

def objRead(fn):

    vertices = []
    indices = []
    with open(fn, "r") as f:
        for line in f:
            if line[0] == "#":
                continue
            if line[-1] == "\n" or line[-1] == "\r" :
                line = line[:-1]
            temp = line.split(" ")
            if temp[0] =="v":
                vertices.append(np.array([float(temp[1]) * 30 + 8.0, float(temp[2]) * 30, float(temp[3]) * 30 - 30]))
            elif temp[0] == "f" :
                indices.append((int(temp[1]), int(temp[2]), int(temp[3])))
    iteml = []

    print len(vertices)
    print len(indices)
    for item in indices:
        p1 = vertices[item[0] - 1]
        p2 = vertices[item[1] - 1]
        p3 = vertices[item[2] - 1]
        tri = Triangle(p1, p2, p3, np.array([0.5 ,1.0, 0.8]), 0.02, 0.75, 1, 30, 0.0)
        iteml.append(tri)

    return iteml



