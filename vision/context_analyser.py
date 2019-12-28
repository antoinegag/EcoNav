import numpy as np
import os
import os.path
import argparse
import logging
from urllib.request import Request, urlopen
import random
import string
import setup_arg
import cv2
from datetime import datetime

# load the stop_sign detector Haar cascade, then detect stop_sign faces
# in the input image
stop_sign_cascade = cv2.CascadeClassifier(
    'cascades/stop_sign_classifier.xml')

if(stop_sign_cascade.empty()):
    logging.critical("Unable to load stop sign classifier")
    exit(-1)

SF = 1.15  # scale factor
N = 6  # minimum neighbours

record = False
save = False
brand = False

start_time = datetime.now().strftime(f"%Y-%m-%d")


def version():
    return "0.1.0-ALPHA (DEV BUILD)"


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def file_timestamp(suffix="recording", extension="mp4"):
    return datetime.now().strftime(f"%Y-%m-%d-%H-%M-%S-{suffix}.{extension}")


def drawDetectedBounds(img, entry, color=(255, 0, 0), thickness=2, index=-1):
    x, y, w, h = entry
    image = cv2.putText(img, "Stop sign", (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2, 8)
    return cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness)


def brandFrame(img):
    height, width, channels = img.shape

    img = cv2.putText(img, "EcoNav " + version(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                      0.5, (0, 0, 255), 1, cv2.LINE_AA)

    img = cv2.putText(img, start_time, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                      0.5, (0, 0, 255), 1, cv2.LINE_AA)

    img = cv2.putText(img, f"Scale factor: {SF}", (10, height - 15), cv2.FONT_HERSHEY_SIMPLEX,
                      0.5, (0, 0, 255), 1, cv2.LINE_AA)
    img = cv2.putText(img, f"Min Neighbors: {N}", (10, height - 40), cv2.FONT_HERSHEY_SIMPLEX,
                      0.5, (0, 0, 255), 1, cv2.LINE_AA)

    return img


def processImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    logging.debug(
        "Detecting stop signs. Scale factor: %d, Min Neighbors: %d", SF, N)

    stop_signs = stop_sign_cascade.detectMultiScale(
        gray, scaleFactor=SF, minNeighbors=N)

    if len(stop_signs) > 0:
        logging.info("Found %d stop signs", len(stop_signs))

    logging.debug("stop signs coordinates:")
    logging.debug(stop_signs)

    # draw a blue rectangle on the image w/ text
    for i, stop_sign in enumerate(stop_signs):
        img = drawDetectedBounds(img, stop_sign, (255, 0, 0))

    if brand:
        img = brandFrame(img)

    return img


args = setup_arg.setup()

cap = cv2.VideoCapture(args["src"])

if not cap.isOpened():
    logging.fatal("Unable to open video")
    exit(-1)

if(args["verbose"]):
    logging.basicConfig(level=logging.INFO)

elif args["debug"]:
    logging.basicConfig(level=logging.DEBUG)

if args["save"] | args["record"]:
    if not os.path.exists(args["outdir"]):
        os.makedirs(args["outdir"])

if args["minneighbors"]:
    N = int(args["minneighbors"])

if args["scalefactor"]:
    SF = float(args["scalefactor"])

logging.info("N: %d, SF: %.2f", N, SF)

if args["brand"]:
    brand = True

id = randomString()
if args["record"]:
    record = True
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    raw_writer = cv2.VideoWriter(
        args["outdir"] + file_timestamp("raw"), fourcc, 24, (640, 480))

if args["save"]:
    save = True
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    processed_writer = cv2.VideoWriter(
        args["outdir"] + file_timestamp("processed"), fourcc, 24, (640, 480))

while cap.isOpened():
    # If frame is available and actual frame
    ret, frame = cap.read()

    if (not args["headless"]) & args["displayraw"]:
        cv2.imshow("Raw", frame)

    if ret:
        if record:
            raw_writer.write(frame)

        processed = processImage(frame)

        if save:
            processed_writer.write(processed)

        if not args["headless"]:
            cv2.imshow("Processed", processed)
            if cv2.waitKey(1) == 27:
                break
    else:
        break

cap.release()

if record:
    raw_writer.release()

if save:
    processed_writer.release()

cv2.destroyAllWindows()
