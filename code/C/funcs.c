#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include "structs.h"

int N_PLAYERS = 2;
GameType GAME_TYPE = people;

Deck deck;
Deck* pDeck = &deck;

Hand players[maxNumberOfHands];
Hand* pPlayers[maxNumberOfHands];

// ---- CARD ----
void initializeCard(Card* pCard, Color color, Number number, Type type) {
    pCard->color = color;
    pCard->number = number;
    pCard->type = type;
}

void cardToString(Card* pCard, char strPrint[]) {
    switch (pCard->number) {
    case zero:  strcpy(strPrint, (pCard->type == number) ? " Zero" : " Null"); break;
    case one:   strcpy(strPrint, "  One"); break;
    case two:   strcpy(strPrint, "  Two"); break;
    case three: strcpy(strPrint, "Three"); break;
    case four:  strcpy(strPrint, " Four"); break;
    case five:  strcpy(strPrint, " Five"); break;
    case six:   strcpy(strPrint, "  Six"); break;
    case seven: strcpy(strPrint, "Seven"); break;
    case eigth: strcpy(strPrint, "Eight"); break;
    case nine:  strcpy(strPrint, " Nine"); break;
    default:    strcpy(strPrint, "?????"); break;
    }

    switch (pCard->color) {
    case red:     strcat(strPrint, " of Red     -> "); break;
    case green:   strcat(strPrint, " of Green   -> "); break;
    case blue:    strcat(strPrint, " of Blue    -> "); break;
    case yellow:  strcat(strPrint, " of Yellow  -> "); break;
    case colored: strcat(strPrint, " of Colored -> "); break;
    default:      strcat(strPrint, " of ??????  -> "); break;
    }

    switch (pCard->type) {
    case number:  strcat(strPrint, "Number "); break;
    case skip:    strcat(strPrint, "Skip   "); break;
    case reverse: strcat(strPrint, "Reverse"); break;
    case draw:    strcat(strPrint, "Draw   "); break;
    case wild:    strcat(strPrint, "Wild   "); break;
    default:      strcat(strPrint, "????   "); break;
    }
}

void printCard(Card* pCard) {
    char strPrint[50];
    cardToString(pCard, strPrint);
    printf("%s", strPrint);
}

// --- Card gets ---
int getCardColor(int ownerIndex, int cardIndex) {
    return pPlayers[ownerIndex]->cards[cardIndex]->color;
}

int getCardType(int ownerIndex, int cardIndex) {
    return pPlayers[ownerIndex]->cards[cardIndex]->type;
}

int getCardNumber(int ownerIndex, int cardIndex) {
    return pPlayers[ownerIndex]->cards[cardIndex]->number;
}

int getNumberOfCardsInHand(int ownerIndex) {
    return pPlayers[ownerIndex]->numberOfCards;
}

// ---- DECK ----
void initializeDeck(Deck* pDeck) {
    Card* pCard;
    int index = 0;
    // Normal Cards
    for (int i = 0; i < 2; i++)
    {
        for (int num = ((i == 1) ? one : zero); num < numberNumber; num++)
        {
            for (int color = red; color < colorNumber; color++)
            {
                pCard = &(pDeck->ordered[index]);
                initializeCard(pCard, color, num, number);
                index++;
            }
        }
    }

    // Wild Card
    Number cardNumber = zero;
    for (int i = 0; i < 2; i++)
    {
        for (int wildType = skip; wildType < wildNumber + 1; wildType++)
        {
            for (int color = red; color < colorNumber; color++)
            {
                if (wildType == draw)
                    cardNumber = two;
                else if (wildType == wild && i == 1)
                    cardNumber = four;
                else
                    cardNumber = zero;
                pCard = &(pDeck->ordered[index]);
                initializeCard(pCard, (wildType == wild) ? colored : color, cardNumber, wildType);
                index++;
            }

        }
    }

    for (int i = 0; i < cardsInDeck; i++) {
        pDeck->shuffled[i] = &(pDeck->ordered[i]);
        pDeck->inGame[i] = NULL;
    }

    pDeck->numberOfCards = cardsInDeck;
    pDeck->currentCard = 0;
}

void shuffleDeck(Deck* pDeck) {
    srand(time(NULL));
    int randomIndex = rand() % (normalCardsNumber/colorNumber + 1);
    randomIndex *= rand() % (colorNumber);
    Card* pCard;
    for (int i = 0; i < cardsInDeck; i++)
    {
        pCard = pDeck->shuffled[i];
        pDeck->shuffled[i] = pDeck->shuffled[randomIndex];
        pDeck->shuffled[randomIndex] = pCard;
        randomIndex = rand() % (cardsInDeck);
    }

}

void printDeck(Deck* deck , bool isShuffled) {
    if (deck->numberOfCards == 0)
        printf("Without cards");

    for (int i = 0; i < deck->numberOfCards; i++)
    {
        if (i != 0 && i % 4 == 0)
            printf("\n");

        if (isShuffled == true)
            printCard(deck->shuffled[i]);
        else
            printCard(&(deck->ordered[i]));
        printf(" | ");
    }
}

void pyPrintDeck(bool isShuffled){
    printDeck(pDeck, isShuffled);
}

Card* getCardFromShuffled(Deck* pDeck) {
    Card* pCard;
    pCard = pDeck->shuffled[cardsInDeck - pDeck->numberOfCards];
    pDeck->numberOfCards--;
    return pCard;
}

int getCardColorFromDeck(int cardIndex) {
    return pDeck->inGame[cardIndex]->color;
}

int getCardTypeFromDeck(int cardIndex) {
    return pDeck->inGame[cardIndex]->type;
}

int getCardNumberFromDeck(int cardIndex) {
    return pDeck->inGame[cardIndex]->number;
}

// ---- HAND ----
void initializeHand(Hand* pHand) {
    pHand->numberOfCards = 0;
    for (int i = 0; i < maxCardsInHand; i++)
        pHand->cards[i] = NULL;
}


void addCardToHand(Hand* pHand, Deck* pDeck) {
    Card* pCard;
    pCard = getCardFromShuffled(pDeck);
    pHand->cards[pHand->numberOfCards] = pCard;
    pHand->numberOfCards++;
}

Card* getCardFromHand(int ownerIndex, int index) {
    Card* pCard;
    if (index >= pPlayers[ownerIndex]->numberOfCards) return NULL;
    pCard = pPlayers[ownerIndex]->cards[index];
    pPlayers[ownerIndex]->cards[index] = NULL;
    for (int i = index + 1; i < pPlayers[ownerIndex]->numberOfCards; i++)
        pPlayers[ownerIndex]->cards[i - 1] = pPlayers[ownerIndex]->cards[i];
    pPlayers[ownerIndex]->numberOfCards--;
    return pCard;
}

void printHand(int ownerIndex) {
    printf("%d%c Player's Cards:\n", ownerIndex, 248);
    for (int i = 0; i < pPlayers[ownerIndex]->numberOfCards; i++)
    {
        printCard(pPlayers[ownerIndex]->cards[i]);
    }
}

void drawCard(int ownerIndex) {
    if (pDeck->numberOfCards != 0)
        addCardToHand(pPlayers[ownerIndex], pDeck);
}

// ---- GAME ----
void gameSettings(int numberOfPlayers, GameType type) {
    N_PLAYERS = numberOfPlayers;
    GAME_TYPE = type;
}

void printSettings() {
    printf("Number of players: %d\n", N_PLAYERS);
    printf("Game Type: %d", GAME_TYPE);
}

void initializePlayersHand(Hand players[], Hand* pPlayers[]) {
    for (int i = 0; i < N_PLAYERS; i++) {
        pPlayers[i] = &(players[i]);
        initializeHand(pPlayers[i]);
    }
}

void initializePlayersGame(Deck* pDeck, Hand* pPlayers[]) {
    for (int player = 0; player < N_PLAYERS; player++)
    {
        for (int i = 0; i < cardsInHand; i++)
        {
            addCardToHand(pPlayers[player], pDeck);
        }
    }
}

void swapCardFromHandToGame(int ownerIndex, int cardIndex){
    pDeck->inGame[pDeck->currentCard] = getCardFromHand(ownerIndex, cardIndex);
    pDeck->currentCard++;
}

int getNumberOfPlayers() {
    return N_PLAYERS;
}
