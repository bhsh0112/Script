import os

import numpy as np
import cv2

import stroke.find

inPath = "./copybook/"


def getNum1(img, i, j):
    num = -1
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if img[x][y] == 255:
                num += 1
    return num


def getNum2(img, i, j):
    num = 0
    flag = False
    y = j - 2
    for x in range(i - 2, i + 2):
        if img[x][y] == 255:
            if flag == 0:
                num += 1
            flag = True
        else:
            flag = False
    x = i + 2
    for y in range(j - 2, j + 2):
        if img[x][y] == 255:
            if flag == 0:
                num += 1
            flag = True
        else:
            flag = False
    y = j + 2
    for x in range(i + 2, i - 2, -1):
        if img[x][y] == 255:
            if flag == 0:
                num += 1
            flag = True
        else:
            flag = False
    x = i - 2
    for y in range(j + 2, j - 2, -1):
        if img[x][y] == 255:
            if flag == 0:
                num += 1
            flag = True
        else:
            flag = False
    if img[i - 2][j - 2] == 255 and img[i - 2][j - 1] == 255:
        num -= 1
    return num


def pointExist(point, points):
    for p in points:
        if abs(point[0] - p[0]) < 9 and abs(point[1] - p[1]) < 9:
            return True
    return False


def reducePoints(points):
    reduced = []
    for point in points:
        if not pointExist(point, reduced):
            reduced.append(point)
    return reduced


def deburr(points):
    for p1 in points["end"]:
        for p2 in points["inter"]:
            if abs(p1[0] - p2[0]) < 20 and abs(p1[1] - p2[1]) < 20:
                points["end"].remove(p1)
                points["inter"].remove(p2)
    return points


def findPoints(img):
    points = {"end": [], "inter": []}
    for i in range(2, img.shape[0] - 2):
        for j in range(2, img.shape[1] - 2):
            if img[i][j] == 255:
                if getNum1(img, i, j) != 2:
                    num = getNum2(img, i, j)
                    if num < 2:
                        points["end"].append((j, i))
                    elif num > 2:
                        points["inter"].append((j, i))
    points["end"] = reducePoints(points["end"])
    points["inter"] = reducePoints(points["inter"])
    # points = deburr(points)
    return points


def drawPoints(img, points, bgr, radius):
    for point in points:
        cv2.circle(img, point, radius, bgr, -1)
    return img


def drawCntPoints(img, cnts, bgr, radius):
    for cnt in cnts:
        for p in cnt:
            cv2.circle(img, (p[0][0], p[0][1]), radius, bgr, -1)
    return img


def drawStrokes(img, strokes, bgr, radius):
    strokeNum = 1
    for stroke in strokes:
        pointNum = 1
        for point in stroke:
            cv2.circle(img, point, radius, bgr, -1)
            cv2.putText(
                img,
                str(strokeNum) + " " + str(pointNum),
                point,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
            pointNum += 1
        strokeNum += 1
    return img


def get(img):
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((9, 9), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.ximgproc.thinning(img, cv2.ximgproc.THINNING_GUOHALL)

    points = findPoints(img)

    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [
        cv2.approxPolyDP(cnt, 5, True)
        for cnt in contours
        if cv2.arcLength(cnt, True) > 100
    ]

    res = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(res, cnts, -1, (255, 255, 255), 1)
    res = drawCntPoints(res, cnts, (255, 0, 0), 3)
    res = drawPoints(res, points["end"], (0, 255, 0), 3)
    res = drawPoints(res, points["inter"], (0, 0, 255), 3)

    return res


if __name__ == "__main__":

    for filename in os.listdir(inPath):
        src = cv2.imread(inPath + filename, cv2.IMREAD_GRAYSCALE)
        _, img = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((9, 9), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.ximgproc.thinning(img, cv2.ximgproc.THINNING_GUOHALL)

        points = findPoints(img)
        strokes = stroke.find.getStrokes(filename[0:-4], points)

        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = [
            cv2.approxPolyDP(cnt, 5, True)
            for cnt in contours
            if cv2.arcLength(cnt, True) > 100
        ]

        res = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        cv2.drawContours(res, cnts, -1, (255, 255, 255), 1)
        res = drawCntPoints(res, cnts, (255, 0, 0), 3)
        res = drawPoints(res, points["end"], (0, 255, 0), 3)
        res = drawPoints(res, points["inter"], (0, 0, 255), 3)
        if strokes:
            res = drawStrokes(res, strokes, ((0, 0, 255)), 3)

        cv2.imshow("source", src)
        cv2.imshow("image", img)
        cv2.imshow("result", res)
        # cv2.imwrite("./result/" + filename, res)

        key = cv2.waitKey(0)
        if key == ord("q"):
            exit()
