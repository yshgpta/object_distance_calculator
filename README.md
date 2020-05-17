# Calculation of distance between objects in video
This project deals with the calculation of distance between objects in a video with the help of opencv.
For this we take a reference object whose width is predefined. With this knowledge we can compute the ditance between the objects.

## Libraries 
<ul>
<li> imutils </li>
<li> openCV </li>
<li> numpy </li>
<li> scipy </li>
</ul>

## Usage
`pip install requirements.txt` </br>
 Create two folders `Frames` and `Processed` for storing frames of your video in source directory. </br>
 Add your video to source directory. </br>
 Change the width/frame rate of your reference object. </br>
`python3 distance_calculation.py`</br>


###### Here is one of processed video
![](generated.gif)