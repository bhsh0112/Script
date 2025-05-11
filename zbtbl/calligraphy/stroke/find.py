import importlib


def getStrokes(charName, points):
    try:
        char = importlib.import_module("stroke." + charName)
        return char.getStrokes(points)
    except:
        return None
