# Librerías utilizadas para manejo de DataFrames y colorear la consola
import pandas as pd
from termcolor import colored

# Archivos CSV usados para hacer la información persistente
pathBirds = '../knowledge/birds.csv'
pathQuestions = '../knowledge/questions.csv'

# Función del algoritmo para encontrar el ave en base a sus propiedades
def train(questions, birds):
    # Diccionario y sus llaves para concretar la búsqueda de información
    # de forma posiciónal y directa
    birdDict = {}
    answers = {}
    # Se guarda una copia que permitirá manipular la información temporalmente
    # Conservando el original por si se requiere nuevamente cierta información
    birds_copy = birds.copy()
    questions_ids = questions['id'].tolist()
    position = 0
    questions_ids[position] = questions_ids[position]

    # Recorrido de preguntas para obtener propiedades a buscar/añadir
    for question in questions['question'].tolist():
        # Muestra de pregunta y obtención de respuesta de teclado
        print()
        print(colored(question, 'cyan'))
        answer = input(colored('> ', 'grey'))
        answer = answer.upper().replace('Í', 'I')
        
        # Se guardan las respuestas del usuario convertidas a 0 y 1 respectivamente
        # Lo cuál se usará para mostrar el resumen final
        if answer == 'SI':
            property = 1.0
            answers[question] = 'SI'
        else:
            property = 0.0
            answers[question] = 'NO'

        # Recorrido de las aves para hacer la comparación de propiedades
        # Viendo así cuáles son aquellas que cumplen con los requisitos actuales
        for idx in birds_copy.index:
            # Las aves que no cumplan con lo buscado, no serán contempladas en el análisis actual
            if birds_copy[str(questions_ids[position])][idx] != property:
                # En caso de quedar solamente 1 ave, pasar a preguntar si es la que el usuario busca
                if len(birds_copy) == 1 and position < len(questions):
                    print(colored('\nParece que necesitaremos más detalles sobre tu ave.', 'green'))
                    print(colored('Aunque en base al analisis actual...', 'green'))
                    break
                birds_copy.drop(idx, axis=0, inplace=True)
                
        # Guardamos la respuesta del usuario
        birdDict[str(questions_ids[position])] = property

        # Si sólo queda 1 ave en el diccionario, podemos obtener sus propiedades
        if len(birds_copy) == 1:
            print(colored("\n¿El ave en la que piensas es: " + colored(birds_copy["name"].iat[0], 'red') + colored(" ?", 'yellow'), 'yellow'))
            keepPlaying = input("> ")
            keepPlaying = keepPlaying.upper().replace('Í', 'I')
            
            if (keepPlaying == "SI"):
                # Si es el ave que el usuario buscaba y obtenemos el resumen del por qué la elección
                birdProperties(birds_copy, answers)
            else:
                # Seguir buscando el ave sin la opción que no fue la indicada
                # Se elimina el ave que se le mencionó y se realiza mismo proceso con aves restantes
                birds.drop(birds_copy["id"].iat[0], axis=0, inplace=True)
                birds_copy = birds.copy()
        
        position += 1

    # Añadir nueva ave en caso de que no sea la que el usuario busque
    insertNewBird(birds, birdDict, questions)

# Muestra el resumen de lo que se respondió sobre el ave que se decidió
def birdProperties(bird, answers):
    print('\nTu ave es: ', colored(bird["name"].iat[0], 'red'))
    print(colored('\nPorque mencionaste lo siguiente: \n', 'green'))

    for question, answer in answers.items():
        if answer == 'SI':
            print('\t' + colored(question, 'yellow'), '\n', colored('\tSI', 'green'))
        else:
            print('\t' + colored(question, 'yellow'), '\n', colored('\tNO', 'red'))
        
        print()
    quit()

def insertNewBird(birds, birdDict, questions):
    print('\n--------------------------------------------------------------------------------')
    
    # Se le pide nombre y la propiedad extra para añadirla
    print(colored('Tu ave con las propiedades mencionadas, sólo necesitamos algo más...', 'magenta'))
    print(colored('\nIntroduzca el nombre de la ave', 'cyan'))
    birdName = input(colored('> ', 'grey'))
    
    print(colored('\n¿El ave tiene alguna caracteristica distintiva? ' + colored('Introducela a modo de pregunta', 'grey'), 'cyan'))
    question = input(colored('> ', 'grey'))

    # Se sobreescriben los archivos con la información nueva
    birds = pd.read_csv(pathBirds)
    birdDict['id'] = len(birds.values)
    birdDict['name'] = birdName
    birdDict[str(len(birds.columns) - 1)] = 1.0

    tempDict = {
        'id': len(questions) + 1,
        'question': question
    }

    birds = birds.append(birdDict, ignore_index=True)
    birds.to_csv(pathBirds, index=False)

    questions = questions.append(tempDict, ignore_index=True)
    questions.to_csv(pathQuestions, index=False)
    
    # Se le muestra un resumen de cómo fue añadida su ave y con que propiedades
    print('\nTu ave es: ', colored(birdDict["name"], 'red'))
    print(colored('\nFue añadida con las siguientes propiedades: \n', 'green'))

    questionIndex = 0
    q_id = questions['id'].tolist()
    for question in questions['question'].tolist():
        if birdDict[str(q_id[questionIndex])] == 1.0:
            print('\t' + colored(question, 'yellow'), '\n', colored('\tSI', 'green'))
        else:            
            print('\t' + colored(question, 'yellow'), '\n', colored('\tNO', 'red'))
        
        print()
        questionIndex += 1

    quit()

def main():
    questions = pd.read_csv(pathQuestions)
    birds = pd.read_csv(pathBirds)

    questions = questions.sample(frac=1).reset_index(drop=True)

    print(colored('\n*********** Bienvenido al sistema de detección de aves ***********', 'green'))
    print()
    print(colored('\tContestarás algunas preguntas para tratar de describir al ave', 'magenta'))
    print(colored('\tEn cuánto se tenga una posible ave con tu actual descripción', 'magenta'))
    print(colored('\tSe te preguntará si es aquella en la que estás pensando', 'magenta'))
    print(colored('\tY al final se te será mostrada la ave detectada con tus respuestas finales', 'magenta'))
    print(colored('\tEn caso de no ser lo que esperabas o no se encuentre, podrás añadirla (:', 'magenta'))
    print()
    print(colored('**************************  AVENATOR  ****************************', 'blue'))
    print()

    train(questions, birds)

main()