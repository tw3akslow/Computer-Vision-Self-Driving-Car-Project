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
We will overlap our interest region with our cany image by using the bitewise function that will use both photographs binary data to only show the region of interest. 0n1=0 1n1=1 like in the case of our white triangle has 255 and its  binary representation is 1 with sorounding bit representation of 0.
Then we will use the probabilistic Hough transform algorithm for line detection. 
We will use our display_borders function to  display our lanes in a black image.
We will combine both images using the addweight function that takes the sum of our color image with our border image.If its adding 0s(the black portion of our image)to whaterver is the  intensity of the original image it will just stay the same its only when we add the pixel intensities of our lines with the original picture pixels that will see a diference.
Then we will use the cv2 capture function too decode every video frame and use the same functions that we used previously for our image.

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
    mask = np.zeros_like(image)#creates an array of of 0s  with the same number of rows and columns than our correspondant images. All pixels will be black
    cv2.fillPoly(mask,triangle,255)#we will fill our mask with our triangle and set the color to white. "IS IMPORTANT TO NOTE THAT fillPolly fills an area composed of various polygons this is why our triangle has a  [[]] structure."
    masked_img = cv2.bitwise_and(image,mask)#Computing the bitwise of both of these images takes the bitwise & and pixel in both arrays ultimatlety masking the canny image to only show the area of interest.
    return masked_img

def display_borders(image,lines):
    border_image = np.zeros_like(image)#automatically the image will be black
    color=(0, 255, 0)#green
    if lines is not None: #We have to check if it actually detected any lines
        for line in lines:
            #print(lines)
            x1, y1, x2, y2 = line.reshape(4)#We are basically reshaping our 2D array into a 1 dimensional array without changing its contents
            cv2.line(border_image, (x1, y1), (x2, y2),color, 10)#draws a green  line with 10 thickness segment between our points in the image.
    return (border_image)

def average_slope_intercept(image, lines):
    leftarray = []# For our left lane
    rightarray = [] #For our right lane
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4) #We are basically reshaping our 2D array into a 1 dimensional array without changing its contents.
        parameters = np.polyfit((x1, x2),(y1, y2),1)# Polyfit will fit a polynomial with coeficients that describe the slope and y intercept we use degree 1 so we get the parameters of a linear function.
        #print(parameters)#Will print the slope and the y intercept.
        slope = parameters[0]
        y_intercept = parameters[1]
        if slope < 0: #if the slope is negative we will append it to the left side
            leftarray.append((slope,y_intercept))#will apend to array in form of a touple.
        else:
            rightarray.append((slope, y_intercept))#Else we will apend it to the right side.
    leftside_average = np.average(leftarray, axis = 0)
    rightside_average = np.average(rightarray, axis = 0)
    left_line = make_cordinates(image, leftside_average)
    right_line = make_cordinates(image, rightside_average)
    arr = np.array([left_line, right_line])
    return arr

def make_cordinates(image,line_parameters):
    slope, intercept = line_parameters
    #print(image.shape)#This will print the (height,width,number of chanels)
    y1 = image.shape[0]# Height
    y2 = int(y1 * (3/5))#Go up until height is 420 .
    #In terms of x we know  y = mx+b then the value of x would be x = (y-b)/m
    x1 =int( (y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])
#Code for image below
'''
image =cv2.imread("static /media/test_image.jpg") #This loads the image and returns it as a multidimensional numpy array containing the relative intensaties of each pixel in the array.
road_image = np.copy(image) # it is important that we create a copy of our image so the changes we make dont affect the original image
canny_image = canny(road_image)#sketch the gradients that pass the high tresholds with white and low tresholds with black as they fall below the low treshold.
croped_img = interest_region(canny_image) #creates an image from a 2-dimensional numpy array.
lines = cv2.HoughLinesP(croped_img, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)#Implements the probabilistic Hough transform algorithm for line detection. we will use 2 pixels for precision acompained with 1 degree precision in radians,our next argument will be our treshold that is the minimum amount of votes per bin needed to accept a candidate line in this case 100 .We will use a placeholder array for our lines argument  with our min lenght and gap arguments.
average_lines = average_slope_intercept(road_image, lines)
border_image = display_borders(road_image, average_lines)
combined_img = cv2.addWeighted(road_image, 0.8, border_image, 1, 1) #Takes the sum of our color image with our border image.If its adding 0s (black portion of our image)to whatever intensity of the original image it will just stay the same its only when we add the pixel intensities of our lines with the original picture pixels that will see a diference.The numbers next to each image is = the weight  assigned to each image.The last parameter is the scalar value added to both arrays.
cv2.imshow("results", road_image)
cv2.waitKey(0)# Will kill it when user presses any key
'''

#Code for video below
capture = cv2.VideoCapture("static /media/test2.mp4")
while capture.isOpened():
    b, frame = capture.read()#will decode every video frame will return booleand and current frame for our image
    canny_image = canny(frame)  # sketch the gradients that pass the high tresholds with white and low tresholds with black as they fall below the low treshold.
    croped_img = interest_region(canny_image)  # creates an image from a 2-dimensional numpy array.
    lines = cv2.HoughLinesP(croped_img, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)  # Implements the probabilistic Hough transform algorithm for line detection. we will use 2 pixels for precision acompained with 1 degree precision in radians,our next argument will be our treshold that is the minimum amount of votes per bin needed to accept a candidate line in this case 100 .We will use a placeholder array for our lines argument  with our min lenght and gap arguments.
    average_lines = average_slope_intercept(frame, lines)
    border_image = display_borders(frame, average_lines)
    combined_img = cv2.addWeighted(frame, 0.8, border_image, 1, 1)  # Takes the sum of our color image with our border image.If its adding 0s (black portion of our image)to whatever intensity of the original image it will just stay the same its only when we add the pixel intensities of our lines with the original picture pixels that will see a diference.The numbers next to each image is = the weight  assigned to each image.The last parameter is the scalar value added to both arrays.
    cv2.imshow("result", combined_img)
    cv2.waitKey(1)











