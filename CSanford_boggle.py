"""
Created by Clay Sanford, Boggle!
As a note, this is probably not optimized, but it ~works~!
"""
from random import sample as samp #Since I only need to use the sample function from the random library, I only import the sample function.
#import socket

class wordsGiven: #Creates a class for the words, to easily check with a built in function!
    def __init__(self):
       self.allWords = []
       self.valScoredWords = [] 
       self.invalScoredWords = []
       self.totalScore = 0
       
    def checkWords(self): #A function to check (and score) all submitted words.
        for word in self.allWords: #For every submitted word
            word = word.lower() #Converts words to lowercase, so that I don't have to worry about cases.
            #print(word) #debug
            if word == 'x': #Included to ignore the cancel character of X, in the event it gets passed here.
                continue
            elif word in self.valScoredWords or word in self.invalScoredWords: #Checks if the word has been scored
                print('The word %s has already been used' % word.upper()) #Prints that the word has been scored
                continue #This is the only function that does not append to the list; it's already there, it doesn't need to be re-added
            elif len(word) < 3: #If the word isn't at least 3 letters long, say it's too short. 
                print('The word %s is too short' %word.upper())
                self.invalScoredWords.append(word)
                continue 
            elif word not in wordList: #If the word isn't in the list supplied, say it is invalid
                print('"%s" is not a word.' %word.upper())
                self.invalScoredWords.append(word)
                continue
            if word not in self.valScoredWords or word not in self.invalScoredWords:
                if 'q' in word:
                    word += 't' #This has to be done in case you try something like "IRAQ", because I'm too lazy to use a try & catch
                    if word[word.index('q')+1] != 'u':
                        word = word[:-1]
                        print('The word %s is not present in the grid.'%word.upper())
                        self.invalScoredWords.append(word)
                        continue
                    else:
                        word = word[:-1]
                        sendWord = word[:(word.index('q')+1)] + word[(word.index('q')+2):]
                        concept = gameBoard.wordInBoard(sendWord.upper()) #Send everything but the u after the word.
                        if concept == 0:
                            print('The word %s is not present in the grid.'%word.upper())
                            self.invalScoredWords.append(word)
                            continue
                        elif concept == 2:
                            print('The word %s is not present without using the same die twice'%word.upper())
                            self.invalScoredWords.append(word)
                            continue
                        
            if (word not in self.valScoredWords or word not in self.invalScoredWords) and 'q' not in word:
                conceptual = gameBoard.wordInBoard(word.upper())
                if conceptual == 0:
                    print('The word %s is not present in the grid.'%word.upper())
                    self.invalScoredWords.append(word)
                    continue       
                if conceptual == 2:
                    print('The word %s is not present without using the same die twice'%word.upper())
                    self.invalScoredWords.append(word)
                    continue
            pts = scoreWord(word)
            self.totalScore += pts
            print('The word %s is worth ' %word.upper() + str(pts) + ' points')
            self.valScoredWords.append(word)
        print('Your total score is ' + str(self.totalScore) + ' points!') #Prints the total counted score.
                
def scoreWord(word): #A function to score every word; this should ONLY be called after passing through every check, as it will score improper words.
    if len(word) < 5:
        return 1 #3 or 4 letters is 1 pt
    if len(word) < 6:
        return 2 #5 letters is 2 pts
    if len(word) < 7:
        return 3 #6 letters is 3 pts
    if len(word) < 8:
        return 5 #7 letters is 5 pts
    return 11 #8+ letters is 11 pts
            

class die: #Creates a class for the dice; dice as a singular is die and I think that's funny
    def __init__(self, sides):
        self.sides = sides #Every dice has 6 sides
        self.shown = None #The rolled side that is currently shown
        self.position = None #The position of the dice on the board (0-15)
        self.relations = [] #The dice touching the die, i.e. die 0 is touching 1 and 4 cardinally and 5 diagonally.
    def roll(self):
        self.shown = str(samp(self.sides, 1)) #Uses the sample function to pick one of the sides
    
class board: #Creates a class for the entire board; This class essentially handles the dice as well
    def __init__(self, allDice): #Created by including all 16 dice
        self.dieList = allDice #Contains a list of all dice
        self.positions = [] #Contains a list of positions of all the dice

    
    def shuffle(self): #A function to shuffle the board
        for dice in self.dieList: #Roll every die
            dice.roll()
        self.positions = samp(self.dieList, 16) #Pick every die location (really creates a random order of the 16 dice)
        die.relations = self.dieRelate() #Finds which dice are touching
       
    def drawBoard(self): #Prints the board to the console
        for i,v in enumerate(self.positions):
            if v.shown != "['Q']":
                print('%s' % str(v.shown).translate({39: None}), end=' ') #I found this translate method to get rid of ' - it seems pretty clever.
                if ((i+1)%4) == 0: #Every 4th die, create a new line.
                    print('\n')
            else:
                print('[Qu]', end=' ') #This has to be done for the way I handled qu in the word itself. I hate q.
                if ((i+1)%4) == 0: #Every 4th die, create a new line.
                    print('\n')

    
    def dieRelate(self): #Because I'm not using a list of 4 lists for my die positions, I need to store their neighbors. This is probably silly, yet it should function.
        for i,v in enumerate(self.positions):
            if i == 0:
                v.position = 0
                v.relations = [1, 4, 5]
            elif i == 1:
                v.position = 1
                v.relations = [0, 2, 4, 5, 6]
            elif i == 2:
                v.position = 2
                v.relations = [1, 3, 5, 6, 7]
            elif i == 3:
                v.position = 3
                v.relations = [2, 6, 7]
            elif i == 4:
                v.position = 4
                v.relations = [0, 1, 5, 8, 9]
            elif i == 5:
                v.position = 5
                v.relations = [0, 1, 2, 4, 6, 8, 9, 10]
            elif i == 6:
                v.position = 6
                v.relations = [1, 2, 3, 5, 7, 9, 10, 11]
            elif i == 7:
                v.position = 7
                v.relations = [2, 3, 6, 10, 11]
            elif i == 8:
                v.position = 8
                v.relations = [4, 5, 9, 12, 13]
            elif i == 9:
                v.position = 9
                v.relations = [4, 5, 6, 8, 10, 12, 13, 14]
            elif i == 10:
                v.position = 10
                v.relations = [5, 6, 7, 9, 11, 13, 14, 15]
            elif i == 11:
                v.position = 11
                v.relations = [6, 7, 10, 14, 15]
            elif i == 12:
                v.position = 12
                v.relations = [8, 9, 13]
            elif i == 13:
                v.position = 13
                v.relations = [8, 9, 10, 12, 14]
            elif i == 14:
               v.position = 14
               v.relations = [9, 10, 11, 13, 15]
            elif i == 15:
                v.position = 15
                v.relations = [10, 11, 14]
    
    def getLetterArray(self, start, char): #Give a die position and the letter you're looking for, returns all dice nearby with that letter
        temp = []
        #print(start) #Debug
        for die in self.positions[start].relations:
            if char == gameBoard.positions[die].shown[2]:
                temp.append(die)
        return temp
        
    def isRelation(self, a, b): #Artifact; give two die positions, returns 1 if they're nearby
        if self.positions[a].position in self.positions[b].relations:
            return 1
        return 0

    def wordInBoard(self, word): #A function to check. Only handles uppercase words. ONLY CALL WITH UPPERCASE WORDS. AND NO QU.
        possiblePaths = []
        for die in self.dieList: #Check what dice match the first letters
            if word[0] == die.shown[2]:
                possiblePaths.append([die.position])
        if possiblePaths == []: #If the first letter isn't present, get return nothing.
            return 0
        #print('Possible starts are: ', end='') #Debug
        #print(possiblePaths)
        nextLayer = []
        tempArray = []
        for i,v in enumerate(word):
            if i == 0:
                continue
            for k,position in enumerate(possiblePaths):
                #print('Starting position is : ',end='') #Debug
                #print(position)
                nextLayer = (self.getLetterArray(position[-1], v))
                if len(nextLayer) == 0:
                    pass
                elif len(nextLayer) == 1:
                    position.append(nextLayer[0])
                else:
                    position.append(nextLayer[-1])
                    for j in range(len(nextLayer)-1):
                        tempArray.append(position.copy())
                        tempArray[-1][-1] = (nextLayer[j])
               # print('Ending position is: ',end='') #Debug
                #print(position)
            for findLetter in tempArray:
                possiblePaths.append(findLetter)
        #Possible paths is now a list of all possible paths for the word
        for attempt in possiblePaths:
            if couldBeWord(attempt, word) and singleCount(attempt):
                return 1
        for attempt in possiblePaths:
            if couldBeWord(attempt, word):
                return 2
        return 0

def couldBeWord(lenCheck, word):    
    if len(lenCheck) == len(word):
        return 1
    return 0

def singleCount(countMe):
    for i in countMe:
        if countMe.count(i) > 1:
            return 0
    return 1

if __name__ == "__main__":
    f = open("words.txt", 'r') #Opens the downloaded words file TODO: Replace this with a socket request
    wordList = f.readlines() #Create a list object for valid words. This is probably stupidly inefficient, but there's nothing ridiculously complex happening, so this /should/ be fine
    for v,x in enumerate(wordList):
        wordList[v] = x[:-1] #Remove "\n" from every entry
        wordList[v] = wordList[v].lower() #Lowercase all words, just to not have to worry about case.
    f.close()
    #Create all 16 dice:
    d1 = die(['A', 'E', 'A', 'N', 'E', 'G'])
    d2 = die(['A', 'H', 'S', 'P', 'C', 'O'])
    d3 = die(['A', 'S', 'P', 'F', 'F', 'K'])
    d4 = die(['O', 'B', 'J', 'O', 'A', 'B'])
    d5 = die(['I', 'O', 'T', 'M', 'U', 'C'])
    d6 = die(['R', 'Y', 'V', 'D', 'E', 'L'])
    d7 = die(['L', 'R', 'E', 'I', 'X', 'D'])
    d8 = die(['E', 'I', 'U', 'N', 'E', 'S'])
    d9 = die(['W', 'N', 'G', 'E', 'E', 'H'])
    d10 = die(['L', 'N', 'H', 'N', 'R', 'Z'])
    d11 = die(['T', 'S', 'T', 'I', 'Y', 'D'])
    d12 = die(['O', 'W', 'T', 'O', 'A', 'T'])
    d13 = die(['E', 'R', 'T', 'T', 'Y', 'L'])
    d14 = die(['T', 'O', 'E', 'S', 'S', 'I'])
    d15 = die(['T', 'E', 'R', 'W', 'H', 'V'])
    d16 = die(['N', 'U', 'I', 'H', 'M', 'Q']) #I have learned to hate the letter Q.
    #Create the board:
    gameBoard = board([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16])
    gameBoard.shuffle() #Shuffle the board
    playerList = wordsGiven() #Create an object for the list of players
    gameBoard.drawBoard() #Print the board to the terminal
    imp = str(input("Start typing your words! (press enter after each word and enter 'X' when done)\n"))
    while imp != 'X' and imp != 'x':
        playerList.allWords.append(imp)    
        imp = str(input())
    print()
    playerList.checkWords()