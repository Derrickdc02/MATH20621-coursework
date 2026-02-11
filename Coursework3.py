"""
MATH20621 - Coursework 3
Student name: Yaocong Deng
Student id:   REDACTED
Student mail: REDACTED
"""

import random # import random package for cards shuffle
import copy   # import copy package for copys

def display_state(s, *, clear=False):
    """
    Display the state s

    If 'clear' is set to True, erase previous displayed states
   """
    def colored(r, g, b, text):
        rb,gb,bb=(r+2)/3,(g+2)/3,(b+2)/3
        rd,gd,bd=(r)/1.5,(g)/1.5,(b)/1.5
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    def inverse(text):
        rb,gb,bb=.2,.2,.2
        rd,gd,bd=.8,.8,.8
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    colours = [(1.0, 0.349, 0.369),
               (1.0, 0.573, 0.298),
               (1.0, 0.792, 0.227),
               (0.773, 0.792, 0.188),
               (0.541, 0.788, 0.149),
               (0.322, 0.651, 0.459),
               (0.098, 0.509, 0.769),
               (0.259, 0.404, 0.675),
               (0.416, 0.298, 0.576)]

    n_columns = len(s['stacks'])
    if clear:
        print(chr(27) + "[2J")

    print('\n')
    row = 0
    numrows = max(len(stack) for stack in s['stacks'])
    for row in range(numrows-1,-1,-1):
        for i in range(n_columns):
            num_in_col = len(s['stacks'][i])
            if num_in_col > row:
                val = s['stacks'][i][row]
                if num_in_col == row+1 and s['blocked'][i]:
                    print(inverse(' '+str(val)+' '),end=' ')
                else:
                    if s['complete'][i]:
                        print(colored(*colours[val-1],'   '),end=' ')
                    else:
                        print(colored(*colours[val-1],' '+str(val)+' '),end=' ')
            else:
                print('    ',end='')
        print()
    print(' A   B   C   D   E   F')
    

# Q1
def initial_state():
    '''
    Create the initial game state for a new solitaire game.

    This function shuffles a deck of cards containing four copies of numbers 1–9,
    evenly distributes the cards into six stacks, and sets the 'blocked' and 'complete'
    flags for all stacks to `False`.
    
    Returns
    -------
    initials : dict
        a dictionary describing initial state with:
        'blocked' - list of bool indicating whether each stack is blocked.
                    Initially, all stacks are unblocked ('False')
        'complete' - list of bool indicating whether each stack is complete.
                     Initially, all stacks are incomplete ('False')
        'stacks' - list of list shows the initial state of card stacks. 
                   Each stack is represented as a list of integers, which represents a card.

    '''
    # create a deck including four copies of each of the numbers 1–9
    deck = [i for i in range(1,10)] * 4
    random.shuffle(deck) # shuffle the deck
    
    # create a new, empty dictionary
    initials = {}
    # set all stacks as not blocked or complete
    initials['blocked'] = [False] * 6
    initials['complete'] = [False] * 6
    # distribute cards evenly into six stacks
    initials['stacks'] = [deck[i * 6 : (i+1) * 6] for i in range(6)]
    
    return initials
    

# Q2
def parse_move(input_str):
    '''
    Parse a user input to interpret a move in the solitaire game.
    
    Parameters
    ----------
    input_str : str
        
        The user input with the format:
        - "AB3": Move 3 cards from stack A onto stack B.
        - "AB": Move 1 card from stack A onto stack B (the default setting if no number is provided).
        - "R" or "r": Restart the game
        - "U" or "u": Undo the last move

    Returns
    -------
    con_input :  int or tuple (source_stack, destination_stack, number_of_cards)
        Q2/Q6 a tuple interpreted input into correct format with all number, e.g. (0, 1, 3).
        Q7 return 0 if input 'R' or 'r' (restart)
        Q8 return -1 if input 'U' or 'u' (undo)
        
    Raises
    ------
    ValueError
        If the input is invalid due to the following:
        - Incorrect format, e.g. too short or too long, or invaild characters.
        - Source and destination stacks are the same.
        - Number of cards to move is zero or negative.
        - Source and destination stacks are outside the range A to F.
    '''
    # return 0 when input 'R' or 'r' for Q7
    if input_str.upper() == 'R':
        return 0 
    
    # return -1 when input 'U' or 'u' for Q8
    elif input_str.upper() == 'U':
        return -1
    
    # convert the input as a list
    input_str = list(input_str)
    # create a new, empty list
    con_input = []
    # limit the lenth of input
    if len(input_str) < 2 or len(input_str) > 3:
        raise ValueError("Input must be two letters (A-F) followed optionally by a number (e.g., 'AB3').")
        
    # unpack input with source, destination
    source = input_str[0]
    destination = input_str[1]
    
    # limit the first two input must be letter 'A-F'
    if source < 'A' or source >'F' or destination < 'A' or destination > 'F':
        raise ValueError("Source and destination must be within the range A-F.")
    
    # read the number of cards to move (1 if there's no input)
    number_of_cards = int(input_str[2]) if len(input_str) == 3 else 1
    
    # make sure the number is positive, and the source and destination are different to avoid error  
    if number_of_cards <= 0:
        raise ValueError("Number of cards should be a postive integer.")
        
    if source == destination:
        raise ValueError("The source stack and destination stack should be different.")

    # convert the alphabet 'A-f' into number '0-6'
    source_stack = ord(source) - ord('A')
    destination_stack = ord(destination) - ord('A')
    
    # pack three element as a tuple
    con_input = (source_stack, destination_stack, number_of_cards)
    
    return con_input 

# Q3
def validate_move(state, move):
    '''
    Determining if a move is valid. 
    This function verifies whether moving a 
    
    Parameters
    ----------
    state : dict
        A valid game state containing:
        'blocked' - list of bool indicating whether each stack is blocked.
        'complete' - list of bool indicating whether each stack is complete.
        'stacks' - list of list shows the initial state of card stacks. 
    move : tuple (source, destination, number_of_cards)
        An interpreted user input representing cards move.
        - source_stack (int): Index of the source stack
        - destination_stack (int): Index of destination stack
        - number_of_cards (int): The number of cards to move

    Returns
    -------
    bool
        True if the move is vaild according to the game's rules'; 
        otherwise, False.
    '''
    # unpack move with source, destination and number of cards
    source_stack, destination_stack, number_of_cards = move
    
    # check the stack has enough cards
    if number_of_cards > len(state['stacks'][source_stack]):
        print("Invalid move: Source stack does not have enough cards.")
        return False
    
    # check if moving into (from) a completed set
    if state['complete'][destination_stack] or state['complete'][source_stack]:
        print("Invalid move: Source stack or destination stack is already complete.")
        return False
    
    # check if moving into a blocked set
    if state['blocked'][destination_stack]:
        print("Invalid move: Destination stack is blocked.")
        return False
    
    # move multiple cards on a stack at once if only if they are ordered
    cards_to_move = state['stacks'][source_stack][-number_of_cards:]
    if number_of_cards > 1 and sorted(cards_to_move) != list(range(cards_to_move[-1], cards_to_move[0] + 1)):
        print("Invalid move: Cards to move are not in order.")
        return False
    
    # when the destination stack is not empty
    if state['stacks'][destination_stack]:
        # check the top card of the destination
        top_card = state['stacks'][destination_stack][-1]
        if number_of_cards > 1: # one card might be valid because of the blocking rule
            if cards_to_move[0] != top_card - 1:    # if the moves don't match the top card
                print("Invalid move: Cards to move don't match the top card.")
                return False
    
        # move the top card of the blocked stack
        if state['blocked'][source_stack]:
            # return false if the blocked card move to an unvaild location
            if state['stacks'][source_stack][-1] != top_card - 1:
                print("Invalid move: The move doesn't follow the unblock rule.")
                return False  
            
    return True  # return true if it meets all condition

# Q4
def apply_move(state, move):
    '''
    Move the cards and update the blocked and complete fields of the game state.
    
    This function updates the game state by moving the specified number of cards 
    from the source stack to the destination stack. It also manages the `blocked` 
    and `complete` fields to reflect the changes after the move.
    
    Parameters
    ----------
    state : dict
        A dictionary represent the current state of the game:
        'blocked' - list of bool indicating whether each stack is blocked.
        'complete' - list of bool indicating whether each stack is complete.
        'stacks' - list of list shows the initial state of card stacks.
    move : tuple
        A vaild move contains of source of stack, destination and number of cards, i.e. (A, B, 3). 

    Returns
    -------
    None
        The function modifies the `state` dictionary in place.

    '''
    # unpack move with source, destination and number of cards
    source_stack, destination_stack, number_of_cards = move
    
    # load the cards to move
    cards_to_move = state['stacks'][source_stack][-number_of_cards:]
    
    # if the destination stack is not empty, we record the number of the top card
    if state['stacks'][destination_stack]:
        top_card = state['stacks'][destination_stack][-1]
        
        # if the one moved card is not 1 smaller than the top card, block the stack
        if number_of_cards == 1 and cards_to_move[0] != top_card - 1:
            state['blocked'][destination_stack] = True
    
    # if the source stack is blocked and the move is vaild (according to Q2 and Q3), unblock the stack
    if state['blocked'][source_stack]:
        state['blocked'][source_stack] = False
    
    # take the card(s) to move out of the source stack
    state['stacks'][source_stack] = state['stacks'][source_stack][:-number_of_cards]
    # put the card(s) to move into the destination stack
    state['stacks'][destination_stack].extend(cards_to_move)
    
    # if the destination stack contain 1-9 in order, it becomes complete      
    if state['stacks'][destination_stack] == list(range(9,0,-1)):
        state['complete'][destination_stack] = True
    
    
    

# Q5
def game_won(state):
    '''
    Detecting a win if there are 4 complete stacks.
    A stack is considered complete if it contains the sequence 
    [9, 8, ..., 1] in descending order.
    This function determines whether the game is in a winning state by verifying 
    that all stacks in the game are either complete or empty. 

    Parameters
    ----------
    state : dict
        A dictionary describing the current valid game state.

    Returns
    -------
    bool
        Returns 'True' if the game won, i.e. all stacks are ether empty or complete.
        Returns 'False' otherwise.

    '''
    return state['complete'].count(True) == 4  # true if there are 4 completed stacks


# For questions 1-5, DO NOT edit the play_game function.
# For the tasks in questions 1-5 initial_state, parse_move,
# validate_move, apply_move, and game_won must work with the
# the unmodified play_game function.

# For questions 6, 7 and 8, you should modify the play_game
# function

def play_game():
    # When we start the game,
    board = initial_state()
    history = [copy.deepcopy(board)]
    try:
        while True:
            # Display the current game state
            display_state(board, clear=False)

            # Read input from the user.
            # (Do not alter this line, even in questions 6, 7, 8.)
            move_str = input()

            try:
                # Parse the text typed by the user and convert it to a move
                move = parse_move(move_str)
            
                # if the input is R(r), restart the game
                if move == 0:
                    board = initial_state()
                    history = [copy.deepcopy(board)]  # deepcopy the state for undo
            
                # if the input is U(u), undo the move
                elif move == -1:
                    if len(history) > 1: 
                        history.pop()     # delete the last move history
                        board = copy.deepcopy(history[-1]) # return to the last state
                
                elif move:
                   # If the move was valid, we apply the move on current state
                   if validate_move(board, move):
                        apply_move(board, move)
                        history.append(copy.deepcopy(board)) # deepcopy the state, save for undo function
            except ValueError as e:
                print(f"Error - {e} Please try again.")

            # If we've won, end the game
            if game_won(board):
                display_state(board, clear=False)   # display the final winning state
                break

    except KeyboardInterrupt: # If the user presses Ctrl-C, quit
        pass


play_game()