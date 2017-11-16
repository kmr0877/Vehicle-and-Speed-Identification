#!/usr/bin/python
#written by mohan for COMP9517
#calculates speed of vehicles in realtime in km/hr
#this code mainly focusses on detecting and tracking cars by using trained  classifier which already has features of cars

#key_formula =  ( speed in object plane / distance of camera from road ) = ( speed in image plane / focal length )
#approx fps of the video = 30

#to obtain accurate value distance to object (mm)  =   focal length (mm) * real height of the object (mm) * image height (pixels)
                 #                                      ----------------------------------------------------------------
              #                                                   object height (pixels) * sensor height (mm)
import cv2
import skvideo.io
import numpy as np
import random
from collections import deque


def make_new_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

count = 0

# capt.Video frames from a video
cap = skvideo.io.vread('3.mp4')

# import the xml file which contains features of about 500+ car images
car_cascade = cv2.CascadeClassifier('cars.xml')
# i am tracking car using their centroids so i am maintaining a centroid list of all cars present in a frame
centroids_list = deque([])
car_count = 0
with open("out.csv", "w") as o:
    pass

# loop runs if capturing has been initialized.
for i in range(0, cap.shape[0]):
    center1 = []
    center2 = []

    # convert to gray scale of each frames
    # print("i:", i)
    image = cap[i]
    gray_image = cv2.cvtColor(cap[i], cv2.COLOR_BGR2GRAY)

    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray_image, 1.1, 1)

    # loop over all the found cars
    for (x, y, w, h) in cars:
        xA = x
        xB = x + w
        yA = y
        yB = y + h
# Enumerate over all the cars in centroids_list
        #each centroid_list element contains: [last_updated_frame, color, position, 
        #lock_count, unlock_count, lockstate(unlocked by default), list_of_car_speeds_in_prev_frames, id] 
        not_matched = True
        for idx, centroid_data in enumerate(centroids_list):
            if centroid_data[0] == count:
                continue
            if centroids_list[idx][4] == 0:
                centroids_list[idx][5] = "unlocked"
                centroids_list[idx][4] = 5

            # check proximity using manhattan distance
            X = abs(float(centroid_data[2][0] + centroid_data[2][2]) / 2 - float(xA + xB) / 2)
            Y = abs(float(centroid_data[2][1] + centroid_data[2][3]) / 2 - float(yA + yB) / 2)
            # if there is a rectangle in 10 pixel proximity of a rectangle of previous frame than i am assuming that,
            # the car in the rectangle is same as it was in the previous frame
            # 10 can be changed to any other value based on the movement happening in the frames, if vehicles are moving
            # more than 10 pixels per frame suppose 20 so change the value to 20
            if X < 5 and Y < 5:

                not_matched = False
                centroids_list[idx][4] = 5
                centroids_list[idx][2] = [xA, yA, xB, yB]
                centroids_list[idx][6].append(np.sqrt(X ** 2 + Y ** 2) * 30)
                if centroids_list[idx][5] == "unlocked":

                    if centroids_list[idx][0] == count - 1:
                        centroids_list[idx][3] += 1

                    else:
                        centroids_list[idx][3] = 0

                if centroids_list[idx][3] == 3:
                    centroids_list[idx][5] = "locked"
                    centroids_list[idx][3] = 0
                if centroids_list[idx][6][-1] != 0.0:
                    cv2.rectangle(image, (xA, yA), (xB, yB), centroid_data[1], 2)
                    cv2.putText(image, str(centroids_list[idx][6][-1]),
                                (xA, yA), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (np.average(centroid_data[1])/2), 1, cv2.LINE_AA)
                centroids_list[idx][0] = count
                break

#    If rectangle not matches with previous rectangles that means it is a new car so make a new rectangle
        #if rectangle is not matching wiht previous rectangles ,then it is assumed that a new car has come and so new rectangle
        if not_matched:
            color = make_new_color()

            # append new rectangle in previous cars list
            centroids_list.appendleft([count, color, (xA, yA, xB, yB), 1, 5, "unlocked", [0], car_count])
            car_count += 1
            # cv2.rectangle(image, (xA, yA), (xB, yB), color, 2)
            # cv2.putText(image, "0",
            #             (xA, yA), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
            prev_color = color
            prev_coords = [xA, yA, xB, yB]

    # plot all remaining locked rectangles
    for idx, centroid_data in enumerate(centroids_list):

        if centroid_data[5] == "locked" and centroid_data[0] != count:
            centroids_list[idx][4] -= 1
            if centroids_list[idx][6][-1] != 0.0:
                cv2.rectangle(image, (centroid_data[2][0], centroid_data[2][1]), (centroid_data[2][2], centroid_data[2][3]),
                              centroid_data[1], 2)
               # cv2.putText(image, str(centroids_list[idx][6][-1]),
                #            (centroid_data[2][0], centroid_data[2][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, centroid_data[1], 1,
                 #           cv2.LINE_AA)
                cv2.putText(image, str(centroids_list[idx][6][-1]),
                            (centroid_data[2][0], centroid_data[2][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (np.average(centroid_data[1])/2), 1,
                            cv2.LINE_AA)
            if centroids_list[idx][4] == 0:
                centroids_list[idx][5] = "unlocked"
                centroids_list[idx][4] = 5
                centroids_list[idx][3] = 0

        if count - centroid_data[0] == 10:
            if sum(centroid_data[6]) / len(centroid_data[6]) != 0.0:
                with open("out.csv", "a") as o:
                    o.write(str(centroid_data[7]) + ": " + str(sum(centroid_data[6]) / len(centroid_data[6])) + "\n")

    centroids_list = deque([car_data for car_data in list(centroids_list) if count - car_data[0] < 10])

    # Display frames in a window
    cv2.imshow('video2', image)

    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break

    # outputs all the video frames into out folder present in the working directory
    cv2.imwrite("out/" + str(count) + ".jpg", image)
    count += 1
