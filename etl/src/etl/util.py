
def readFromFile(fileName):
    lines = []
    with open(fileName, 'r') as file:
        line = file.readline()
        while line:
            line = file.readline()
            lines.append(line)

    return lines
