import random as n
import pygame
from pygame import *
def k(w,h):return m(lambda x:[0]*h,' '*w)
def cg(g):return m(lambda x:x[:],g)
def ro(o,c,r):return o if r<1 else ro(m(lambda x:m(lambda y:o[y][3-x-1+c],b(4)),b(4)),c,r-1)
def mo(o):
 p=n.choice(m(lambda x:[x%3+1,x in(0,3),m(lambda y:ord(y)-97,'bfjn cgkj bfjk fgjk cgfj bfgk befg'.split()[x])],b(7)))
 for t in p[2]:o[t%4][t/4]=p[0]
 return o,p[1]
m,b,v,z,L=map,range,filter,255,len
def q(a,o,x,y,n=1):
 g=cg(a)
 for c in b(16):
  tx,ty,p=c%4+x,c/4+y,o[c%4][c/4]
  if p:
   if tx<0 or tx>9 or ty>19 or (a[tx][ty] and n):return 3
   g[tx][ty]=p
 return g
