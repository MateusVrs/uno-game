#include <string.h>
#include "structs.h"

// ---- Card ----
void initializeNormalCard(NormalCard* pCard, Color color, Number number, Type type) {
    pCard->color = color;
    pCard->number = number;
    pCard->type = type;
}

void normalCardToString(NormalCard* pCard, char strPrint[]) {
    switch (pCard->number) {
    case zero:  strcpy(strPrint, " Zero"); break;
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
    case red:    strcat(strPrint, " of Red"); break;
    case green:  strcat(strPrint, " of Green"); break;
    case blue:   strcat(strPrint, " of Blue"); break;
    case yellow: strcat(strPrint, " of Yellow"); break;
    default:     strcat(strPrint, " of ??????"); break;
    }
}

void printNormalCard(NormalCard* pCard) {
    char strPrint[20];
    normalCardToString(pCard, strPrint);
    printf("%s %10c", strPrint, ' ');
}

// ---- Deck ----
void initializeDeck(Deck* pDeck) {
    NormalCard* pNormalCard;
    pDeck->numberOfCards = cardsInDeck;
    int normalIndex = 0;
    for (size_t i = 0; i < 2; i++)
    {
        for (size_t num = ((i == 1) ? 1 : 0); num < numberNumber; num++)
        {
            for (size_t color = 0; color < colorNumber; color++)
            {
                pNormalCard = &(pDeck->normalCards[normalIndex]);
                initializeNormalCard(pNormalCard, color, num, number);
                normalIndex++;
            }
        }
    }
}

// ---- Hand ----
void initializeHand(Hand* pHand, char ownerName[ownerNameLen]) {
    strcpy(pHand->ownerName, ownerName);
    pHand->numberOfCards = 0;
    for (size_t i = 0; i < cardsInHand; i++) {
        pHand->cards->normalCards[i] = NULL;
        pHand->cards->wildCard[i] = NULL;
    }
}
