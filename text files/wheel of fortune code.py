from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }
count = 0
roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    df = open('dictionary.txt', 'r')
    dictionary = df.readlines()
    for i in range(len(dictionary)):
        dictionary[i] = str(dictionary[i]).strip().lower()

def readTurnTxtFile():
    global turntext   
    readturntext = open(turntextloc)
    turntext = readturntext.read()
    


def readFinalRoundTxtFile():
    global finalroundtext
    global finalroundloc
    readfinalroundtext = open(finalRoundTextLoc)
    finalroundtext = readfinalroundtext.read()

def readRoundStatusTxtFile():
    global roundstatus
    readroundstatus = open(roundstatusloc)
    roundstatus = readroundstatus.read()
 

def readWheelTxtFile():
    global wheellist
    readwheel = open('wheeldata.txt')
    readwheellines = readwheel.readlines()
    for i in readwheellines:
        wheellist.append(i.rstrip())

def getPlayerInfo():
    global players
    print('Welcome to Wheel of Fortune! Please enter the name of the three players!')
    players[0]["name"] = input('Please enter the name of player 1:')
    players[1]["name"] = input('Please enter the name of player 2:')
    players[2]["name"] = input('Please enter the name of player 3:')


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
    global roundNum
    roundNum = 0
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    roundWord = random.choice(dictionary)
    dictionary.remove(roundWord)
    blankWord = ['_' for i in roundWord]
    return roundWord,blankWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    roundWord, blankWord = getWord()
    for i in range(0,3):
        players[i]["roundtotal"] = 0
    initPlayer = random.randrange(0,3)

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    stillinTurn = True
    wheelland = random.choice(wheellist)
    if wheelland == 'BANKRUPT':
        print(f"The wheel landed on {wheelland}")
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
    # Check for bankrupcy, and take action.
    elif wheelland == 'LOSE A TURN':
        print(f"The wheel landed on {wheelland}")
        stillinTurn = False
    # Check for loose turn
    else:
        while True:
            playerletter = input(f"The wheel landed on {wheelland}, please guess a letter: ")
            if playerletter in vowels:
                print('Sorry, that is not a consonate')
            else: 
                goodGuess, count = guessletter(playerletter, playerNum)
                if goodGuess == False:
                    stillinTurn = False
                    break
                else:
                    players[playerNum]["roundtotal"] += (count * int(wheelland))
                    stillinTurn = True
                    break
   
    # Get amount from wheel if not loose turn or bankruptcy DONE
    # Ask user for letter guess DONE
    # Use guessletter function to see if guess is in word, and return count
    
    # Change player round total if they guess right.     
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global roundWord
    global blankWord
    global count
    # parameters:  take in a letter guess and player number
    if letter in roundWord:
        indexlist = []
        indexlist = [i for i, ltr in enumerate(roundWord) if ltr == letter]
        count = len(indexlist)
        for i in indexlist:
            blankWord[i] = letter
        print(blankWord)
        goodGuess = True
        
    else:
        print(f'Sorry, {letter} was not in the word.')
        goodGuess = False
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess DONE
    # return count of letters in word. 
    # ensure letter is a consonate.
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    if players[playerNum]['roundtotal'] >= 250:
        while True:
            vowelguess = input('Please enter a vowel: ')
            if vowelguess in vowels:
                guessletter(vowelguess, playerNum)
                players[playerNum]['roundtotal'] -=250
            goodGuess = True
            break
    else:
        print('Sorry, you do not have enough money for buying a vowel.')
        goodGuess = True
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    wordguess = input('Please guess the word: ')
    
    # Ask for input of the word and check if it is the same as wordguess
    if wordguess == roundWord:
        blankWord = [char for char in roundWord]
        print(f"That's right! The word was {blankWord}")
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish) 
    else:
        print('Sorry, that was not the word.')
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    print(turntext.format(name = players[playerNum]["name"],money = players[playerNum]["roundtotal"], word = blankWord))
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinTurn = True
    while stillinTurn:
        if '_' not in blankWord:
            stillinTurn = False
            break
        choice = input(f'Please enter S for spin, B for buy a vowel, and G to guess the word')
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundNum
    readRoundStatusTxtFile()
    roundNum = roundNum + 1
    for i in range(0,3):
        players[i]["gametotal"] += players[i]["roundtotal"]
    print(f'This is round Number {roundNum}')
    
    
    initPlayer = wofRoundSetup()
    roundInProgress = True
    while roundInProgress == True:

        if '_' not in blankWord:
            roundInProgress = False
            print(roundstatus.format(name=initPlayer, word= roundWord))
            break
        #Begin the current players turn
        wofTurn(initPlayer)
        initPlayer +=1
        if initPlayer > 2:
            initPlayer = 0
        
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.


    
    

    
    
def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing.
    
    maxamount = max(players[0]['gametotal'], players[1]['gametotal'], players[2]['gametotal'])
    for k,v in players.items():
        if players[k]['gametotal'] == maxamount:
            winplayer = k
    print(finalroundtext.format(name = players[winplayer]["name"],money = players[winplayer]["gametotal"]))
    
    roundWord, blankWord = getWord()
    guessletter('r',winplayer)
    guessletter('s',winplayer)
    guessletter('t',winplayer)
    guessletter('l',winplayer)
    guessletter('n',winplayer)
    guessletter('e',winplayer)
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f'RSTLNE have already been guessed, which leaves you with {blankWord}')
    print('You now get to guess 3 consonates and 1 vowel, and then you will guess the word if you have not gotten it already.')
    print('Please guess 3 more consonates and 1 more vowel')
    guessletter(input('Please guess a consonate'), winplayer)
    guessletter(input('Please guess another consonate'), winplayer)
    guessletter(input('Please guess one final consonate'), winplayer)
    guessletter(input('Please guess a vowel'), winplayer)
    if '_' not in blankWord:
        players[winplayer]['gametotal'] += 100000
        print('Congratulations, you guessed the word correctly')
        print(f"The word was {roundWord}, and {players[winplayer]['name']} has won {players[winplayer]['gametotal']} dollars!")
        
    else:
        print (f'Here is the word after your guessses: {blankWord}')
        guessWord(winplayer)
        if '_' not in blankWord:
            players[winplayer]['gametotal'] += 100000
            print('Congratulations, you guessed the word correctly!')
            print(f"The word was {roundWord}, and {players[winplayer]['name']} has won {players[winplayer]['gametotal']} dollars!")
        # Print out the current blankWord again
        else:
            print(f'Sorry, wrong word. The word was {roundWord}.')
        # Remember guessletter should fill in the letters with the positions in blankWord
        # Get user to guess word
        # If they do, add finalprize and gametotal and print out that the player won 


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()
    
    
if __name__ == "__main__":
    main()
