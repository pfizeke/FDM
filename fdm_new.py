# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 22:33:32 2022

@author: pfize
"""

import numpy as np
import matplotlib.pyplot as plt

circle = lambda x,y,x0,y0,r: (x-x0)**2 + (y-y0)**2 < r**2
line = lambda x,y,x0,y0,s: s*(x*x0 + y*y0) < s

class dom2d:
    def __init__(self,xmin,xmax,ymin,ymax,scale):
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.scale=scale
        self.grid=set()
        for i in range(int(xmin/scale),int(xmax/scale)+1):
            for j in range(int(ymin/scale),int(ymax/scale)+1):
                self.grid.add((i,j))
        self.boundary=set()
        for i in self.grid:
            if len(self.grid.intersection(set([(i[0]-1,i[1])
                                               ,(i[0]+1,i[1])
                                               ,(i[0],i[1]-1)
                                               ,(i[0],i[1]+1)])))<4:
                self.boundary.add(i)
        self.subs=[]
        self.sub_bounds=[]
    def plot(self,data=None,marker='.'):
        if data==None:
            data=self.grid
        data=self.scale*np.asarray(list(data)).T
        plt.plot(data[0],data[1],marker)
    def sub(self,bounds,exclude=True):
        grid=set()
        boundary=set()
        for i in self.grid:
            in_sub=True
            for j in bounds:
                in_sub=in_sub*j(i[0]*self.scale,i[1]*self.scale)
            if in_sub:
                grid.add(i)
        if exclude:
            self.grid.difference_update(grid)
            self.boundary.difference_update(grid)
        for i in grid:
            if len(self.grid.intersection(set([(i[0]-1,i[1])
                                               ,(i[0]+1,i[1])
                                               ,(i[0],i[1]-1)
                                               ,(i[0],i[1]+1)])))>0:
                boundary.add(i)
        self.subs.append(grid)
        self.sub_bounds.append(boundary)

def conn(data):
    res=dict()
    for i in data:
        vic=data.intersection(set([(i[0]-1,i[1]),(i[0]+1,i[1]),(i[0],i[1]-1),(i[0],i[1]+1)]))
        res.update({i:list(vic)})
    return res
        
dom=dom2d(-3,3,-3,3,0.1)
dom.sub([lambda x,y:circle(x,y,-3,-3,2)])
dom.sub([lambda x,y:circle(x,y,-3,3,2)])
dom.sub([lambda x,y:circle(x,y,3,-3,2)])
dom.sub([lambda x,y:circle(x,y,3,3,2)])
"""
dom.sub([lambda x,y:line(x,y,0,1,1),
         lambda x,y:line(x,y,1,0,1),
         lambda x,y:line(x,y,0,-1,1),
         lambda x,y:line(x,y,-1,0,1)])
"""
plt.figure(figsize=(9,9))
plt.xlabel('x, mm')
plt.ylabel('y, mm')
plt.title('Potential array 2D')
dom.plot(dom.grid,'b+')
dom.plot(dom.boundary,'g.')
for i in dom.subs:
    dom.plot(i,'k.')
for i in dom.sub_bounds:
    dom.plot(i,'r.')
