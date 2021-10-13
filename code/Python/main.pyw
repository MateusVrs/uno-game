import tkinter as tk
from tkinter.ttk import *
from ctypes import *
from functools import partial
from tkinter.constants import END
from PIL import Image, ImageTk
from math import ceil, floor

mainc = cdll.LoadLibrary('code/C/libmain.so')
root = tk.Tk()

GameType = {'pessoas': 0}
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

    def windowGeometry(self):
        self.win_x, self.win_y = 1100, 450
        self.x_screen = int(root.winfo_screenwidth()/2 - self.win_x/2)
        self.y_screen = int(50)

    def windowConfig(self):
        root.geometry(
            f'{self.win_x}x{self.win_y}+{self.x_screen}+{self.y_screen}')
        root.minsize(width=self.win_x, height=self.win_y)
        root.title('Uno Game')
        root.bind('<Key>', self.keyFunctions)

    def startGameButton(self):
        self.btnStartGame = tk.Button(root, text='Começar Jogo')
        self.btnStartGame.pack(side='bottom', pady=25)
        self.btnStartGame.bind('<Button-1>', self.startGame)

    def gameSettingsInput(self):
        self.vcmd = (root.register(self.validateInputToNumber), '%P')
        self.frameNumberOfPlayers = tk.Frame(root, name='numberOfPlayers')
        self.frameNumberOfPlayers.pack(side='top', pady=25)

        self.labelNumberOfPlayers = tk.Label(
            self.frameNumberOfPlayers, text='Número de Jogadores')
        self.labelNumberOfPlayers.pack(side='top')
        self.entryNumberOfPlayers = tk.Entry(
            self.frameNumberOfPlayers, width=10, validate='all', validatecommand=self.vcmd)
        self.entryNumberOfPlayers.pack(side='top')

        self.frameTypeOfGame = tk.Frame(root, name='typeOfGame')
        self.frameTypeOfGame.pack(side='top')

        self.labelTypeOfGame = tk.Label(
            self.frameTypeOfGame, text='Tipo de Jogo')
        self.labelTypeOfGame.pack(side='top')
        self.choicesTypeOfGame = list(GameType.keys())
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

    def checkNumberOfPlayers(self):
        self.labelPopUpNumberOfPlayers = tk.Label(
            self.frameNumberOfPlayers, text='Necessário 2 ou mais jogadores\n(máximo: 14)', fg='red')
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
        self.currentCardInGame = 0
        self.toggleSignal = 1
        self.isGameOrdered = True
        self.isHandActive = False
        self.playersButtons = list()
        self.createPlayerButtons()
        self.addCardToGame(self.currentCardInGame)

    def createPlayerButtons(self):
        self.framePlayerHands = tk.Frame(root, name='playerHandsTop')
        self.framePlayerHands.pack(side='top')

        for player in range(mainc.getNumberOfPlayers()):
            self.buttonPlayerAction = tk.Button(
                self.framePlayerHands, name=f"player{player}", text=f"Jogador {player + 1}")
            self.buttonPlayerAction.configure(relief='ridge')
            self.buttonPlayerAction.grid(
                column=player % 7, row=0 if player < 7 else 1, padx=15, pady=25)
            self.buttonPlayerAction['command'] = partial(
                self.printAllCardsInHand, player)
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

    def createHandTopLevel(self):
        self.playerCards = tk.Toplevel(root, name='playerTopLevel')
        self.playerCards.bind('<Destroy>', self.deleteHandToLevel)
        self.playerCards.attributes('-topmost', 'true')
        self.playerCards.withdraw()
        self.isHandActive = True

    def deleteHandToLevel(self, event):
        try:
            del self.playerCards
            self.isHandActive = False
        except:
            pass

    def printAllCardsInHand(self, ownerIndex):
        if not self.isHandActive:
            self.currentPage = 1
            self.currentPlayer = ownerIndex
            self.buttonsFromPerson = list()
            self.cardsFromPersonImg = list()
            self.cardsFromPerson = list()

            self.createHandTopLevel()

            labelPlayerNumber = tk.Label(
                self.playerCards, text=f"Jogador {ownerIndex + 1}")
            labelPlayerNumber.pack(anchor='n', pady=10)

            frameCards = tk.Frame(
                self.playerCards, name='frameCardsFromPlayer')
            frameCards.pack(anchor='center', pady=10)

            self.framePlayerButtons = tk.Frame(
                self.playerCards, name='framePlayerButtons')
            self.framePlayerButtons.pack(anchor='s')

            for cardIndex in range(mainc.getNumberOfCardsInHand(ownerIndex)):
                eachCardType = CardType[mainc.getCardType(
                    ownerIndex, cardIndex)]
                eachCardNumber = mainc.getCardNumber(ownerIndex, cardIndex)

                eachCardColor = f'{Colors[mainc.getCardColor(ownerIndex, cardIndex)]}'
                eachCardReferenceColor = f'{ReferenceColors[mainc.getCardColor(ownerIndex, cardIndex)]}'
                if eachCardColor == 'colored':
                    eachCardColor = 'white'

                self.createCardBtn(ownerIndex, frameCards, cardIndex, eachCardType,
                                   eachCardNumber, eachCardColor, eachCardReferenceColor)

            self.showPlayerCards()

            nextPageButton = tk.Button(
                self.framePlayerButtons, text='Próxima página', width=15)
            nextPageButton['command'] = partial(self.nextPage, ownerIndex)
            nextPageButton.pack(side='right', padx=15)

            skipButton = tk.Button(
                self.framePlayerButtons, text='Pular vez', width=15)
            skipButton['command'] = partial(self.skipPlayer, ownerIndex)
            skipButton.pack(side='right', padx=5)
            self.buttonsFromPerson.append(skipButton)
            skipButton['state'] = 'disable'

            previousPageButton = tk.Button(
                self.framePlayerButtons, text='Página anterior', width=15)
            previousPageButton['command'] = partial(self.previousPage)
            previousPageButton.pack(side='left', padx=15)

            drawButton = tk.Button(
                self.framePlayerButtons, text='Comprar carta', width=15)
            drawButton['command'] = partial(
                self.drawCard, ownerIndex, frameCards, skipButton)
            self.buttonsFromPerson.append(drawButton)
            drawButton.pack(side='left', padx=5)

            self.playerCards.update()
            self.playerCards.geometry(
                f'{root.winfo_width()}x{320}+{int(root.winfo_x())}+{int(root.winfo_y() + root.winfo_height() - 150)}')
            self.playerCards.resizable(False, False)
            self.playerCards.deiconify()

    def disablePersonBtn(self):
        for btn in self.buttonsFromPerson:
            btn['state'] = 'disable'

    def clearCurrentCards(self):
        for index in range((self.currentPage-1)*7, self.currentPage*7):
            try:
                self.cardsFromPerson[index].grid_remove()
            except:
                break

    def disableCards(self):
        for card in self.cardsFromPerson:
            card['state'] = 'disable'

    def showPlayerCards(self):
        for index in range((self.currentPage-1)*7, self.currentPage*7):
            try:
                self.cardsFromPerson[index].grid()
            except:
                break

    def nextPage(self, ownerIndex):
        numberOfCards = mainc.getNumberOfCardsInHand(ownerIndex)
        if self.currentPage + 1 <= ceil(numberOfCards/7):
            self.clearCurrentCards()
            self.currentPage += 1
            self.showPlayerCards()

    def previousPage(self):
        if self.currentPage - 1 > 0:
            self.clearCurrentCards()
            self.currentPage -= 1
            self.showPlayerCards()

    def createCardBtn(self, ownerIndex, frameCards, cardIndex, eachCardType, eachCardNumber, eachCardColor, eachCardReferenceColor):
        eachCardImg = Image.open(
            f'images/{eachCardNumber}-{eachCardType}.png').resize((99, 150))
        eachCardImg = ImageTk.PhotoImage(eachCardImg)
        self.cardsFromPersonImg.append(eachCardImg)

        eachBtn = tk.Button(frameCards, background=eachCardColor, activebackground=eachCardColor,
                            image=self.cardsFromPersonImg[cardIndex], borderwidth=-8, relief='flat')
        eachBtn.grid(column=cardIndex % 7, row=0, padx=5, pady=5)
        eachBtn['command'] = partial(
            self.nextPlayer, ownerIndex, cardIndex, eachCardType, eachCardNumber, eachCardReferenceColor)
        self.cardsFromPerson.append(eachBtn)
        eachBtn.grid_remove()

    def drawCard(self, ownerIndex, frameCards, skipButton):
        mainc.drawCard(ownerIndex)

        cardIndex = mainc.getNumberOfCardsInHand(ownerIndex) - 1
        eachCardType = CardType[mainc.getCardType(ownerIndex, cardIndex)]
        eachCardNumber = mainc.getCardNumber(ownerIndex, cardIndex)

        eachCardColor = f'{Colors[mainc.getCardColor(ownerIndex, cardIndex)]}'
        eachCardReferenceColor = f'{ReferenceColors[mainc.getCardColor(ownerIndex, cardIndex)]}'
        if eachCardColor == 'colored':
            eachCardColor = 'white'

        self.createCardBtn(ownerIndex, frameCards, cardIndex, eachCardType,
                           eachCardNumber, eachCardColor, eachCardReferenceColor)
        self.showPlayerCards()

        skipButton['state'] = 'normal'

    def addCardToGame(self, cardIndex):
        self.frameCardsInGame = tk.Frame(root, name='frameCardsInGame')
        self.frameCardsInGame.pack(anchor='center', pady=20)

        self.cardInTopType = CardType[mainc.getCardTypeFromDeck(cardIndex)]
        self.cardInTopNumber = mainc.getCardNumberFromDeck(cardIndex)

        self.cardInTopColor = f'{Colors[mainc.getCardColorFromDeck(cardIndex)]}'
        if self.cardInTopColor == 'colored':
            self.cardInTopColor = 'white'
        else:
            self.cardInTopReferenceColor = f'{ReferenceColors[mainc.getCardColorFromDeck(cardIndex)]}'

        self.cardInTopImg = Image.open(
            f'images/{self.cardInTopNumber}-{self.cardInTopType}.png').resize((99, 150))
        self.cardInTopImg = ImageTk.PhotoImage(self.cardInTopImg)

        self.labelCardInTop = tk.Label(self.frameCardsInGame, image=self.cardInTopImg,
                                       name='cardInTop', background=self.cardInTopColor, borderwidth=-5)
        self.labelCardInTop.pack(anchor='center')

        self.currentCardInGame += 1

    def nextPlayer(self, ownerIndex, cardIndex, eachCardType, eachCardNumber, eachCardReferenceColor):
        if (eachCardReferenceColor in [self.cardInTopReferenceColor, 'colored']) or (eachCardType == self.cardInTopType and eachCardType != 'number') or (eachCardNumber == self.cardInTopNumber and eachCardType == self.cardInTopType == 'number'):
            numberOfPlayers = mainc.getNumberOfPlayers()
            if eachCardType == 'reverse' and numberOfPlayers > 2:
                self.currentPlayer += -1 if self.isGameOrdered else 1
                self.isGameOrdered = False if self.isGameOrdered else True
                self.toggleSignal = 1 if self.isGameOrdered else -1
            elif eachCardType == 'skip' or eachCardType == 'reverse':
                self.currentPlayer += 2 * (self.toggleSignal)
            else:
                self.currentPlayer += 1 * (self.toggleSignal)

            if self.currentPlayer >= numberOfPlayers:
                defaultTimes = floor(self.currentPlayer/numberOfPlayers)
                self.currentPlayer -= numberOfPlayers*defaultTimes

            self.playersButtons[ownerIndex]['state'] = 'disable' if eachCardReferenceColor != 'colored' else 'normal'
            self.playersButtons[self.currentPlayer]['state'] = 'normal' if eachCardReferenceColor != 'colored' else 'disable'

            if eachCardReferenceColor == 'colored':
                self.chooseWildColor(ownerIndex, cardIndex)
            else:
                self.playerCards.destroy()
                self.isHandActive = False
                self.actionsAddCardToGame(ownerIndex, cardIndex)
        else:
            print("choose a valid card")

    def actionsAddCardToGame(self, ownerIndex, cardIndex):
        mainc.swapCardFromHandToGame(ownerIndex, cardIndex)
        self.frameCardsInGame.destroy()
        self.addCardToGame(self.currentCardInGame)

    def skipPlayer(self, ownerIndex):
        self.currentPlayer += 1 * (self.toggleSignal)
        if self.currentPlayer == mainc.getNumberOfPlayers():
            self.currentPlayer = 0
        self.playersButtons[ownerIndex]['state'] = 'disable'
        self.playersButtons[self.currentPlayer]['state'] = 'normal'
        self.playerCards.destroy()
        self.isHandActive = False

    def chooseWildColor(self, ownerIndex, cardIndex):
        self.disableCards()
        self.disablePersonBtn()
        self.frameChooseColor = tk.Frame(
            self.playerCards, name='frameChooseWildColor')
        self.frameChooseColor.pack(side='bottom', pady=5)

        labelTitle = tk.Label(self.frameChooseColor, text='Escolha a cor')
        labelTitle.pack()

        for color, refColor in zip(Colors[:-1], ReferenceColors[:-1]):
            eachBtn = tk.Button(self.frameChooseColor, text=refColor,
                                background=color, activebackground=color, width=15)
            eachBtn.pack(side='left', padx=10)
            eachBtn['command'] = partial(
                self.setcardInTopColor, ownerIndex, cardIndex, color, refColor)

    def setcardInTopColor(self, ownerIndex, cardIndex, newColor, newRefColor):
        self.cardInTopColor = newColor
        self.cardInTopReferenceColor = newRefColor
        self.playerCards.destroy()
        self.isHandActive = False
        self.playersButtons[self.currentPlayer]['state'] = 'normal'
        self.playersButtons[ownerIndex]['state'] = 'disable'
        self.actionsAddCardToGame(ownerIndex, cardIndex)


home = Home()
root.mainloop()
