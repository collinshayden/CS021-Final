#Hayden Collins
#CS 028
#Final Project

from legal_moves import legal_moves_of_color, determine_castling_rights

letters = ['a','b','c','d','e','f','g','h']
numbers = ['1','2','3','4','5','6','7','8']
numbers_reverse = ['8','7','6','5','4','3','2','1']

board_dict = {}
moves_dict = {}
king_locations = {'white': 'e1', 'black': 'e8'}

turn = 'white'
move_count = 1
game_end = False

def main():
  set_board_dict()
  display_board()

  while game_end == False:
    request_input()

#asks the user to input a move
def request_input():
  inputStr = input('Enter a move in long algebraic form (e2e4 for example, quit to exit, help for a list of commands): ')
  commands(inputStr)
  
#if the user inputs one of the command names defined below, execute that command block.
def commands(inputStr):
  commands_list = ['quit', 'help', 'legal_moves', 'short_legal_moves', 'display', 'checkmate_setup', 'promotion_setup', 'castling_setup', 'en_passant_setup', 'show_moves']
  if inputStr in commands_list:
    if inputStr == 'quit':
      global game_end
      game_end = True
      return #empty return to exit the function after quitting

    elif inputStr == 'help':
      print("\nWelcome to my chess program. To input a move, use long algebraic notation.")
      print("This is the current coordinate of the piece you would like to move followed by the new coordinate position (no spaces).")
      print("\nTo see a list of legal moves in long algebraic notation (the same as the input format), type 'legal_moves'.")
      print("\nTo see a list of legal moves in short algebraic notation (piece letter + new position), type 'short_legal_moves'.")
      print("\nTo setup the board to demonstate checkmate, type 'checkmate_setup'.")
      print("\nTo setup the board to demonstate promotion, type 'promotion_setup'.")
      print("\nTo setup the board to demonstate castling, type 'castling_setup'.")
      print("\nTo redisplay the board, type 'display'.")
      print("\nTo see a list of the moves played, type 'show_moves'.")
      print("\nTo exit the program, type 'quit'.")
      print("\nTo see this message again, type 'help'\n")

    elif inputStr == 'display':
      display_board()

    elif inputStr == 'legal_moves':#lists all legal moves in long algebraic form (the same form as input)
      long_algebraic_moves = []
      legal_moves_dict = legal_moves_of_color(turn, king_locations, board_dict)
      for key in legal_moves_dict:#key is the coordinate of a piece that can be moved
        for value in legal_moves_dict[key]:#value is the list of legal moves the piece can make
          long_algebraic_moves.append(key+value)
      long_algebraic_moves.sort()#better for displaying when sorted
      print(f"The legal moves in this position are {long_algebraic_moves}")

    elif inputStr == 'short_legal_moves':#lists all legal moves in short algebraic form. primarily for debugging (easier to read)
      short_algebraic_moves = []
      legal_moves_dict = legal_moves_of_color(turn, king_locations, board_dict)
      for key in legal_moves_dict:#key is the coordinate of a piece that can be moved
        starting_position = key
        for value in legal_moves_dict[key]:#value is the list of legal moves the piece can make
          new_position = value
          piece = board_dict[starting_position]['piece']#type of piece on the starting position
          piece_symbol = piece[0].upper() if piece != 'pawn' else ''#the letter that represents the piece (e.g. Q for queen, blank for pawn)
          if board_dict[new_position] != None: piece_symbol += 'x'#if the move is a capture, it should be Qxf6 instead of Qf6
          short_algebraic_moves.append(piece_symbol+new_position)#note, I am not including a + when it is check, too complicated to add
      short_algebraic_moves.sort()#better for displaying when sorted
      print(f"The legal moves in this position are {short_algebraic_moves}")
    
    elif inputStr == 'checkmate_setup':
      set_board_dict(position='checkmate_setup')
      display_board()
      print("Recommended continuation: h7h8 checkmate")

    elif inputStr == 'promotion_setup':
      set_board_dict(position='promotion_setup')
      display_board()
      print("Recommended continuation: h7h8 queen, a2a1 queen, e5f5, a1h8")
    
    elif inputStr == 'castling_setup':
      set_board_dict(position='castling_setup')
      display_board()
      print("Recommended continuation: e1g1")
    elif inputStr == 'en_passant_setup':
      set_board_dict(position='en_passant_setup')
      display_board()

    elif inputStr == 'show_moves':
      for move_num in moves_dict:
        print(f"{move_num}. {moves_dict[move_num]['white']}, {moves_dict[move_num]['black']}")

  else:
    move(inputStr)#if the input was not a command, send it to move(), validity is checked there

  if game_end == False:  
    request_input()#if a command was the input (and not quit) it prompts for another input

#takes in a move in long algebraic form, seperates into starting and new position, executes move if legal
def move(inputStr):
  if game_end == False:
    try:
      starting_position = inputStr[0]+inputStr[1]
      new_position = inputStr[2]+inputStr[3]

      legal_moves_dict = legal_moves_of_color(turn, king_locations, board_dict)
      try:
        legal_moves_dict[starting_position].extend(check_for_en_passant(starting_position))
      except:
        pass
      legal_moves_dict[starting_position].extend(determine_castling_rights(starting_position, board_dict, king_locations))
      if board_dict[starting_position]['color'] == turn:#if the piece selected to be moved is the same color as the turn
        if new_position in legal_moves_dict[starting_position]:#if the new position is a legal move of the selected piece
          castle_if_played(starting_position, new_position)
          en_passant_if_played(starting_position, new_position)
          #updating the board
          board_dict[new_position] = board_dict[starting_position]
          board_dict[new_position]['moved'] = True
          board_dict[starting_position] = None
          
          record_move(starting_position, new_position)
          update_king_location()
          check_for_promotion(new_position)
          display_board()
          change_turn()
          check_for_game_end()
        else:
          print(f'{inputStr} is not a legal move')
          print(f"The legal moves in this position are {legal_moves_dict}")

      else: 
        print(f"It is {turn} to move")
    except:
      print(f"{inputStr} is not a valid input.")
      
#sets the board to starting position
def set_board_dict(position='standard'):
  global board_dict, turn, moves_dict, move_count
  turn = 'white'; moves_dict = {}; move_count = 1
  for l in letters:
    for n in numbers: 
      board_dict[l+n] = None

  if position == 'standard':
    #white
    for l in letters:
      board_dict[l+'2'] = {'piece': 'pawn', 'color': 'white', 'moved': False}
    board_dict['a1'], board_dict['h1'] = {'piece': 'rook', 'color': 'white', 'moved': False}, {'piece': 'rook', 'color': 'white', 'moved': False}
    board_dict['b1'], board_dict['g1'] = {'piece': 'night', 'color': 'white', 'moved': False}, {'piece': 'night', 'color': 'white', 'moved': False}
    board_dict['c1'], board_dict['f1'] = {'piece': 'bishop', 'color': 'white', 'moved': False}, {'piece': 'bishop', 'color': 'white', 'moved': False}
    board_dict['d1'] = {'piece': 'queen', 'color': 'white', 'moved': False}
    board_dict['e1'] = {'piece': 'king', 'color': 'white', 'moved': False}

    #black
    for l in letters:
      board_dict[l+'7'] = {'piece': 'pawn', 'color': 'black', 'moved': False}
    board_dict['a8'], board_dict['h8'] = {'piece': 'rook', 'color': 'black', 'moved': False}, {'piece': 'rook', 'color': 'black', 'moved': False}
    board_dict['b8'], board_dict['g8'] = {'piece': 'night', 'color': 'black', 'moved': False}, {'piece': 'night', 'color': 'black', 'moved': False}
    board_dict['c8'], board_dict['f8'] = {'piece': 'bishop', 'color': 'black', 'moved': False}, {'piece': 'bishop', 'color': 'black', 'moved': False}
    board_dict['d8'] = {'piece': 'queen', 'color': 'black', 'moved': False}
    board_dict['e8'] = {'piece': 'king', 'color': 'black', 'moved': False}

  elif position == 'checkmate_setup':#setting up a position to test checkmate
    board_dict['e8'] = {'piece': 'king', 'color': 'black', 'moved': True}
    board_dict['e6'] = {'piece': 'king', 'color': 'white', 'moved': True}
    board_dict['h7'] = {'piece': 'rook', 'color': 'white', 'moved': True}

  elif position == 'promotion_setup':#setting up a position to test promotion
    board_dict['e7'] = {'piece': 'king', 'color': 'black', 'moved': True}
    board_dict['a2'] = {'piece': 'pawn', 'color': 'black', 'moved': True}

    board_dict['e5'] = {'piece': 'king', 'color': 'white', 'moved': True}
    board_dict['h7'] = {'piece': 'pawn', 'color': 'white', 'moved': True} 

  elif position == 'castling_setup':#setting up a position to test castling
    set_board_dict(position='standard')
    board_dict['e4'] = board_dict['e2']; board_dict['e4']['moved'] = True; board_dict['e2'] = None
    board_dict['c4'] = board_dict['f1']; board_dict['c4']['moved'] = True; board_dict['f1'] = None
    board_dict['f3'] = board_dict['g1']; board_dict['f3']['moved'] = True; board_dict['g1'] = None

    board_dict['e5'] = board_dict['e7']; board_dict['e5']['moved'] = True; board_dict['e7'] = None
    board_dict['h6'] = board_dict['h7']; board_dict['h6']['moved'] = True; board_dict['h7'] = None
    board_dict['c6'] = board_dict['b8']; board_dict['c6']['moved'] = True; board_dict['b8'] = None
  
  elif position == 'en_passant_setup':
    board_dict['e4'] = {'piece': 'pawn', 'color': 'white', 'moved': True} 
    board_dict['f7'] = {'piece': 'pawn', 'color': 'black', 'moved': False} 
    board_dict['d7'] = {'piece': 'pawn', 'color': 'black', 'moved': False} 
    board_dict['e8'] = {'piece': 'king', 'color': 'black', 'moved': True}
    board_dict['e1'] = {'piece': 'king', 'color': 'white', 'moved': True}
#displays the board and pieces in console
def display_board():
  print('\n')
  for n in numbers_reverse:
    for l in letters:
      if board_dict[l+n] == None:
        print('|  |', end = '')
      else:
        print('|' + board_dict[l+n]['color'][0] + board_dict[l+n]['piece'][0].upper() + '|', end = '')
    print(f'{n}\n')
  for l in letters:
    print(f'|{l}|', end=' ')
  print('\n')

#updates the global variables for white/black king location, called at the end of each move
#this could be coded more efficiently, but this is more robust and simple 
def update_king_location():
  global king_locations
  for l in letters:
    for n in numbers:
      if board_dict[l+n] != None and board_dict[l+n]['piece'] == 'king':
        if board_dict[l+n]['color'] == 'white':
          king_locations['white'] = l+n
        else:
          king_locations['black'] = l+n

#if the king moves two squares (this is determined as legal or not in determine_castling_rights()), moves the rook to the correct place
def castle_if_played(starting_position, new_position):
  if starting_position == 'e1' and new_position == 'g1':
    board_dict['f1'] = board_dict['h1']
    board_dict['f1']['moved'] = True
    board_dict['h1'] = None
  elif starting_position == 'e1' and new_position == 'c1':
    board_dict['d1'] = board_dict['a1']
    board_dict['d1']['moved'] = True
    board_dict['a1'] = None
  elif starting_position == 'e8' and new_position == 'g8':
    board_dict['f8'] = board_dict['h8']
    board_dict['f8']['moved'] = True
    board_dict['h8'] = None
  elif starting_position == 'e8' and new_position == 'c8':
    board_dict['d8'] = board_dict['a8']
    board_dict['d8']['moved'] = True
    board_dict['a8'] = None

#checks if a pawn advances from the 7th to 8th rank
def check_for_promotion(new_position):
  if board_dict[new_position]['piece'] == 'pawn':
    if new_position[1] == '8':
      piece = request_promotion()
      board_dict[new_position] = {'piece': piece, 'color': 'white', 'moved': True}
    elif new_position[1] == '1':
      piece = request_promotion()
      board_dict[new_position] = {'piece': piece, 'color': 'black', 'moved': True}

#asks user for a piece to promote their pawn to
def request_promotion():
  promotion_options = ['night', 'bishop', 'rook', 'queen']
  piece = input(f"What piece would you like to promote your pawn to? Valid pieces are: {promotion_options} ")
  while piece not in promotion_options:
    piece = input(f"{piece} is not a valid piece. Valid pieces are: {promotion_options} ")
  return piece

#checks if en passant is legal, and returns legal en passant moves
def check_for_en_passant(starting_position):
  legal_moves = []
  if board_dict[starting_position]['piece'] == 'pawn':
    if turn == 'white':
      if starting_position[1] == '5':
        previous_move = moves_dict[move_count-1]['black']
        letter_index = letters.index(starting_position[0])
        if previous_move[0] == letters[letter_index-1]:
          legal_moves.append(letters[letter_index-1]+'6')
        elif previous_move[0] == letters[letter_index+1]:
          legal_moves.append(letters[letter_index+1]+'6')
    else: 
      if starting_position[1] == '4':
        previous_move = moves_dict[move_count]['white']
        letter_index = letters.index(starting_position[0])
        if previous_move[0] == letters[letter_index-1]:
          legal_moves.append(letters[letter_index-1]+'3')
        elif previous_move[0] == letters[letter_index+1]:
          legal_moves.append(letters[letter_index+1]+'3')
  return legal_moves

#removes the pawn that was captured en passant
def en_passant_if_played(starting_position, new_position):
  if board_dict[starting_position]['piece'] == 'pawn':
    if turn == 'white':
      if starting_position[0] != new_position[0]:
        if board_dict[new_position] == None:
          board_dict[new_position[0]+str(int(new_position[1])-1)] = None
    else:
      if starting_position[0] != new_position[0]:
        if board_dict[new_position] == None:
          board_dict[new_position[0]+str(int(new_position[1])+1)] = None

#updates the global turn variable
def change_turn():
  global turn, move_count
  if turn == 'white': turn = 'black'; 
  else: turn = 'white'; move_count += 1

#updates a dictionary of the moves played. 
def record_move(starting_position, new_position):
  try:
    if turn == 'white':
      moves_dict[move_count] = {'white': starting_position+new_position, 'black': ''}
    else:
      moves_dict[move_count]['black'] = starting_position+new_position
  except:
    print('error adding move to move_dict')

#checks for checkmate, may add draws later
def check_for_game_end():
  if len(legal_moves_of_color(turn, king_locations, board_dict)) == 0:
    global game_end
    game_end = True
    change_turn()
    print(f"Checkmate, {turn} wins.")
    again = input(f"\nWould you like to play again? Enter 'y' or 'n': ")
    if again == 'y':
      reset()
    
#resets the necessary global variables, and recalls main(), effectively restarting the program
def reset():
  global turn, game_end
  turn = 'white'
  game_end = False
  main()

main()