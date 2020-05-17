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
<ul>
<li>`pip install requirements.txt`</li>
<li>Create two folders `Frames` and `Processed` for storing frames of your video in source directory.</li>
<li>Add your video to source directory.</li>
<li>Change the width/frame rate of your reference object.</li>
<li>`python3 distance_calculation.py`
</ul>

###### Here is one of processed video
![](generated.gif)