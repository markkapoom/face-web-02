import numpy
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-y", "--display", type=int, default=1,
                help="whether or not to display output frame to screen")

args = vars(ap.parse_args())
data = pickle.loads(open(args["encodings"], "rb").read())
aaa = ''
cam = cv2.VideoCapture(0)
while True:
    # grab the frame from the threaded video stream
    ret, frame = cam.read()

    # convert the input frame from BGR to RGB then resize it to have
    # a width of 750px (to speedup processing)
    rgb = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb,
                                            model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    per = []
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding, tolerance=0.5)
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
            aaa2 = 0
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
            face_distances = face_recognition.face_distance(data["encodings"], encoding)
            for i, face_distance in enumerate(face_distances):
                if face_distance < 0.6:
                    aaa2 = (1 - face_distance) * 100
                    print(numpy.round(aaa2, 4))
            aaa = "%.2f" % round(aaa2, 2)
        # update the list of names
        per.append(aaa)
        names.append(name)
        # per.append(face_distances)
    # loop over the recognized faces
    for ((top, right, bottom, left), name, aaa) in zip(boxes, names, per):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name + aaa, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    # if the video writer is None *AND* we are supposed to write
    # the output video to disk initialize the writer
    # if writer is None and args["output"] is not None:
    #    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    #    writer = cv2.VideoWriter(args["output"], fourcc, 20,
    #                             (frame.shape[1], frame.shape[0]), True)
    # if the writer is not None, write the frame with recognized
    # faces to disk
    # if writer is not None:
    #    writer.write(frame)
    # the screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()

# check to see if the video writer point needs to be released
# if writer is not None:
# writer.release()
