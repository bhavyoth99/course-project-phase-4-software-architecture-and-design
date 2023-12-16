from django.shortcuts import render, redirect,get_object_or_404
from .models import Game, Card, Player,Turn
import random 

LEVELS = {
    'K-2': 1,
    '3-5': 2,
    '6-8': 3,
}

PATTERNS = {
    1: ['all_red', 'all_black', 'all_hearts', 'all_clubs'], # Patterns for level K-2
    2: ['all_single_digit_primes', 'add_to_9', 'all_queens', 'ace_and_black_jack'], # Patterns for level 3-5
    3: ['all_primes', 'poker_flush', 'poker_straight', 'poker_full_house', 'poker_four_of_a_kind'], # Patterns for level 6-8
}


suits = ['clubs', 'diamonds', 'hearts', 'spades']
ranks = list(range(2, 11)) + ['jack', 'queen', 'king', 'ace']
cards = [
    {'suit': suit, 'rank': rank, 'image': f'cards/{rank}_of_{suit}.png'}
    for suit in suits
    for rank in ranks
]


from random import choice

def start_game(request):
    if request.method == 'POST':
        level_name = request.POST.get('level', 'K-2')  # Default to 'K-2' if not provided
        level_number = LEVELS.get(level_name, 1)  # Default to 1 if level_name is not found in LEVELS

        # Get patterns for the given level and select one randomly
        patterns_for_level = PATTERNS.get(level_number, ['all_red'])  # Default to ['all_red'] if level_number not found
        pattern = choice(patterns_for_level)

        game = Game(level=level_number, pattern=pattern)
        game.save()

        # Create a dealer and seller
        dealer, _ = Player.objects.get_or_create(game=game, role='dealer')
        seller, _ = Player.objects.get_or_create(game=game, role='seller')

        # Create a deck of cards for the game
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                Card.objects.create(suit=suit[0], rank=rank, game=game)

        # Redirect to the game view
        return redirect('play_game', game_id=game.id)
    else:
        return render(request, 'main/start_game.html')



def check_pattern(cards, pattern):
    if pattern == 'all_red':
        return all(card.suit in ['hearts', 'diamonds'] for card in cards)
    
    if pattern == 'all_black':
        return all(card.suit in ['clubs', 'spades'] for card in cards)
    
    if pattern == 'all_hearts':
        return all(card.suit == 'hearts' for card in cards)
    
    if pattern == 'all_clubs':
        return all(card.suit == 'clubs' for card in cards)

    if pattern == 'all_single_digit_primes':
        return all(card.rank in [2, 3, 5, 7] for card in cards)
    
    if pattern == 'add_to_9':
        return sum(card.rank for card in cards) == 9
    
    if pattern == 'all_queens':
        return all(card.rank == 12 for card in cards)
    
    if pattern == 'ace_and_black_jack':
        return all((card.rank == 1 and card.suit in ['clubs', 'spades']) or card.rank == 11 for card in cards)

    if pattern == 'all_primes':
        return all(card.rank in [2, 3, 5, 7, 11, 13] for card in cards)
    
    if pattern == 'poker_flush':
        return len(set(card.suit for card in cards)) == 1

    if pattern == 'poker_straight':
        ranks = sorted(card.rank for card in cards)
        return all(ranks[i] == ranks[i + 1] - 1 for i in range(len(ranks) - 1))

    if pattern == 'poker_full_house':
        ranks = [card.rank for card in cards]
        return max(ranks.count(rank) for rank in set(ranks)) == 3 and min(ranks.count(rank) for rank in set(ranks)) == 2
    
    if pattern == 'poker_four_of_a_kind':
        ranks = [card.rank for card in cards]
        return max(ranks.count(rank) for rank in set(ranks)) == 4

    return False


def play_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    cards = Card.objects.filter(game=game)
    pattern = request.session.get('pattern') or PATTERNS[game.level][random.randint(0, len(PATTERNS[game.level]) - 1)]  # Select a pattern for this level
    request.session['pattern'] = pattern  # Store the pattern in the session

    # Loop through the cards and associate the image file path with each card
    for card in cards:
        rank = str(card.rank).lower() if card.rank != 10 else card.rank
        suit = card.suit.lower()
        card.image = f'img/cards/{rank}_of_{suit}.png'

    matching_cards = []  # Initialize an empty list for matching cards

    if request.method == 'POST' and 'select_cards' in request.POST:
        selected_card_ids = request.POST.getlist('selected_cards')
        selected_cards = [card for card in cards if str(card.id) in selected_card_ids]

        if len(selected_cards) != 4:
            error_message = "You must select exactly 4 cards."
        else:
            matching_cards = [card for card in selected_cards if check_pattern([card], pattern)]

            if len(matching_cards) == 4:
                # Victory! Redirect to the victory page.
                return redirect('win_view', game_id=game.id)

    # Always render the page to continue the game
    context = {
        'game': game,
        'cards': cards,
        'matching_cards': matching_cards,
        'error_message': error_message if 'error_message' in locals() else None,
    }
    return render(request, 'main/play_game.html', context)



def win_view(request, game_id):
    pattern = request.session.get('pattern', 'No pattern found')  # Retrieve the pattern from the session
    return render(request, 'main/win.html', {'pattern': pattern})



def game_view(request, game_id):
    game = Game.objects.get(pk=game_id)
    # More game logic here...

    context = {
        'game': game,
        # Add other relevant data here...
    }
    return render(request, 'game/game.html', context)



