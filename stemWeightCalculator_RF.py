from __future__ import print_function, division, absolute_import

''' V1.2 Robofont Script for stem weight calculation
based on Family Stem Weight Calculator by Pablo Impallari
this script expects to have 2 fonts open with a reference glyph e.g. n'''

from mojo.tools import IntersectGlyphWithLine

## OPTIONS
s = 9 # Interpolation steps
referenceGlyph = "n" # for stem measurement (it takes the 1st stem for the calculation)
BeamPos = 200 # vertical position of stem measurement of reference glyph
roundValues = False # or False if values should not be rounded
measureStems = True # or False - if calculation should use the following two values (t + b)
t = 10 # thin-value (only used if measureStems = False)
b = 100 # black-value (only used if measureStems = False)


# E = interpolated value using equal steps (linear function in x)
def equalSteps(t,b,s,x):
    E = (b-t)/(s-1)*(x-1)+t
    return E

# L = the interpolated value using Luc(as) Formula (an exponential function in x)
def luc(t,b,s,x):
    L = t*(b/t)**((x-1)/(s-1))
    return L

# I = the interpolated value using Impallari Formula (a weighted average of E and L)
def impallari(t,b,s,x,L,E):
    I = (x-1)/(s-1)*E+(s-x)/(s-1)*L
    I = ((b * x**2) - ((2 * b) * x) + b + ((s**2 * t) * (b / t)**((x - 1) / (s - 1))) - (((s * t) * x) * (b / t)**((x - 1) / (s - 1))) + ((s * t) * x) - ((s * t) * (b / t)**((x - 1) / (s - 1))) - (t * x**2) - (s * t) + ((t * x) * (b / t)**((x - 1) / (s - 1))) + (t * x)) / (s**2 - (2 * s) + 1)
    return I

def get_stem1_of_reference_glyphs(f):
    result = IntersectGlyphWithLine(f[referenceGlyph], ((-2100, BeamPos), (f[referenceGlyph].width+2500, BeamPos)), canHaveComponent=True, addSideBearings=False)
    xValuesFromIntersection = [int(round(x[0])) for x in result]
    xValuesSorted = sorted(xValuesFromIntersection)
    stem1 = (xValuesSorted[1]-xValuesSorted[0])
    return (f,stem1)


def perform(t,b,roundValues):

    if measureStems == True:
        if len(AllFonts()) != 2:
            print("please open 2 fonts! - not more or less!")
            return
        fontAndStemDict = {}
        for f in AllFonts():
            fontAndStemDict[get_stem1_of_reference_glyphs(f)[0]] = get_stem1_of_reference_glyphs(f)[1]
        sortedFontsAndWeightsDict = [(k, fontAndStemDict[k]) for k in sorted(fontAndStemDict, key=fontAndStemDict.get, reverse=False)]
        #source1 = sortedFontsAndWeightsDict[0][0][referenceGlyph]
        #font1 = sortedFontsAndWeightsDict[0][0]
        stem1font1 = sortedFontsAndWeightsDict[0][1]
        #source2 = sortedFontsAndWeightsDict[1][0][referenceGlyph]
        #font2 = sortedFontsAndWeightsDict[1][0]
        stem1font2 = sortedFontsAndWeightsDict[1][1]
        t = stem1font1 
        b = stem1font2
    if measureStems == False:
        pass

    impallarisValues = []
    lucsValues = []
    schneidersValues = []
    for x in range(s):
        x = x+1
        E = equalSteps(t,b,s,x)
        L = luc(t,b,s,x)
        I = impallari(t,b,s,x,L,E)
        if roundValues == True:
            impValue = int(round(I))
            lucValue = int(round(L))
            impallarisValues.append(impValue)
            lucsValues.append(lucValue)
            schneidersValues.append(int(round(((impValue+lucValue)/2)))) 
        else:
            impValue = round(I,2)
            lucValue = round(L,2)
            schneiderValue = round(((impValue+lucValue)/2),2)
            impallarisValues.append(round(I,2))
            lucsValues.append(round(L,2))
            schneidersValues.append(schneiderValue)


    ############ output
    print("Impallari:"+"\t\t"+"StemWeight:"+"\t\t"+"InterpolValue:")
    print("-------------------------------------------------")
    for idx, x in enumerate(impallarisValues):
        if roundValues == True:
            impValue = int(round(((x - impallarisValues[0])/(impallarisValues[-1]-impallarisValues[0]))*1000))
        if roundValues != True:
            impValue = round(((x - impallarisValues[0])/(impallarisValues[-1]-impallarisValues[0]))*1000,2)
            impValue = '%#05.2f' % impValue
            x = '%#05.2f' % x
        print(str(idx+1)+"\t\t\t\t"+str(x)+"\t\t\t\t"+str(impValue))
    print()
    print("Schneider:"+"\t\t"+"StemWeight:"+"\t\t"+"InterpolValue:")
    print("-------------------------------------------------")
    for idx, x in enumerate(schneidersValues):
        if roundValues == True:
            schValue = int(round(((x - schneidersValues[0])/(schneidersValues[-1]-schneidersValues[0]))*1000))
        if roundValues != True:
            schValue = round(((x - schneidersValues[0])/(schneidersValues[-1]-schneidersValues[0]))*1000,2)
            schValue = '%#05.2f' % schValue
            x = '%#05.2f' % x
        print(str(idx+1)+"\t\t\t\t"+str(x)+"\t\t\t\t"+str(schValue))
    print()
    print("Luc(as):"+"\t\t"+"StemWeight:"+"\t\t"+"InterpolValue:")
    print("-------------------------------------------------")
    for idx, x in enumerate(lucsValues):
        if roundValues == True:
            lucValue = int(round(((x - lucsValues[0])/(lucsValues[-1]-lucsValues[0]))*1000))
        if roundValues != True:
            lucValue = round(((x - lucsValues[0])/(lucsValues[-1]-lucsValues[0]))*1000,2)  
            lucValue = '%#05.2f' % lucValue
            x = '%#05.2f' % x
        print(str(idx+1)+"\t\t\t\t"+str(x)+"\t\t\t\t"+str(lucValue))

perform(t,b,roundValues)
