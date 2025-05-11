import os

import cv2

import scan
import cut
import get

photoPath = "./photo/"
scanPath = "./scan/"
charPath = "./char/"

charWidth = 110
charHeight = 150
positions = [(100, 150), (100, 350), (100, 550), (280, 150), (280, 350), (280, 550)]

scanNum = 1
charNum = 1

for filename in os.listdir(photoPath):
    inputImg = cv2.imread(photoPath + filename)
    cv2.imshow(
        "input",
        cv2.resize(inputImg, (int(inputImg.shape[1] / 6), int(inputImg.shape[0] / 6))),
    )
    grayImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)
    ret, scanImg = scan.scan(grayImg)
    if ret == False:
        continue
    cv2.imshow("scan", scanImg)
    cv2.imshow(
        "scan",
        cv2.resize(scanImg, (int(scanImg.shape[1] / 6), int(scanImg.shape[0] / 6))),
    )
    key = cv2.waitKey(0)
    if key == ord("q"):
        exit()
    elif key == ord("c"):
        continue
    elif key == ord("s"):
        cv2.imwrite(scanPath + str(scanNum) + ".jpg", scanImg)
        scanNum += 1
    charImgs = cut.cut(scanImg, positions, charWidth, charHeight)
    for charImg in charImgs:
        cv2.imshow("char", charImg)
        key = cv2.waitKey(0)
        if key == ord("q"):
            exit()
        elif key == ord("c"):
            continue
        elif key == ord("s"):
            cv2.imwrite(charPath + str(charNum) + ".jpg", charImg)
            charNum += 1
        getImg = get.get(charImg)
        cv2.imshow("get", getImg)
