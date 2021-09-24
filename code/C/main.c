#include <stdio.h>
#include <stdlib.h>
#include "funcs.c"

#define N_PLAYERS 3
Hand players[N_PLAYERS];
Hand* pPlayers[N_PLAYERS];

int main() {
    Deck deck;
    Deck* pDeck = &deck;

    initializeDeck(pDeck);
    shuffleDeck(pDeck);

    for (size_t i = 0; i < N_PLAYERS; i++) {
        pPlayers[i] = &(players[i]);
        initializeHand(pPlayers[i]);
    }
    initializePlayersHand(pDeck, pPlayers, N_PLAYERS);
    for (size_t i = 0; i < N_PLAYERS; i++)
    {
        printHand(pPlayers[i], i + 1);
        printf("\n");
    }
}

// gcc -shared -o libmain.dll -fPIC main.c
