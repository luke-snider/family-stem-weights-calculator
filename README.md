# family-stem-weights-calculator
A python version of Pablo Impallari's font family stem weights calculator for Robofont and GlyphsApp. 


stemWeightCalculator_RF.py + stemWeightCalculator_GlyphsApp.py:
------------------------------------
calculates and print stem values and the related interpolation values within a font family

• Stem Values are calculated from the first stem of a reference glyph (e.g. "n") at a certain vertical postion (BeamPos) in two fonts (RoboFont) or two master layers (GlyphsApp).

• Or one can manually provide values for calculation in the script itself.

(for details take a look at OPTIONS in the script)

stemWeightCalculatorDrawbot.py
------------------------------------
A Script for RoboFont and Glyphs App that creates a graph of stem weight calculations with DrawBot.

It draws 3 curves (Luc de Groot's interpolation theory, Pablo Impallari's proposal and a curve which lies in between both: the Schneider Interpolation Curve)

Requires the DrawBot extension:

GlyphsApp: https://github.com/schriftgestalt/DrawBotGlyphsPlugin

Robofont: https://github.com/typemytype/drawBotRoboFontExtension



stemWeightCalculator_RF.py + stemWeightCalculator_GlyphsApp.py:
------------------------------------
![alt text](https://github.com/luke-snider/family-stem-weights-calculator/blob/master/thin.png)
![alt text](https://github.com/luke-snider/family-stem-weights-calculator/blob/master/black.png)
![alt text](https://github.com/luke-snider/family-stem-weights-calculator/blob/master/output.png)

stemWeightCalculatorDrawbot.py
------------------------------------
![alt text](https://github.com/luke-snider/family-stem-weights-calculator/blob/master/graph2.png)
