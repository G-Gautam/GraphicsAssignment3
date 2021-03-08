'''
Module Name: tessel
Author: CS3388
Contributor: Gautam Gupta
DOC: 03-07-2021

Purpose: This class tesselates (fills a plane with repeating polygons) the objects of a graphical scene into convex polygons
and computes the color shade to fill the polgons with. It uses different polymetric object, camera, and a light source to 
achieve this.

Parameters:
objectList: A list of parametric objects from the previous assingment of type parametricObject
camera: A cameraMatrix object to implement a synthethic camera matrix
light: A single lightsource of type lightSource which has a set position and intensity to influence the color index

Contribution:
Implemented the constructor of the class including the decleration of instance variables as needed. The constructor utilizes
the predefined and implemented helper methods of the class to tesselate parametric objects. The code for the constructor was
written based on the guided comments (left in code).
'''
import numpy as np
from matrix import matrix

class tessel:

    def __init__(self,objectList,camera,light):
        EPSILON = 0.001
        #Create an empty list of faces. This is an instance variable for this class
        self.__faceList = []
        #Create an empty list for the points forming a face
        facePoints = []
	    #Transform the position of the light into viewing coordinates (use method worldToViewingCoordinates from class cameraMatrix)
        lightViewing = camera.worldToViewingCoordinates(light.getPosition())
	    #Get light intensity values
        lightIntensity = light.getIntensity()

        #For each object in objectList:
        for obj in objectList:
            #Get the object color
            color = obj.getColor()
            #u becomes the start value of the u-parameter range for the object
            u = obj.getURange()[0]
            #While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
            while u + obj.getUVDelta()[0] < obj.getURange()[1] + EPSILON:
                #v become the start value of the v-parameter range for the object
                v = obj.getVRange()[0]
                #While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
                while v + obj.getUVDelta()[1] < obj.getVRange()[1] + EPSILON:
                    #Collect surface points transformed into viewing coordinates in the following way:
                        #Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
                        #Transform these points with the transformation matrix of the object
                        #Transform these points from world to viewing coordinates
                        #Append these points (respecting the order) to the list of face points
                    facePoints.append(camera.worldToViewingCoordinates(obj.getT()*obj.getPoint(u,v)))
                    facePoints.append(camera.worldToViewingCoordinates(obj.getT()*obj.getPoint(u,v+obj.getUVDelta()[1])))
                    facePoints.append(camera.worldToViewingCoordinates(obj.getT()*obj.getPoint(u+obj.getUVDelta()[0],v+obj.getUVDelta()[1])))
                    facePoints.append(camera.worldToViewingCoordinates(obj.getT()*obj.getPoint(u+obj.getUVDelta()[0],v)))

                    #Make sure we don't render any face with one or more points behind the near plane in the following way:
                    #Compute the minimum Z-coordinate from the face points
                    minZ = self.__minCoordinate(facePoints, 2)
                    #If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):
                    if not minZ > -camera.getNp():
                        #Compute the centroid point of the face points
                        centroid = self.__centroid(facePoints)
                        #Compute the normal vector of the face, normalized
                        normalVector = self.__vectorNormal(facePoints)
                        #Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
                        if not self.__backFace(centroid, normalVector):
                            #S is the vector from face centroid to light source, normalized
                            S = self.__vectorToLightSource(lightViewing, centroid)
                            #R is the vector of specular reflection
                            R = self.__vectorSpecular(S, normalVector)
                            #V is the vector from the face centroid to the origin of viewing coordinates
                            V = self.__vectorToEye(centroid)
                            #Compute color index
                            colorIndex = self.__colorIndex(obj, normalVector, S, R, V)
                            #Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
                            #(object color (red channel) * light intensity (red channel) * index,
                            redChannel = int(color[0]*lightIntensity[0]*colorIndex)
                            # object color (green channel) * light intensity (green channel) * index,
                            greenChannel = int(color[1]*lightIntensity[1]*colorIndex)
                            # object color (blue channel) * light intensity (blue channel) * index)
                            blueChannel = int(color[2]*lightIntensity[2]*colorIndex)
                            faceColor = (redChannel, greenChannel, blueChannel)

                            pixelFacePoints = []
                            #For each face point:
                            for facePoint in facePoints:
                                #Transform point into 2D pixel coordinates and append to a pixel face point list
                                pixelFacePoints.append(camera.viewingToPixelCoordinates(facePoint))
                            #Add all face attributes to the list of faces in the following manner:
                            #append pixel Z-coordinate of face centroid, the pixel face point list, and the face color
                            self.__faceList.append((camera.viewingToPixelCoordinates(centroid).get(2,0),pixelFacePoints,faceColor))
                    #Re-initialize the list of face points to empty
                    facePoints = []
                    #v become v + delta v
                    v += obj.getUVDelta()[1]
                #u becomes u + delta u
                u += obj.getUVDelta()[0]

    def __minCoordinate(self,facePoints,coord): 
	#Computes the minimum X, Y, or Z coordinate from a list of 3D points
	#Coord = 0 indicates minimum X coord, 1 indicates minimum Y coord, 2 indicates minimum Z coord.
        min = facePoints[0].get(coord,0)
        for point in facePoints:
            if point.get(coord,0) < min:
                min = point.get(coord,0)
        return min

    def __backFace(self,C,N):
	#Computes if a face is a back face with using the dot product of the face centroid with the face normal vector
        return C.dotProduct(N) > 0.0

    def __centroid(self,facePoints):
	#Computes the centroid point of a face by averaging the points of the face
        sum = matrix(np.zeros((4,1)))
        for point in facePoints:
            sum += point
        return sum.scalarMultiply(1.0/float(len(facePoints)))

    def __vectorNormal(self,facePoints):
	#Computes the normalized vector normal to a face with the cross product
        U = (facePoints[3] - facePoints[1]).removeRow(3).normalize()
        V = (facePoints[2] - facePoints[0]).removeRow(3).normalize()
        return U.crossProduct(V).normalize().insertRow(3,0.0)

    def __vectorToLightSource(self,L,C):
        return (L.removeRow(3) - C.removeRow(3)).normalize().insertRow(3,0.0)

    def __vectorSpecular(self,S,N):
        return  S.scalarMultiply(-1.0) + N.scalarMultiply(2.0*(S.dotProduct(N)))

    def __vectorToEye(self,C):
        return C.removeRow(3).scalarMultiply(-1.0).normalize().insertRow(3,0.0)

    def __colorIndex(self,object,N,S,R,V):
	#Computes local components of shading
        Id = max(N.dotProduct(S),0.0)
        Is = max(R.dotProduct(V),0.0)
        r = object.getReflectance()
        index = r[0] + r[1]*Id + r[2]*Is**r[3]
        return index

    def getFaceList(self):
        return self.__faceList