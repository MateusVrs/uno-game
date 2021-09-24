#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include "structs.h"

// ---- Card ----
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
    char strPrint[20];
    cardToString(pCard, strPrint);
    printf("%s", strPrint);
}

// ---- Deck ----
void initializeDeck(Deck* pDeck) {
    Card* pCard;
    int index = 0;
    // Normal Cards
    for (size_t i = 0; i < 2; i++)
    {
        for (size_t num = ((i == 1) ? one : zero); num < numberNumber; num++)
        {
            for (size_t color = red; color < colorNumber; color++)
            {
                pCard = &(pDeck->ordered[index]);
                initializeCard(pCard, color, num, number);
                index++;
            }
        }
    }

    // Wild Card
    Number cardNumber = zero;
    for (size_t i = 0; i < 2; i++)
    {
        for (size_t wildType = skip; wildType < wildNumber + 1; wildType++)
        {
            for (size_t color = red; color < colorNumber; color++)
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

    for (size_t i = 0; i < cardsInDeck; i++)
        pDeck->shuffled[i] = &(pDeck->ordered[i]);

    pDeck->numberOfCards = cardsInDeck;
}

void shuffleDeck(Deck* pDeck) {
    srand(time(NULL));
    int randomIndex = rand() % (cardsInDeck);
    Card* pCard;
    for (size_t i = 0; i < cardsInDeck; i++)
    {
        pCard = pDeck->shuffled[i];
        pDeck->shuffled[i] = pDeck->shuffled[randomIndex];
        pDeck->shuffled[randomIndex] = pCard;
        randomIndex = rand() % (cardsInDeck);
    }

}

void printDeck(Deck* pDeck, bool isShuffled) {
    for (size_t i = 0; i < cardsInDeck; i++)
    {
        if (i != 0 && i % 4 == 0)
            printf("\n");

        if (isShuffled == true)
            printCard(pDeck->shuffled[i]);
        else
            printCard(&(pDeck->ordered[i]));
        printf(" | ");
    }
}

Card* getCardFromShuffled(Deck* pDeck) {
    Card* pCard;
    pCard = pDeck->shuffled[cardsInDeck - pDeck->numberOfCards];
    pDeck->numberOfCards--;
    return pCard;
}

// ---- Hand ----
void initializeHand(Hand* pHand) {
    pHand->numberOfCards = 0;
    for (size_t i = 0; i < maxCardsInHand; i++)
        pHand->cards[i] = NULL;
}


void addCardToHand(Hand* pHand, Deck* pDeck) {
    Card* pCard;
    pCard = getCardFromShuffled(pDeck);
    pHand->cards[pHand->numberOfCards] = pCard;
    pHand->numberOfCards++;
}

Card* getCardFromHand(Hand* pHand, int index) {
    Card* pCard;
    if (index >= pHand->numberOfCards) return NULL;
    pCard = pHand->cards[index];
    pHand->cards[index] = NULL;
    for (size_t i = index + 1; i < pHand->numberOfCards; i++)
        pHand->cards[i - 1] = pHand->cards[i];
    pHand->numberOfCards--;
    return pCard;
}

void printHand(Hand* pHand, int ownerIndex) {
    printf("%d%c Player's Cards:\n", ownerIndex, 248);
    for (size_t i = 0; i < pHand->numberOfCards; i++)
    {
        printCard(pHand->cards[i]);
        printf("\n");
    }
}

// ---- Game ----
void initializePlayersHand(Deck* pDeck, Hand* pPlayers[], int numberOfPlayers) {
    for (size_t player = 0; player < numberOfPlayers; player++)
    {
        for (size_t i = 0; i < cardsInHand; i++)
        {
            addCardToHand(pPlayers[player], pDeck);
        }
    }   
}
