import os
import math
import face_recognition
import argparse
import pickle
import cv2

# construct the argument parser and parse the arguments
import numpy

aaa = ''
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
# load the input image and convert it from BGR to RGB
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb,
                                        model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)
# initialize the list of names for each face detected
names = []

per = []
# loop over the facial embeddings
for encoding in encodings:
    # attempt to match each face in the input image to our known
    # encodings
    matches = face_recognition.compare_faces(data["encodings"],
                                             encoding)
    # print(matches)
    name = "Unknown"
    # check to see if we have found a match
    if True in matches:
        # find the indexes of all matched faces then initialize a
        # dictionary to count the total number of times each face
        # was matched
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        # loop over the matched indexes and maintain a count for
        # each recognized face face
        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1
        # determine the recognized face with the largest number of
        # votes (note: in the event of an unlikely tie Python will
        # select first entry in the dictionary)
        face_distances = face_recognition.face_distance(data["encodings"], encoding)
        name = max(counts, key=counts.get)
        aaa2=0
        for i, face_distance in enumerate(face_distances):
            if face_distance < 0.6:
                aaa2 = (1 - face_distance) * 100
                print(numpy.round(aaa2, 4))
        aaa = "%.2f" % round(aaa2, 2)
        # update the list of names
    per.append(aaa)
    # update the list of names
    names.append(name)
for ((top, right, bottom, left), name, aaa) in zip(boxes, names, per):
    # draw the predicted face name on the image
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name+aaa, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)

# show the output image
# imS = cv2.resize(image, (600, 400))
'''for i, face_distance in enumerate(face_distances):
    if face_distance < 0.6:
        print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
        print(
            "- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
        print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(
            face_distance < 0.5))
        aaa = (1 - face_distance) * 100
        print(face_distance)
        print(aaa)
        print(numpy.round(aaa, 4))  # upto 4 decimal places'''
cv2.imshow("Image", image)
#base = os.path.basename(args["image"])
#path = 'D:/test0002/output'
#cv2.imwrite(os.path.join(path, base), image)

cv2.waitKey(0)
# python test.py --encodings encodings.pickle --image D:\dowloads\pp.jpg

