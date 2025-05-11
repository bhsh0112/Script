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
    temp1 = [points["inter"][0], points["inter"][1]]
    temp1.sort()
    temp2 = [points["inter"][-1], points["inter"][-2]]
    temp2.sort()
    strokes[2].append(temp1[1])
    strokes[2].append(temp2[0])
    strokes[3].append(temp1[0])
    strokes[3].append(temp2[1])
    return strokes
