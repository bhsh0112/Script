import os

import numpy as np
import cv2

inPath = "./scan/"
outPath = "./char/"


def getRange(position, shape, charWidth, charHeight):
    x1 = 0
    x2 = shape[1]
    y1 = 0
    y2 = shape[0]
    if position[0] - charWidth > 0:
        x1 = position[0] - charWidth
    if position[0] + charWidth < shape[1]:
        x2 = position[0] + charWidth
    if position[1] - charHeight > 0:
        y1 = position[1] - charHeight
    if position[1] + charHeight < shape[0]:
        y2 = position[1] + charHeight
    return x1, x2, y1, y2


def getCorners(cnts):
    corners = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        corners.append([x, y, x + w, y + h])
    return corners


def siftCorners(corners, width, height, centerThr, paddingThr):
    retCorners = []
    for corner in corners:
        rightNum = (
            (corner[0] > paddingThr)
            + (corner[1] > paddingThr)
            + (width - corner[2] > paddingThr)
            + (height - corner[3] > paddingThr)
        )
        if (
            rightNum == 4
            and abs((corner[0] + corner[2]) - width) < centerThr
            and abs((corner[1] + corner[3]) - height) < centerThr
        ):
            retCorners.append(corner)
    return retCorners


def getExtremums(corners):
    extremums = corners[0]
    for corner in corners:
        if corner[0] < extremums[0]:
            extremums[0] = corner[0]
        if corner[1] < extremums[1]:
            extremums[1] = corner[1]
        if corner[2] > extremums[2]:
            extremums[2] = corner[2]
        if corner[3] > extremums[3]:
            extremums[3] = corner[3]
    return extremums


def processExts(extremums, resizeNum, x, y, shape, padding):
    t = extremums[0] + x - padding
    extremums[0] = (t if t > 0 else 0) * resizeNum
    t = extremums[1] + y - padding
    extremums[1] = (t if t > 0 else 0) * resizeNum
    t = extremums[2] + x + padding
    extremums[2] = (t if t < shape[1] else shape[1]) * resizeNum
    t = extremums[3] + y + padding
    extremums[3] = (t if t < shape[0] else shape[0]) * resizeNum
    return extremums


def getRanges(input, resizeNum, positions, charWidth, charHeight):
    ranges = []
    height = int(input.shape[0] / resizeNum)
    width = int(input.shape[1] / resizeNum)
    img = cv2.resize(input, (width, height))
    k1 = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, k1)
    k2 = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k2)
    for position in positions:
        x1, x2, y1, y2 = getRange(position, img.shape, charWidth, charHeight)
        roi = img[y1:y2, x1:x2]
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = [
            cv2.convexHull(cnt) for cnt in contours if cv2.arcLength(cnt, True) > 200
        ]
        corners = getCorners(cnts)
        corners = siftCorners(corners, roi.shape[1], roi.shape[0], 190, 2)
        if not corners:
            continue
        extremums = getExtremums(corners)
        """
        cv2.imshow("morphology", img)
        test = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(test, cnts, -1, (0, 255, 0), 1)
        cv2.rectangle(
            test,
            (extremums[0], extremums[1]),
            (extremums[2], extremums[3]),
            (0, 0, 255),
            1,
        )
        cv2.imshow("range" + str(positions.index(position)), test)
        """
        extremums = processExts(extremums, resizeNum, x1, y1, img.shape, 8)
        ranges.append(extremums)
    return ranges


def drawRanges(img, ranges, bgr):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for range in ranges:
        cv2.rectangle(img, (range[0], range[1]), (range[2], range[3]), bgr, 10)
    return img


def getResizeNum(range, width):
    return width / (((range[0] - range[2]) ** 2 + (range[1] - range[3]) ** 2) ** 0.5)


def getPosition(shape, width):
    x1 = int((width - shape[1]) / 2)
    x2 = x1 + shape[1]
    y1 = int((width - shape[0]) / 2)
    y2 = y1 + shape[0]
    return x1, x2, y1, y2


def cut(img, positions, charWidth, charHeight):
    chars = []
    ranges = getRanges(img, 6, positions, charWidth, charHeight)
    """
    imgRange = drawRanges(img, ranges, (0, 0, 255))
    cv2.imshow(
        "ranges",
        cv2.resize(imgRange, (int(imgRange.shape[1] / 6), int(imgRange.shape[0] / 6))),
    )
    """
    k1 = np.ones((6, 6), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, k1)
    for range in ranges:
        output = np.zeros((512, 512), np.uint8)
        output.fill(255)
        roi = img[range[1] : range[3], range[0] : range[2]]
        resizeNum = getResizeNum(range, output.shape[0])
        roi = cv2.resize(
            roi,
            (int(roi.shape[1] * resizeNum), int(roi.shape[0] * resizeNum)),
        )
        cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            if cv2.arcLength(cnt, True) < 50:
                cv2.drawContours(roi, [cnt], 0, 0, -1)
        x1, x2, y1, y2 = getPosition(roi.shape, output.shape[0])
        output[y1:y2, x1:x2] = 255 - roi
        k2 = np.ones((3, 3), np.uint8)
        output = cv2.erode(output, k2)
        chars.append(output)
    return chars


if __name__ == "__main__":

    charWidth = 110
    charHeight = 150
    positions = [(100, 150), (100, 350), (100, 550), (280, 150), (280, 350), (280, 550)]
    num = 1

    for filename in os.listdir(inPath):
        input = cv2.imread(inPath + filename, cv2.IMREAD_GRAYSCALE)
        ranges = getRanges(input, 6, positions, charWidth, charHeight)

        cv2.imshow(
            "input",
            cv2.resize(input, (int(input.shape[1] / 6), int(input.shape[0] / 6))),
        )
        imgRange = drawRanges(input, ranges, (0, 0, 255))
        cv2.imshow(
            "ranges",
            cv2.resize(
                imgRange, (int(imgRange.shape[1] / 6), int(imgRange.shape[0] / 6))
            ),
        )

        k1 = np.ones((6, 6), np.uint8)
        img = cv2.morphologyEx(input, cv2.MORPH_OPEN, k1)
        output = np.zeros((512, 512), np.uint8)
        for range in ranges:
            output.fill(255)
            roi = img[range[1] : range[3], range[0] : range[2]]
            resizeNum = getResizeNum(range, output.shape[0])
            roi = cv2.resize(
                roi,
                (int(roi.shape[1] * resizeNum), int(roi.shape[0] * resizeNum)),
            )
            cnts, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in cnts:
                if cv2.arcLength(cnt, True) < 50:
                    cv2.drawContours(roi, [cnt], 0, 0, -1)
            x1, x2, y1, y2 = getPosition(roi.shape, output.shape[0])
            output[y1:y2, x1:x2] = 255 - roi
            k2 = np.ones((3, 3), np.uint8)
            output = cv2.erode(output, k2)
            cv2.imshow("output", output)
            key = cv2.waitKey(0)
            if key == ord("q"):
                exit()
            elif key == ord("b"):
                break
            elif key == ord("s"):
                cv2.imwrite(outPath + str(num) + ".jpg", output)
                num += 1
