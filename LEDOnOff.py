import cv2
import time
import os
import HandTrackingModule as htm
import paho.mqtt.client as paho


def getConnection():
    client = paho.Client()
    client.connect("broker.mqttdashboard.com", 1883)
    client.loop_start()
    return client


wCam, hCam = 640, 480

pTime, cTime = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector()

client = getConnection()

while True:
    success, img = cap.read()
    detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        if lmList[8][2] < lmList[6][2]:
            client.publish("trpv/led/command", "on", 2)
            cv2.putText(img, "on", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        else:
            client.publish("trpv/led/command", "off", 2)
            cv2.putText(img, "off", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)