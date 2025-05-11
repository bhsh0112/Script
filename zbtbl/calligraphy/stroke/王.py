def getStrokes(points):
    points["end"].sort(key=lambda x: x[1])
    points["inter"].sort(key=lambda x: x[1])
    strokes = [[], [], [], []]
    strokes[0].append(points["end"][0])
    strokes[0].append(points["end"][1])
    strokes[0].sort()
    strokes[1].append(points["end"][2])
    strokes[1].append(points["end"][3])
    strokes[1].sort()
    strokes[2].append(points["end"][4])
    strokes[2].append(points["end"][5])
    strokes[2].sort()
    strokes[3].append(points["inter"][0])
    strokes[3].append(points["inter"][2])
    return strokes
