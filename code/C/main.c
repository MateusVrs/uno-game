#include <stdio.h>
#include <stdlib.h>
#include "funcs.c"

int main() {
    initializeDeck(pDeck);
    shuffleDeck(pDeck);
    initializePlayersHand(players, pPlayers);
    initializePlayersGame(pDeck, pPlayers);
    pDeck->inGame[0] = getCardFromShuffled(pDeck);
}

// gcc -shared -o libmain.dll -fPIC main.c
