import cv2
import numpy as np
import matplotlib.pyplot as plt
'''
We will use edge detection to be able to indentify sharp changes in intensity/color in adjacent pixels.
Intensity of a pixel goes from 0 -255 Black-White.
In contrast gradient is the measure of change in brightness over adjacent pixels.And strong gradients can help us identify edges on our image.
We will be converting our image to grayscale since it only deals with one color chanel instead of 3 with RGB images.
Once we have converted our image to grayscale we have to reduce image noise to smoothen our image because image noise can affect edge detection.
We will use the Gausian blur to smooth picture and filter image noise.
The way the gausian blur works by setting each pixel to the average of the neighbor pixels therefore smoothing the image.
We will use the cany function to measure adhacent changes in intensity in all directions x, and y like a derivative function for x and y
The Canny function will sketch the gradients that pass the high tresholds with white and low tresholds with black as they fall below the low treshold.
We will use the matplotlib pyplot library to segment the points we want to focus on.
plt.imshow(cannyI) #creates an image from a 2-dimensional numpy array.
plt.show() you get a y and x axis that you can get the points you want to segment in terms of x y
Once we have analysed our area of interest we will create a mask using our interest_region() function.
We will blend our interest region with our cany image by using the bitewise function that will use both photographs binary data to only show the region of interest. 0n1=0 1n1=1 like in the case of our white triangle with binary representation of 1 with sorounding bit representation of 0 

'''

def canny(image):
    grayscale_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)  # cvtColor function helps converts images color and we are using this function to create our greyscale image.
    gblur = cv2.GaussianBlur(grayscale_image, (5, 5),0)  # This is  applying a guassian blur to a grayscale image with a 5*5 kernel(good for most cases) with a standard deviation of 0.
    canny = cv2.Canny(gblur, 50,150)  # Canny function computes grading in all directions of our image.Parameters are (image ,low_threshold,high treshold).If our gradient is greater that the upper treshold it is accepted as an edge pixel ,if its below the low treshold is declined,if its in the middle then it will only be acepted if its connected to an edge Its recomended to use ratios of 1/2 or 1/3 as such we will use 1/3
    return canny

def interest_region(image):
    height = image.shape[0] # y value row 
    triangle = np.array([
        [(200,height),(1100,height),(550,250)]#points x,y for our triangle our area of interest.
    ])#This is our area of interest from our plt chart.Where each array position is represented as an array of points.
    print(triangle)
    mask = np.zeros_like(image)#creates an array of of 0s  with the same number of rows and columns than our correspondant images. All pixels will be black
    cv2.fillPoly(mask,triangle,255)#we will fill our mask with our triangle and set the color to white. "IS IMPORTANT TO NOTE THAT fillPolly fills an area composed of various polygons this is why our triangle has a  [[]] structure."
    masked_img = cv2.bitwise_and(image,mask)#Computing the bitwise of both of these images takes the bitwise & and pixel in both arrays ultimatlety masking the canny image to only hsow the area of interest.
    return masked_img


image =cv2.imread("static /media/test_image.jpg") #This loads the image and returns it as a multidimensional mupy array containing the relative intensaties of each pixel in the array.
road_image = np.copy(image) # it is important that we create a copy of our image so the changes we make dont affect the original image
cannyI = canny(road_image)
cv2.imshow("result",interest_region(cannyI)) #creates an image from a 2-dimensional numpy array.
cv2.waitKey(0)# Will kill it when user presses any key










