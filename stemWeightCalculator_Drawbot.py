from __future__ import print_function, division, absolute_import
import os
from drawBot import *
''' A Script for RoboFont and Glyphs App that creates a graph of different stem weight calculations with DrawBot.
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
    fontsize = 4.5
    fontsizeGraph = 3
    
    txt_index = FormattedString()
    txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
    txt_index.append("#\t", font="Verdana Bold", fontSize=4)
    txt_index.append("Equal", font="Verdana Bold", fontSize=4)
    txt_index.fill(0.8, 0.4, 0.4, 1) # red
    txt_index.append("\tImpallari", font="Verdana Bold", fontSize=4)

    txt_index.fill(0.0, 0.9, 0.0, 1) # green
    txt_index.append("\tSchneider", font="Verdana Bold", fontSize=4)

    txt_index.fill(0, 0.2, 0.5, 0.5) # blue
    txt_index.append("\tLuc(as)", font="Verdana Bold", fontSize=4)
    txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
    txt_index.append("\n-------------------------------------------------------\n", font="Verdana Bold", fontSize=4) 
    
    impValues = []
    lucValues = []

    ### getting Schneider values
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        if roundValues == True:
            impValues.append(int(round(I)))
            lucValues.append(int(round(L)))
        else:
            impValues.append(round(I,2))
            lucValues.append(round(L,2))    
    schneiderValues = []
    for idx, val in enumerate(impValues):
        if roundValues == True:
            schneiderValues.append(int(round(((val+lucValues[idx])/2))))
        else:
            schneiderValues.append(round(((val+lucValues[idx])/2),2))
    
    ### output value table in graph
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        if roundValues == True:
            txt_index.append(str(x)+"\t")
            txt_index.append(str(int(round(E)))+"\t"+str(int(round(I)))+"\t"+str(schneiderValues[x-1])+"\t"+str(int(round(L))), font="Verdana Bold", fontSize=fontsize)
            txt_index.append("\n")
        else:
            txt_index.append(str(x)+"\t")
            txt_index.append(str(round(E,2))+"\t"+str(round(I,2))+"\t"+str(schneiderValues[x-1])+"\t"+str(round(L,2)), font="Verdana Bold", fontSize=fontsize)
            txt_index.append("\n")
    txt_index.append("-------------------------------------------------------", font="Verdana Bold", fontSize=4) 
    text(txt_index, ((10, b+10))) 
    
    


    # GRAPH   
    start = equalSteps(t,b,s,1)
    strokeWidth(0.5)
    fill(None)
    
    #equalSteps (graph + text)
    newPath()
    stroke(0.5, 0.5, 0.5, 0.5) # grey
    moveTo((start, start))
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        lineTo((E, start))
    drawPath()
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        string = str(int(E))
        txt_index = FormattedString()
        txt_index.fill(0.5, 0.5, 0.5, 0.8) # grey
        txt_index.append(string, font="Verdana Bold", fontSize=fontsizeGraph)
        text(txt_index, ((E-2, start-5)))

    #Impallari
    newPath()
    stroke(0.8, 0.4, 0.4, 1) # red
    moveTo((start, start))
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        lineTo((E, I))
    drawPath()

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

    #schneider
    newPath()
    stroke(0.0, 0.9, 0.0, 0.7) # green
    moveTo((start, start))
    for x in range(s):
        try:
            x = x+1
            E = equalSteps(t,b,s,x+1)
            lineTo((E, schneiderValues[x]))
        except IndexError:
            pass
    drawPath()

    ### Graph Text
    for x in range(s):
        x = x+1 
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        string = str(int(I))
        txt_index = FormattedString()
        txt_index.fill(0.8, 0.4, 0.4, 1) # red
        txt_index.append(string, font="Verdana Bold", fontSize=fontsizeGraph)
        txt_index.append("\n")
        string = str(schneiderValues[x-1]) 
        txt_index.fill(0.0, 0.9, 0.0, 1) # green
        txt_index.append(string, font="Verdana Bold", fontSize=fontsizeGraph)
        txt_index.append("\n")
        string = str(int(L))
        txt_index.fill(0, 0.2, 0.5, 0.5) # blue
        txt_index.append(string, font="Verdana Bold", fontSize=fontsizeGraph)
        text(txt_index, ((E-4, I+12)))


    ### OVALS
    stroke(0, 0, 0, 1)
    fill(0, 0, 0, 1)  
    oval(start-0.5, start-0.5, 1, 1)
    
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0.5, 0.5, 0.5, 1) # grey
        fill(0.5, 0.5, 0.5, 1) # grey
        oval(E-0.5, start-0.5, 1, 1)

    #Impallari
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0.8, 0.4, 0.4, 1) # red
        fill(0.8, 0.4, 0.4, 1) # red
        oval(E-0.5, I-0.5, 1, 1)
    #Luc
    for x in range(s-1):
        x = x+2
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        stroke(0, 0.2, 0.5, 1) # blue
        fill(0, 0.2, 0.5, 1) # blue
        oval(E-0.5, L-0.5, 1, 1)

    #schneider
    for x in range(s):
        try:
            x = x+1
            E = equalSteps(t,b,s,x+1)
            stroke(0.0, 0.9, 0.0, 1) # green
            fill(0.0, 0.9, 0.0, 1) # green
            oval(E-0.5, schneiderValues[x]-0.5, 1, 1)
        except IndexError:
            pass

    #saveFile
    fileDirectory = os.path.join(os.path.expanduser('~'), 'Desktop')
    exportFile = os.path.expanduser("%s/%s.pdf")% (fileDirectory, filename)
    saveImage([exportFile])#, multipage=True    

    ############ output
    print("#"+"\t"+"Equal:"+"\t\t"+"Impallari:"+"\t\t"+"Schneider:"+"\t\t"+"Luc(as):")
    print("----------------------------------------------------------------")
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        if roundValues == True:        	
            print(str(x)+"\t"+str(int(round(E)))+"\t\t\t"+str(int(round(I)))+"\t\t\t\t"+str(schneiderValues[x-1])+"\t\t\t\t"+str(int(round(L))))
        else:
            equal = '%#05.2f' % round(E,2)
            Im = '%#05.2f' % round(I,2)
            Sch = '%#05.2f' % schneiderValues[x-1]
            print(str(x)+"\t"+str(equal)+"\t\t"+str(Im)+"\t\t\t"+str(Sch)+"\t\t\t"+str(round(L,2)))
    print("----------------------------------------------------------------")

if drawbotGraph == True:
    drawAGraph()
