# Vehicle-and-Speed-Identification

## __Description__

Vehicle detection and identification systems have become increasingly common in the computer vision community over the last few years . The key processing steps involved in these systems are extracting the features of images in video frames and classifying them using trained component classifiers to determine the class of the object.
Speed detection has traditionally been achieved via directly measuring the distance from the camera to the vehicle in order to calibrate the speed of the vehicle across frame. For speed cameras specifically, they use Doppler radar technology will measures the changes of microwaves reflected from vehicles in order to obtain the speed.
Many approaches have been applied to lane detection, which can be classified as either feature-based or model-based, .Feature-based methods detect lanes by low-level features like lane-mark edges . The feature-based methods are highly dependent on clear lane-marks, and suffer from weak lanemarks, noise and occlusions. Model-based methods represent lanes as a kind of curve model which can be determined by a few critical geometric parameters.

## _Project Goals_ 

• Vehicle Detection: Being able to locate and identify vehicles in a video sequence.

• Speed Detection: Detecting the speed of the identified vehicles (km/hr) in a video sequence.

• Lane Detection: Being able to detect the lane in which the vehicle is travelling on.

## _Design & Algorithms_

Vehicles are detected using a deep learning approach with a fully convolutions network, details of which are explained below.
The data-set is explored here. It is comprised of im- ages taken from the GTI vehicle image database , the KITTI vision benchmark suite, and the ex- amples were extracted from the test video itself. The data-set is labelled with two classes, cars and non-cars. Cars have a label of 1.0, whereas non-cars have a la- bel of 0.0, as can be seen from the following figure:

 
