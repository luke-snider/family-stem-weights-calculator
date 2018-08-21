from __future__ import print_function, division, absolute_import
import os
from drawBot import *
''' A Script for RoboFont and Glyphs App that creates a graph of stem weight calculations with DrawBot.
Requires Drawbot for GlyphsApp: https://github.com/schriftgestalt/DrawBotGlyphsPlugin
Requires Drawbot for Robofont: https://github.com/typemytype/drawBotRoboFontExtension
based on Family Stem Weight Calculator by Pablo Impallari
'''

## OPTIONS
t = 20 # thin
b = 220 # black
s = 9 # steps
roundValues = True
drawbotGraph = True
filename = "graph"


# E = interpolated value using equal steps (linear function in x)
def equalSteps(t,b,s,x):
    E = (b-t)/(s-1)*(x-1)+t
    return E

def luc(t,b,s,x):
    # L = the interpolated value using Luc(as) Formula (an exponential function in x)
    L = t*(b/t)**((x-1)/(s-1))
    return L

def impallari(t,b,s,x,L,E):
    # I = the interpolated value using Impallari Formula (a weighted average of E and L)
    I = (x-1)/(s-1)*E+(s-x)/(s-1)*L
    I = ((b * x**2) - ((2 * b) * x) + b + ((s**2 * t) * (b / t)**((x - 1) / (s - 1))) - (((s * t) * x) * (b / t)**((x - 1) / (s - 1))) + ((s * t) * x) - ((s * t) * (b / t)**((x - 1) / (s - 1))) - (t * x**2) - (s * t) + ((t * x) * (b / t)**((x - 1) / (s - 1))) + (t * x)) / (s**2 - (2 * s) + 1)
    return I

def drawAGraph():
    newPage(b+20, b+20)
    fontsize = 4
    
    txt_index = FormattedString()
    txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
    txt_index.append("Equal Steps", font="Verdana Bold", fontSize=4)
    txt_index.fill(0.8, 0.4, 0.4, 1) # orange
    txt_index.append("\t\tImpallari", font="Verdana Bold", fontSize=4)
    txt_index.fill(0, 0.2, 0.5, 0.5) # blue
    txt_index.append("\t\tLuc(as)", font="Verdana Bold", fontSize=4)

    txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
    txt_index.append("\n-------------------------------------------------------\n", font="Verdana Bold", fontSize=4) 
    ### output
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        if roundValues == True:
            txt_index.append(str(int(round(E)))+"\t\t"+str(int(round(I)))+"\t\t"+str(int(round(L))))
            txt_index.append("\n")
        else:
            txt_index.append(str(round(E,3))+"\t\t"+str(round(I,3))+"\t\t"+str(round(L,3)))
            txt_index.append("\n")
    text(txt_index, ((10, b+10))) 

    # GRAPH   
    start = equalSteps(t,b,s,1)
    strokeWidth(0.5)
    fill(None)
    
    #equalSteps
    newPath()
    stroke(0.5, 0.5, 0.5, 0.5) # grey
    moveTo((start, start))
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        lineTo((E, E))
    drawPath()
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        string = str(int(E))
        txt_index = FormattedString()
        txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
        txt_index.append(string, font="Verdana Bold", fontSize=fontsize)
        text(txt_index, ((E-10, E+2)))

    #Impallari
    newPath()
    stroke(0.8, 0.4, 0.4, 1) # orange
    moveTo((start, start))
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        lineTo((E, I))
    drawPath()
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        string = str(int(I))
        txt_index = FormattedString()
        txt_index.fill(0.8, 0.4, 0.4, 1) # orange
        txt_index.append(string, font="Verdana Bold", fontSize=fontsize)
        text(txt_index, ((E-10, I+2)))

    #Luc
    newPath()
    stroke(0, 0.2, 0.5, 0.5) # blue
    moveTo((start, start))    
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        lineTo((E, L))
    drawPath()    
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        string = str(int(L))
        txt_index = FormattedString()
        txt_index.fill(0, 0.2, 0.5, 0.5) # grey
        txt_index.append(string, font="Verdana Bold", fontSize=fontsize)
        text(txt_index, ((E+2, L-5)))

    ### OVALS
    stroke(0, 0, 0, 1)
    fill(0, 0, 0, 1)  
    oval(start, start, 1, 1)
    
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0.5, 0.5, 0.5, 1) # grey
        fill(0.5, 0.5, 0.5, 1) # grey
        oval(E, E, 1, 1)
    #Impallari
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0.8, 0.4, 0.4, 1) # orange
        fill(0.8, 0.4, 0.4, 1) # orange
        oval(E, I, 1, 1)
    #Luc
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0, 0.2, 0.5, 1) # blue
        fill(0, 0.2, 0.5, 1) # blue
        oval(E, L, 1, 1)
    #saveFile
    fileDirectory = os.path.join(os.path.expanduser('~'), 'Desktop')
    exportFile = os.path.expanduser("%s/%s.pdf")% (fileDirectory, filename)
    saveImage([exportFile])#, multipage=True    

############ output
print("Equal Steps:"+"\t"+"Impallari:"+"\t\t"+"Luc(as):")
print("---------------------------------------")
for x in range(s):
    x = x+1
    E = equalSteps(t,b,s,x)
    L = luc(t,b,s,x)
    I = impallari(t,b,s,x,L,E)
    if roundValues == True:
        print(str(int(round(E)))+"\t\t\t\t"+str(int(round(I)))+"\t\t\t\t"+str(int(round(L))))
    else:
        print(str(round(E,3))+"\t\t\t"+str(round(I,3))+"\t\t\t"+str(round(L,3)))
print("---------------------------------------")

if drawbotGraph == True:
    drawAGraph()
