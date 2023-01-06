stringToMatch1 = 'Tourne gauche de 1 degrees'
stringToMatch2 = 'Avance 1 spaces'
stringToMatch3 = "Tourne droite de 1 degrees"
acceptJustOne = 1
fd = open("turtle", 'r')
with fd as file:
    for line in file:
        line = line.replace("Tourne gauche de ","rt -")
        line = line.replace("Avance","forward")
        line = line.replace("Tourne droite de","rt")
        line = line.replace("degrees","")
        line = line.replace("spaces","")
        line = line.replace("Recule","back")
        text_file = open("newTurtle", "a")
        if (len(line)> 2):
            text_file.write(line)
