'''
Module Name: lightSource
Author: CS3388
Contributor: Gautam Gupta
DOC: 03-07-2021

Purpose: This class implements a single white light source with a default position and intensity for a graphical scene.

Parameters:
position: A column vector of type matrix which contains the real world coordinates of the light's position
color: The color of the light source held as an RGB tuple. Default value white. Influences the color index of the image
intensity: A tuple to contain the intensity/brigthness of the light source. Influences the color index of the image

Contribution:
Implemented the getters and setters of this class based on the method definitons
'''

import numpy as np
from matrix import matrix

class lightSource:

    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    def getPosition(self):
        return self.__position

    def getColor(self):
        return self.__color

    def getIntensity(self):
        return self.__intensity

    def setPosition(self,position):
        self.__position = position

    def setColor(self,color):
        self.__color = color

    def setIntensity(self,intensity):
        self.__intensity = intensity
