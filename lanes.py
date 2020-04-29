import cv2
import numpy as np
'''
We will use edge detection to be able to indentify sharp changes in intensity/color in adjacent pixels.
Intensity of a pixel goes from 0 -255 Black-White.
In contrast gradient is the measure of change in brightness over adjacent pixels.And strong gradients can help us identify edges on our image.
We will be converting our image to grayscale since it only deals with one color chanel instead of 3 with RGB images.
Once we have converted our image to grayscale we have to reduce image noise to smoothen our image because image noise can affect edge detection.
We will use the Gausian blur to smooth picture and filter image noise.
The way the gausian blur works by setting each pixel to the average of the neighbor pixels therefore smoothing the image.
'''
image =cv2.imread("static /media/test_image.jpg") #This loads the image and returns it as a multidimensional mupy array containing the relative intensaties of each pixel in the array.
road_image = np.copy(image) # it is important that we create a copy of our image so the changes we make dont affect the original image
grayscale_image = cv2.cvtColor(road_image, cv2.COLOR_RGB2GRAY)# cvtColor function helps converts images color and we are using this function to create our greyscale image.
gblur = cv2.GaussianBlur(grayscale_image,(5,5),0)#This is  applying a guassian blur to a grayscale image with a 5*5 kernel(good for most cases) with a standard deviation of 0.
cv2.imshow("Result",gblur) #this renders and names our image
cv2.waitKey(0)#Time of 0 will display our window infinitley till we click something in our keyboard.



