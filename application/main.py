import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

questions = pd.read_csv("../knowledge/questions.csv")
birds = pd.read_csv("../knowledge/birds.csv")

def learn():
    questions = pd.read_csv("../knowledge/questions.csv")
    birds = pd.read_csv("../knowledge/birds.csv")

    ans = input("¿El ave tiene alguna caracteristica distintiva? \n")

    if (ans == "S"):
        question = input("Introducela a modo de pregunta\n")
        tempDict = {
            'question': question
        }

        questions = questions.append(tempDict, ignore_index=True)
        questions.to_csv("knowledge\\questions2.csv")

        bird = input("Introduzca el nombre de la ave\n")

        birdDict = {
            "name": bird,
            len(birds.columns) - 1: 1
        }

        birds = birds.append(birdDict, ignore_index=True)
        birds.to_csv("knowledge\\birds2.csv")



def evaluate(ans, prop):
    if (ans == "S"):
        ans = 1
    else:
        ans = 0
    
    fil = []

    for i in range(len(birds)):
        #print(birds.loc[i, prop], birds.loc[i, "name"])
        if (birds.loc[i, prop] != ans):
            #print("Es distinto")
            fil.append(i)
            print(i)
            #print("Es igual")
    
    print(fil)
    birds.drop(fil, axis=0, inplace=True)

    if (len(birds) == 1):
        keepPlaying = input("El ave en la que piensas es: " + birds["name"] + "?")
        if (keepPlaying == "S"):
            quit()
        else:
            learn()
            quit()


qList = list(questions["question"])

cols = list(birds.columns)
cols.pop(0)
cols.pop(len(cols)-1)


for q in qList:
    for col in cols:
        ans = input(q + "\n")
        evaluate(ans, col)
        cols.pop(0)
        break


