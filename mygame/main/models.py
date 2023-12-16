from django.db import models


from django.db import models

class Game(models.Model):
    LEVEL_CHOICES = (
        (1, 'K-2'),
        (2, '3-5'),
        (3, '6-8'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    pattern = models.CharField(max_length=255) # Pattern that dealer wants, e.g., "all red", "all hearts", etc.
    is_active = models.BooleanField(default=True) # To check if the game is active

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # 'dealer' or 'seller'
    hand = models.CharField(max_length=255)  # Cards in player's hand, represented as a string
    penalties = models.IntegerField(default=0)

class Turn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    cards_played = models.CharField(max_length=255) # Cards played in this turn
    is_successful = models.BooleanField() # If the turn was successful according to the pattern


class Card(models.Model):
    SUITS = (
        ('hearts', 'Hearts'),
        ('diamonds', 'Diamonds'),
        ('clubs', 'Clubs'),
        ('spades', 'Spades'),
    )
    RANKS = [str(i) for i in range(2, 11)] +['jack', 'queen', 'king', 'ace']
    suit = models.CharField(max_length=10, choices=SUITS)
    rank = models.CharField(max_length=10, choices=[(r, r) for r in RANKS])
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)  # Reference to the game it belongs to
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__self(self):
        self.suit