import glob
import shutil

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
                help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []
file_path = args["encodings"]
old_data = pickle.loads(open(file_path, "rb").read())
new_embeddings = old_data['encodings']
new_names = old_data['names']
# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(i + 1,
                                                 len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]
    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb,
                                            model=args["detection_method"])
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    # loop over the encodings
    for encoding in encodings:
        # add each encoding + name to our set of known names and
        # encodings
        knownEncodings.append(encoding)
        knownNames.append(name)
        new_embeddings.append(knownEncodings[0])
        new_names.append(knownNames[0])
# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
#data = {"encodings": knownEncodings, "names": knownNames}
#f = open(args["encodings"], "wb")
#f.write(pickle.dumps(data))
#f.close()
testNew = 'encodings.pickle'
print(knownNames,knownEncodings)
data1 = {"encodings": new_embeddings, "names": new_names}
with open(testNew, 'wb') as fp:
    pickle.dump(data1, fp)
    fp.close()
d = "data2/cdgs"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    a = full_path
    print(full_path)
    source_dir = a
    target_dir = 'data/cdgs'
path2 = os.path.normpath(source_dir)
LL=path2.split(os.sep)
path3 = os.path.normpath(target_dir)
LL2=path3.split(os.sep)
print(LL,LL2)
for i, val in enumerate(LL):
    print (i, ",",val)
    if LL[i] == LL2[i]:
        break
    elif LL[i] != LL2[i]:
        target_dir += '/'+LL[2]
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)

#os.replace(ab, "D:/test0002/data2/cdgs/"+new_names)
# python encode.py --dataset data2 --encodings encodings.pickle
