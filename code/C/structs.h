typedef enum { red, yellow, green, blue } Color;
typedef enum { number, reverse, draw, skip, wild } Type;
typedef enum { zero=0, one, two, three, four, five, six, seven, eigth, nine } Number;

enum Constants {
    cardsInHand = 7,
    cardsInDeck = 108,
    normalCardsNumber = 76,
    wildCardsNumber = 32,
    colorNumber = 4,
    numberNumber = 10,
    ownerNameLen = 25,
};

typedef struct {
    Color color;
    Type type;
    Number number;
} NormalCard;

typedef struct {
    Color color;
    Type type;
    Number drawNumber;
} WildCard;

typedef struct{
    NormalCard* normalCards[cardsInHand];
    WildCard* wildCard[cardsInHand];
} pCards;

typedef struct{
    NormalCard normalCards[normalCardsNumber];
    WildCard wildCard[wildCardsNumber];
    int numberOfCards;
} Deck;

typedef struct{
    char ownerName[ownerNameLen];
    int numberOfCards;
    pCards* cards;
} Hand;
