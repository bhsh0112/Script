import os

import numpy as np
import cv2

inPath = "./photo/"
outPath = "./scan/"


def realContour(cnt, shape, padding):
    x, y, w, h = cv2.boundingRect(cnt)
    x += w / 2
    y += h / 2
    if (
        x < padding
        or shape[1] - x < padding
        or y < padding
        or shape[0] - y < padding
        or w < shape[1] / 2
        or h < shape[0] / 2
    ):
        return False
    else:
        return True


def findMaxContour(contours, shape):
    lengths = []
    for cnt in contours:
        lengths.append(cv2.arcLength(cnt, True))
    lengths.sort()
    for length in lengths:
        index = lengths.index(length)
        if realContour(contours[index], shape, 50):
            return index
    return -1


def lineCategory(x1, y1, x2, y2, width, height):
    xMid = width / 2
    yMid = height / 2
    if x1 < xMid and y1 < yMid:
        if x2 > xMid and y2 < yMid:
            return 0
        elif x2 < xMid and y2 > yMid:
            return 1
        else:
            return -1
    elif x1 < xMid and y1 > yMid:
        if x2 < xMid and y2 < yMid:
            return 1
        elif x2 > xMid and y2 > yMid:
            return 2
        else:
            return -1
    elif x1 > xMid and y1 > yMid:
        if x2 < xMid and y2 > yMid:
            return 2
        elif x2 > xMid and y2 < yMid:
            return 3
        else:
            return -1
    elif x1 > xMid and y1 < yMid:
        if x2 > xMid and y2 > yMid:
            return 3
        elif x2 < xMid and y2 < yMid:
            return 0
        else:
            return -1
    else:
        return -1


def getInter(l1, l2):
    x1 = l1[0]
    y1 = l1[1]
    x2 = l1[2]
    y2 = l1[3]
    x3 = l2[0]
    y3 = l2[1]
    x4 = l2[2]
    y4 = l2[3]
    x = int(
        ((x3 - x4) * (x2 * y1 - x1 * y2) - (x1 - x2) * (x4 * y3 - x3 * y4))
        / ((x3 - x4) * (y1 - y2) - (x1 - x2) * (y3 - y4))
    )
    y = int(
        ((y3 - y4) * (y2 * x1 - y1 * x2) - (y1 - y2) * (y4 * x3 - y3 * x4))
        / ((y3 - y4) * (x1 - x2) - (y1 - y2) * (x3 - x4))
    )
    return [x, y]


def pointsPadding(points, padding):
    points[0][0] += padding
    points[0][1] -= padding
    points[1][0] -= padding
    points[1][1] -= padding
    points[2][0] -= padding
    points[2][1] += padding
    points[3][0] += padding
    points[3][1] += padding
    return points


def getPoints(img, resizeNum):
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.Canny(img, 50, 150)
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return
    index = findMaxContour(contours, img.shape)
    if index == -1:
        return
    cnt = contours[index]
    img.fill(0)
    cv2.drawContours(img, [cnt], 0, 255, 1)
    """
    test = np.zeros(img.shape, np.uint8)
    cv2.drawContours(test, contours, -1, 255, 1)
    cv2.imshow("cnts", test)
    cv2.imshow("cnt", img)
    """
    lines = cv2.HoughLinesP(img, 1, 0.01, 20, minLineLength=100, maxLineGap=50)
    if lines is None or not lines.any():
        return
    edges = [[], [], [], []]
    for line in lines:
        x1, y1, x2, y2 = line[0]
        category = lineCategory(x1, y1, x2, y2, img.shape[1], img.shape[0])
        if category != -1:
            edges[category].append([x1, y1, x2, y2])
    if not edges[0] or not edges[1] or not edges[2] or not edges[3]:
        return
    points = []
    for i in range(4):
        points.append(getInter(edges[i - 1][0], edges[i][0]))
    points = pointsPadding(points, 2)
    points = [[i * resizeNum for i in point] for point in points]
    return points


def getDistance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def warp(input, points):
    height = input.shape[0]
    width = int(
        height
        * (getDistance(points[0], points[1]) + getDistance(points[2], points[3]))
        / (getDistance(points[1], points[2]) + getDistance(points[3], points[0]))
    )
    src = np.float32(points)
    tgt = np.float32([[width, 0], [0, 0], [0, height], [width, height]])
    M = cv2.getPerspectiveTransform(src, tgt)
    output = cv2.warpPerspective(input, M, (width, height))
    return output


def scan(src):
    resizeNum = int(src.shape[0] / 300) + 1
    height = int(src.shape[0] / resizeNum)
    width = int(src.shape[1] / resizeNum)
    img = cv2.resize(src, (width, height))
    points = getPoints(img, resizeNum)
    if points is not None:
        output = warp(src, points)
        """
        edges = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        for i in range(4):
            cv2.line(edges, points[i - 1], points[i], (0, 0, 255), 10)
        cv2.imshow(
            "edges",
            cv2.resize(edges, (int(edges.shape[1] / 6), int(edges.shape[0] / 6))),
        )
        """
        thresh = cv2.mean(output)[0] + 30
        _, output = cv2.threshold(output, thresh, 255, cv2.THRESH_BINARY)
        return True, output
    else:
        return False, None


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    num = 1

    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        while True:
            _, frame = cap.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            resizeNum = int(frame.shape[1] / 300) + 1
            height = int(frame.shape[0] / resizeNum)
            width = int(frame.shape[1] / resizeNum)
            img = cv2.resize(frame, (width, height))
            grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pointsTemp = getPoints(grayImg, resizeNum)
            if pointsTemp is not None:
                points = pointsTemp
                for i in range(4):
                    cv2.line(frame, points[i - 1], points[i], (0, 0, 255), 3)
            cv2.imshow(
                "frame",
                cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))),
            )
            key = cv2.waitKey(100)
            if key == ord("s"):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                output = warp(gray, points)
                thresh = cv2.mean(output)[0] + 30
                _, output = cv2.threshold(output, thresh, 255, cv2.THRESH_BINARY)
                cv2.imwrite(outPath + str(num) + ".jpg", output)
                print("write success " + str(num))
                num += 1
            elif key == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    else:
        for filename in os.listdir(inPath):
            src = cv2.imread(inPath + filename, cv2.IMREAD_GRAYSCALE)
            ret, res = scan(src)
            if ret == False:
                continue
            cv2.imshow(
                "result",
                cv2.resize(res, (int(res.shape[1] / 6), int(res.shape[0] / 6))),
            )
            key = cv2.waitKey(0)
            if key == ord("q"):
                exit()
            elif key == ord("s"):
                cv2.imwrite(outPath + str(num) + ".jpg", res)
                num += 1
