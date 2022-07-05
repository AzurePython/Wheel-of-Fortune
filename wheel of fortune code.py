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

#reads in dictionary file and appends values to the dictionary list
def readDictionaryFile():
    global dictionary
    df = open('dictionary.txt', 'r')
    dictionary = df.readlines()
    for i in range(len(dictionary)):
        dictionary[i] = str(dictionary[i]).strip().lower()

#reads in the turn text file
def readTurnTxtFile():
    global turntext   
    readturntext = open(turntextloc)
    turntext = readturntext.read()
    

#reads in the final round text file
def readFinalRoundTxtFile():
    global finalroundtext
    global finalroundloc
    readfinalroundtext = open(finalRoundTextLoc)
    finalroundtext = readfinalroundtext.read()

#reads in the round status text file         
def readRoundStatusTxtFile():
    global roundstatus
    readroundstatus = open(roundstatusloc)
    roundstatus = readroundstatus.read()
 
#reads in the wheel text file and appends values to wheellist
def readWheelTxtFile():
    global wheellist
    readwheel = open('wheeldata.txt')
    readwheellines = readwheel.readlines()
    for i in readwheellines:
        wheellist.append(i.rstrip())

#gets names of players
def getPlayerInfo():
    global players
    print('Welcome to Wheel of Fortune! Please enter the name of the three players!')
    players[0]["name"] = input('Please enter the name of player 1:')
    players[1]["name"] = input('Please enter the name of player 2:')
    players[2]["name"] = input('Please enter the name of player 3:')

#sets up game by runnning basic functions
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

#gets a random word from dictionary, and creates a list of underscores that is the same length as the word       
def getWord():
    global dictionary
    roundWord = random.choice(dictionary)
    dictionary.remove(roundWord)
    blankWord = ['_' for i in roundWord]
    return roundWord,blankWord

#sets up the round, getting the word and blankword and setting the players round total to 0, and getting a random player num
def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    roundWord, blankWord = getWord()
    for i in range(0,3):
        players[i]["roundtotal"] = 0
    initPlayer = random.randrange(0,3)

    return initPlayer

#gets a random item from wheellist, checks for bankrupt and lose turn (returning turn false if so). Checks if letter in turn
#and if it is, adds money to player round and returns stillinturn = true
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


#checks to see if letter is in word and populates blankWord with the letter. Returns goodguess True if it is, False if it is not
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
    
    return goodGuess, count

#checks to see if thhey have enough money to buy a vowel, and if the letter is a vowel, then uses guessletter and
#subtracts 250 dollars from round total
def buyVowel(playerNum):
    global players
    global vowels
    
 
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
    
    return goodGuess      

#asks for a word, then checks if that is the same as the roundword. If it is, populates blankword with the word
#otherwise lets them know that it was not the word. Returns false either way, because turn is over no matter what.
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord

    wordguess = input('Please guess the word: ')
    
    if wordguess == roundWord:
        blankWord = [char for char in roundWord]
        print(f"That's right! The word was {blankWord}")
    else:
        print('Sorry, that was not the word.')
    
    return False
    
#Prints turn text, and gives user a menu while they are still in turn    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    print(turntext.format(name = players[playerNum]["name"],money = players[playerNum]["roundtotal"], word = blankWord))
    
    stillinTurn = True
    while stillinTurn:
        if '_' not in blankWord:
            stillinTurn = False
            break
        choice = input(f'Please enter S for spin, B for buy a vowel, and G to guess the word')
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
  

#Put players game total = to round total, prints round status and iterates through the players until the round is over
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


    
    

    
#Finds the player with the most winnings, prints the final round text file, uses guessletter to find rstlne in the new word,
# asks player for three consonates and vowel, and then checks those using guess letter. Finallyy asks user to guess the word
# and prints a final message of their total winnings if they guess the word correctly. Otherwise lets them know it was wrong.
def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    
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
        else:
            print(f'Sorry, wrong word. The word was {roundWord}.')


#Runs game setup, then iterates through two rounds, and then finally the final round.
def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()
    
#Starts the game    
if __name__ == "__main__":
    main()
