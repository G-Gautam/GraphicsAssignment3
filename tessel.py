import numpy as np
from matrix import matrix

class tessel:

    def __init__(self,objectList,camera,light):
        EPSILON = 0.001
        #Create an empty list of faces. This is an instance variable for this class
        #Create an empty list for the points forming a face
	#Transform the position of the light into viewing coordinates (use method worldToViewingCoordinates from class cameraMatrix)
	#Get light intensity values

	#For each object in objectList:
            #Get the object color
	    #u becomes the start value of the u-parameter range for the object
	    #While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
		v become the start value of the v-parameter range for the object
		#While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
                    #Collect surface points transformed into viewing coordinates in the following way:

		    #Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
		    #Transform these points with the transformation matrix of the object
		    #Transform these points from world to viewing coordinates
		    #Append these points (respecting the order) to the list of face points

                    #Make sure we don't render any face with one or more points behind the near plane in the following way:
		    #Compute the minimum Z-coordinate from the face points
		    #If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):
			#Compute the centroid point of the face points
			#Compute the normal vector of the face, normalized
			#Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
			if not backFace(centroid, face normal):
			    #S is the vector from face centroid to light source, normalized
			    #R is the vector of specular reflection
			    #V is the vector from the face centroid to the origin of viewing coordinates
			    #Compute color index
			    #Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
			    #(object color (red channel) * light intensity (red channel) * index,
			    # object color (green channel) * light intensity (green channel) * index,
			    # object color (blue channel) * light intensity (blue channel) * index)
			    #For each face point:
				#Transform point into 2D pixel coordinates and append to a pixel face point list
			    #Add all face attributes to the list of faces in the following manner:
				#append pixel Z-coordinate of face centroid, the pixel face point list, and the face color
		#Re-initialize the list of face points to empty
		#v become v + delta v
	    #u becomes u + delta u
      
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