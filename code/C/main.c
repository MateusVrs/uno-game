#include <stdio.h>
#include <stdlib.h>
#include "funcs.c"

int main() {
    initializeDeck(pDeck);
    shuffleDeck(pDeck);
    initializePlayersHand(players, pPlayers);
    initializePlayersGame(pDeck, pPlayers);
    pDeck->inGame[pDeck->currentCard] = getCardFromShuffled(pDeck);
    pDeck->currentCard++;
}

// gcc -shared -o libmain.dll -fPIC main.c
// gcc -shared -o libmain.so -fPIC main.c
