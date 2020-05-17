# Calculation of distance of objects in video using opencv
# Author : yshgpta

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import os

# Calculates the mid point of given coordinates
def midpoint(ptA, ptB):
    # using (x1+x2)/2,(y1+y2)/2
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Returns frames at given second
def getFrame(sec,count):
    # video capture at given second
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        # saving the frame
        cv2.imwrite(home_dir + "\\Frames\\" + str(count)+"_image.jpg", image)     # save frame as JPG file
    return hasFrames

def generate_frames():
    # starting second of frame genration
    sec = 0
    frameRate = 1/fps
    #counter used to save numbered image
    count=0
    success = getFrame(sec,count)
    # continue to generate frame till second exceeds the video length
    while success:
        count = count + 1
        sec = sec + frameRate
        # round second to a given precision
        sec = round(sec, 2)
        success = getFrame(sec,count)

def processing():
    for i in range(num_of_images):
        image = cv2.imread(home_dir+"\\Frames\\" + str(i) + "_image.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        
        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # sort the contours from left-to-right and, then initialize the distance colors and reference object
        (cnts, _) = contours.sort_contours(cnts)
        colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
            (255, 0, 255))
        refObj = None

        # loop over the contours individually
        for c in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < 100:
                cv2.imwrite(home_dir + "\\Processed\\" + str(i)+"_image.jpg", image)
                continue
                
            # compute the rotated bounding box of the contour
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            
            # order the points in the contour such that they appear in top-left, top-right, bottom-right, and bottom-left
            # order, then draw the outline of the rotated bounding box
            box = perspective.order_points(box)
            # compute the center of the bounding box
            cX = np.average(box[:, 0])
            cY = np.average(box[:, 1])
            
            if refObj is None:
                # unpack the ordered bounding box, then compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-right and bottom-right
                (tl, tr, br, bl) = box
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                
                # compute the Euclidean distance between the midpoints, then construct the reference object
                D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                refObj = (box, (cX, cY), D / width_of_reference_obj)
                continue
                
            # draw the contours on the image
            orig = image.copy()
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
            
            # stack the reference coordinates and the object coordinates to include the object center
            refCoords = np.vstack([refObj[0], refObj[1]])
            objCoords = np.vstack([box, (cX, cY)])
            
            # loop over the original points
            for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                # draw circles corresponding to the current points and connect them with a line
                cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
                cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
                cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),color, 2)
                
                # compute the Euclidean distance between the coordinates, and then convert the distance 
                # in pixels to distance in units
                D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
                (mX, mY) = midpoint((xA, yA), (xB, yB))
                cv2.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                
                # save the output image
                cv2.imwrite(home_dir + "\\Processed\\" + str(i)+"_image.jpg", orig)
            
def generate_video():
    # setting the name of generated video
    video_name = "generated.mp4"
    frame = cv2.imread(home_dir + "\\Processed\\0_image.jpg")
    # getting dimensions of the image frames
    height,width,layers = frame.shape
    size = (width,height)
    # generate video from images
    video  = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'DIVX'),fps,size)
    
    for i in range(num_of_images):
        video.write(cv2.imread(home_dir+"\\Processed\\"+str(i)+"_image.jpg"))
    # Destroy all the windows/threads and release the video
    cv2.destroyAllWindows()
    video.release()

width_of_reference_obj = 1.062 # In my case its diameter of 2 Rs Indian Coin

#Example Video
vidcap = cv2.VideoCapture('./video.mp4') # Add your own video
home_dir = os.getcwd()

fps = 50  #Frames per second, decreasing it increases processing but hampers continuity of video and vice versa

# This function genrates frames of our video
generate_frames()

# Total Number of frames genrated
num_of_images = len(os.listdir(home_dir + "\\Frames\\"))

# This function process the frames ie. detect and draws the contours,
# calculates the Euclidean distance wrt our reference object and 
# generates the processed frames
processing()

# This funtion convert the processed frames back to video
generate_video()
