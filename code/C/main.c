#include <stdio.h>
#include <stdlib.h>
#include "funcs.c"

int main() {
    Deck myDeck;
    Deck* pMyDeck = &myDeck;
    initializeDeck(pMyDeck);
    for (size_t i = 0; i < normalCardsNumber; i++)
    {
        if (i % 4 == 0 && i != 0)
            printf("\n");
        printNormalCard(&(pMyDeck->normalCards[i]));
    }
    return 0;
}

// gcc -shared -o libmain.dll -fPIC main.c
