import tkinter as tk
from tkinter.ttk import *
from ctypes import *
from functools import partial
from tkinter.constants import END
from PIL import Image, ImageTk

mainc = cdll.LoadLibrary('code/C/libmain.dll')
root = tk.Tk()

GameType = {'people': 0, 'computer': 1}
Colors = ['tomato', 'gold2', 'lime green', 'deep sky blue', 'colored']
ReferenceColors = ['red', 'yellow', 'green', 'blue', 'colored']
CardType = ['number', 'skip', 'reverse', 'draw', 'wild']


class Home():
    def __init__(self):
        self.windowGeometry()
        self.windowConfig()
        self.startGameButton()
        self.gameSettingsInput()
        self.allWindgets = [self.btnStartGame,
                            self.frameNumberOfPlayers, self.frameTypeOfGame]
        self.warningWindgets = list()
        root.update()
        pass

    def windowGeometry(self):
        self.win_x, self.win_y = 1100, 600
        self.x_screen = int(root.winfo_screenwidth()/2 - self.win_x/2)
        self.y_screen = int(root.winfo_screenheight()/2 - self.win_y/2)

    def windowConfig(self):
        root.geometry(
            f'{self.win_x}x{self.win_y}+{self.x_screen}+{self.y_screen}')
        root.minsize(width=self.win_x, height=self.win_y)
        root.title('Uno Game')
        root.bind('<Key>', self.keyFunctions)

    def startGameButton(self):
        self.btnStartGame = tk.Button(root, text='Start Game')
        self.btnStartGame.pack(side='bottom', pady=25)
        self.btnStartGame.bind('<Button-1>', self.startGame)

    def gameSettingsInput(self):
        self.vcmd = (root.register(self.validateInputToNumber), '%P')
        self.frameNumberOfPlayers = tk.Frame(root, name='numberOfPlayers')
        self.frameNumberOfPlayers.pack(side='top', pady=25)

        self.labelNumberOfPlayers = tk.Label(
            self.frameNumberOfPlayers, text='Number of Players')
        self.labelNumberOfPlayers.pack(side='top')
        self.entryNumberOfPlayers = tk.Entry(
            self.frameNumberOfPlayers, width=10, validate='all', validatecommand=self.vcmd)
        self.entryNumberOfPlayers.pack(side='top')

        self.frameTypeOfGame = tk.Frame(root, name='typeOfGame')
        self.frameTypeOfGame.pack(side='top')

        self.labelTypeOfGame = tk.Label(
            self.frameTypeOfGame, text='Type of Game')
        self.labelTypeOfGame.pack(side='top')
        self.choicesTypeOfGame = ['people', 'computer']
        self.comboBoxTypeOfGame = Combobox(
            self.frameTypeOfGame, width=10, values=self.choicesTypeOfGame, state='readonly')
        self.comboBoxTypeOfGame.pack(side='top')

    def validateInputToNumber(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False

    def keyFunctions(self, event):
        pass

    def startGame(self, event):
        global gameWindow
        for windgets in self.warningWindgets:
            windgets.destroy()
        try:
            numberOfPlayers = int(self.entryNumberOfPlayers.get())
            if numberOfPlayers < 2 or numberOfPlayers > 14:
                self.checkNumberOfPlayers()
                return None
            typeOfGame = GameType[self.comboBoxTypeOfGame.get()]
            mainc.gameSettings(numberOfPlayers, typeOfGame)
            mainc.main()
            for windget in self.allWindgets:
                windget.destroy()
            gameWindow = Game()
        except:
            self.checkInputsToStartGame()
            pass

    def checkNumberOfPlayers(self):
        self.labelPopUpNumberOfPlayers = tk.Label(
            self.frameNumberOfPlayers, text='Necessário 2 ou mais jogadores\n(máximo: 15)', fg='red')
        self.labelPopUpNumberOfPlayers.pack(side='bottom')
        self.warningWindgets.append(self.labelPopUpNumberOfPlayers)

    def checkInputsToStartGame(self):
        self.labelPopUpInputs = tk.Label(
            self.frameTypeOfGame, text='Verifique as informações', fg='red')
        self.labelPopUpInputs.pack(side='bottom')
        self.warningWindgets.append(self.labelPopUpInputs)


class Game():
    def __init__(self):
        self.currentPlayer = 0
        self.playersButtons = list()
        self.createDeckButton()
        self.createPlayerButtons()
        self.initializeGame(0)
        pass

    def createDeckButton(self):
        self.frameDeckButton = tk.Frame(root, name='deckBtnShow')
        self.frameDeckButton.pack(anchor='nw', padx=5, pady=5)

        self.deckButton = tk.Button(
            self.frameDeckButton, text='Show deck', height=2)
        self.deckButton.configure(relief='groove')
        self.deckButton['command'] = mainc.pyPrintDeck
        self.deckButton.pack()

    def createPlayerButtons(self):
        self.framePlayerHandsTop = tk.Frame(root, name='playerHandsTop')
        self.framePlayerHandsTop.pack(side='top')

        self.framePlayerHandsBot = tk.Frame(root, name='playerHandsBot')
        self.framePlayerHandsBot.pack(side='top', pady=25)

        for player in range(mainc.getNumberOfPlayers()):
            frame = self.framePlayerHandsTop if player < 8 else self.framePlayerHandsBot
            self.buttonPlayerAction = tk.Button(frame, name=f"player{player}", text=f"Player {player + 1}")
            self.buttonPlayerAction.configure(relief='ridge')
            self.buttonPlayerAction.pack(side='left', padx=15)
            self.buttonPlayerAction['command'] = partial(self.printAllCardsInHand, player)
            self.playersButtons.append(self.buttonPlayerAction)
            if player == self.currentPlayer:
                self.buttonPlayerAction['state'] = 'normal'
            else:
                self.buttonPlayerAction['state'] = 'disable'

    def makeCardText(self, eachCardNumber, eachCardType):
        if eachCardType in ['wild', 'draw'] and eachCardNumber > 0:
            eachCardText = f'+{eachCardNumber} {eachCardType}'
        elif eachCardType in ['reverse', 'skip']:
            eachCardText = f'{eachCardType}'
        else:
            eachCardText = f'{eachCardNumber}'
        return eachCardText

    def printAllCardsInHand(self, ownerIndex):
        self.cardsFromPerson = list()

        self.playerCards = tk.Toplevel(root)
        self.playerCards.attributes('-topmost', 'true')
        self.playerCards.geometry(f'+{root.winfo_x()}+{root.winfo_y()}')

        labelPlayerNumber = tk.Label(self.playerCards, text=f"Player {ownerIndex + 1}")
        labelPlayerNumber.pack()

        for cardIndex in range(mainc.getNumberOfCardsInHand(ownerIndex)):
            eachCardType = CardType[mainc.getCardType(ownerIndex, cardIndex)]
            eachCardNumber = mainc.getCardNumber(ownerIndex, cardIndex)

            eachCardColor = f'{Colors[mainc.getCardColor(ownerIndex, cardIndex)]}'
            eachCardReferenceColor = f'{ReferenceColors[mainc.getCardColor(ownerIndex, cardIndex)]}'
            if eachCardColor == 'colored':
                eachCardColor = 'white'

            self.eachCardImg = Image.open(
                f'images/{eachCardNumber}-{eachCardType}.png').resize((99, 150))
            self.eachCardImg = ImageTk.PhotoImage(self.eachCardImg)
            self.cardsFromPerson.append(self.eachCardImg)

            eachBtn = tk.Button(self.playerCards, background=eachCardColor, activebackground=eachCardColor,
                                image=self.cardsFromPerson[cardIndex], borderwidth=-8, relief='flat')
            eachBtn.pack(pady=5, padx=10, side='left')
            eachBtn['command'] = partial(self.nextPlayer, ownerIndex, eachCardType, eachCardNumber, eachCardReferenceColor)

    def initializeGame(self, cardIndex):
        self.frameCardsInGame = tk.Frame(root, name='frameCardsInGame')
        self.frameCardsInGame.pack(anchor='center')

        eachCardType = CardType[mainc.getCardTypeFromDeck(cardIndex)]
        eachCardNumber = mainc.getCardNumberFromDeck(cardIndex)

        cardInTopColor = f'{Colors[mainc.getCardColorFromDeck(cardIndex)]}'
        if cardInTopColor == 'colored':
            cardInTopColor = 'white'

        self.cardInTopImg = Image.open(
            f'images/{eachCardNumber}-{eachCardType}.png').resize((99, 150))
        self.cardInTopImg = ImageTk.PhotoImage(self.cardInTopImg)

        self.labelCardInTop = tk.Label(self.frameCardsInGame, image=self.cardInTopImg,
                                       name='cardInTop', background=cardInTopColor, borderwidth=-5)
        self.labelCardInTop.pack(anchor='center')
    
    def nextPlayer(self, ownerIndex, eachCardType, eachCardNumber, eachCardReferenceColor):
        self.currentPlayer += 1
        if self.currentPlayer == mainc.getNumberOfPlayers():
            self.currentPlayer = 0
        self.playersButtons[ownerIndex]['state'] = 'disable'
        self.playersButtons[self.currentPlayer]['state'] = 'normal'
        print(eachCardNumber, eachCardReferenceColor, eachCardType)
        self.playerCards.destroy()

home = Home()
root.mainloop()
