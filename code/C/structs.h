typedef enum { red=0, yellow, green, blue, colored } Color;
typedef enum { number=0, skip, reverse, draw, wild } Type;
typedef enum { people=0, computer } GameType;
typedef enum { zero=0, one, two, three, four, five, six, seven, eigth, nine } Number;

enum Constants {
    cardsInHand = 7,
    maxCardsInHand = 108, //maximum number of cards
    cardsInDeck = 108,
    maxNumberOfHands = 14,
    normalCardsNumber = 76,
    wildCardsNumber = 32,
    colorNumber = 4,
    numberNumber = 10,
    wildNumber = 4,
};

typedef struct {
    Color color;
    Type type;
    Number number;
} Card;

typedef struct{
    Card ordered[cardsInDeck];
    Card* shuffled[cardsInDeck];
    Card* inGame[cardsInDeck];
    int numberOfCards;
    int currentCard;
} Deck;

typedef struct{
    int numberOfCards;
    Card* cards[maxCardsInHand];
} Hand;
