#Hayden Collins
#CS 021
#functions related to legal moves for final project
letters = ['a','b','c','d','e','f','g','h']
numbers = ['1','2','3','4','5','6','7','8']

#returns an array of all possible moves (ignoring discovered checks) for a given color
def possible_moves_of_color(color, board_dict):
  total_possible_moves = []
  for l in letters:
    for n in numbers:
      if board_dict[l+n] != None and board_dict[l+n]['color'] == color:
        total_possible_moves.append([l+n, possible_moves(l+n, board_dict)])
  return total_possible_moves

#returns an array of all legal moves for a given color
def legal_moves_of_color(color, king_locations, board_dict):
  total_legal_moves_dict = {}#this will be dict where keys are piece coordinates and values are lists of legal moves (the new position)

  possible_moves = possible_moves_of_color(color, board_dict)
  for move in possible_moves:
    for new_position in move[1]:
      if check_legal_move(move[0],new_position, king_locations, board_dict):
        if total_legal_moves_dict.get(move[0]) != None:
          total_legal_moves_dict[move[0]].append(new_position) 
        else:
          total_legal_moves_dict[move[0]] = [new_position]
  return total_legal_moves_dict

#a move that is theoretically possible may not actually be legal if it places the king in check,
#therefore we must check each possible move to avoid moving into check
#this function returns true or false for legality
def check_legal_move(starting_position, new_position, king_locations, board_dict):
  board_dict_copy = dict(board_dict)#making a true copy
  king_locations_copy = dict(king_locations)
  color = board_dict_copy[starting_position]['color']
  piece_moves = possible_moves(starting_position, board_dict_copy)
  if starting_position == king_locations_copy[color]:#if the piece moving is the king
    king_locations_copy[color] = new_position#update the king's location to the new position

  if new_position in piece_moves:#making sure the move is possible
    board_dict_copy[new_position] = board_dict_copy[starting_position]
    board_dict_copy[starting_position] = None

    if color == 'white':
      for possible_move in possible_moves_of_color('black', board_dict_copy):
        if king_locations_copy['white'] in possible_move[1]:
          return False
    else:
      for possible_move in possible_moves_of_color('white', board_dict_copy):
        if king_locations_copy['black'] in possible_move[1]:
          return False
  return True

#determines is castling is legal, and returns the valid castling squares (g1,c1,g8,c8)
def determine_castling_rights(starting_position, board_dict, king_locations):
  if board_dict[starting_position]['color'] == 'white': opposite_color_legal_moves = legal_moves_of_color('black', king_locations, board_dict)
  else: opposite_color_legal_moves = legal_moves_of_color('white', king_locations, board_dict)

  opposite_color_legal_new_positions = []
  for new_pos_list in opposite_color_legal_moves.values():
    for new_pos in new_pos_list:
      opposite_color_legal_new_positions.append(new_pos)
  castling_moves = []
  if board_dict[starting_position]['piece'] == 'king' and board_dict[starting_position]['moved'] == False:
    if board_dict[starting_position]['color'] == 'white':
      if board_dict['h1'] != None and board_dict['h1']['moved'] == False:
        if board_dict['f1'] == None and board_dict['g1'] == None:
          if 'f1' not in opposite_color_legal_new_positions and 'g1' not in opposite_color_legal_new_positions:
            castling_moves.append('g1')
      if board_dict['a1'] != None and board_dict['a1']['moved'] == False:
        if board_dict['d1'] == None and board_dict['c1'] == None:
          if 'd1' not in opposite_color_legal_new_positions and 'c1' not in opposite_color_legal_new_positions:
            castling_moves.append('c1')
    else:
      if board_dict['h8'] != None and board_dict['h8']['moved'] == False:
        if board_dict['f8'] == None and board_dict['g8'] == None:
          if 'f8' not in opposite_color_legal_new_positions and 'g8' not in opposite_color_legal_new_positions:
            castling_moves.append('g8')

      if board_dict['a8'] != None and board_dict['a8']['moved'] == False:
        if board_dict['d8'] == None and board_dict['c8'] == None:
          if 'd8' not in opposite_color_legal_new_positions and 'c8' not in opposite_color_legal_new_positions:
            castling_moves.append('c8')
  return castling_moves

#returns an array of possible moves for the given coordinate
def possible_moves(coordinate, board_dict):
  legal_moves = []
  if board_dict[coordinate]['piece'] != None:
    letter_cord = coordinate[0]
    num_cord = coordinate[1]
    letter_index = letters.index(letter_cord)
    num_index = numbers.index(num_cord)
    square = board_dict[coordinate]   

    #PAWN
    if square['piece'] == 'pawn':
      if square['color'] == 'white':#white pawns (only go up the board)
        if num_index <= 7:#pawn should never be on the 8th rank (promotion is forced)
          if board_dict[letter_cord+numbers[num_index+1]] == None:#if the square in front is empty
            legal_moves.append(letter_cord+numbers[num_index+1])#pawn can go up 1
          if square['moved'] == False:#if the pawn has not moved
            if board_dict[letter_cord+numbers[num_index+1]] == None and board_dict[letter_cord+numbers[num_index+2]] == None:#if both squares in front are empty
              legal_moves.append(letter_cord+numbers[num_index+2])#the pawn can move 2 squares
        if letter_index+1 <= 7 and num_index+1 <= 7:
          if board_dict[letters[letter_index+1]+numbers[num_index+1]] != None:#if there is a piece on square up and right 1
            if board_dict[letters[letter_index+1]+numbers[num_index+1]]['color'] != square['color']:#if that piece is the opposite color
              legal_moves.append(letters[letter_index+1]+numbers[num_index+1])
        if letter_index-1 >= 0 and num_index+1 <= 7:
          if board_dict[letters[letter_index-1]+numbers[num_index+1]] != None:#if there is a piece on square up and left 1
            if board_dict[letters[letter_index-1]+numbers[num_index+1]]['color'] != square['color']:#if that piece is the opposite color
              legal_moves.append(letters[letter_index-1]+numbers[num_index+1])
      #TODO add en passant
      #moving forwards
      if square['color'] == 'black':#black pawns (only go down the board)
        if num_index-1 >= 0:#pawn should never be on the 1st rank (promotion is forced)
          if board_dict[letter_cord+numbers[num_index-1]] == None:#if the square in front is empty
            legal_moves.append(letter_cord+numbers[num_index-1])#pawn can move down 1
          if square['moved'] == False:#if the pawn has not moved
            if board_dict[letter_cord+numbers[num_index-1]] == None and board_dict[letter_cord+numbers[num_index-2]] == None:#if squares in front are empty
              legal_moves.append(letter_cord+numbers[num_index-2])#pawn can move down 2

        #capturing down right
        if letter_index+1 <= 7 and num_index-1 >= 0:
          if board_dict[letters[letter_index+1]+numbers[num_index-1]] != None:#if there is a piece on square down and right 1
            if board_dict[letters[letter_index+1]+numbers[num_index-1]]['color'] != square['color']:#if that piece is the opposite color
              legal_moves.append(letters[letter_index+1]+numbers[num_index-1])

        #capturing down left
        if letter_index-1 >= 0 and num_index-1 >= 0:
          if board_dict[letters[letter_index-1]+numbers[num_index-1]] != None:#if there is a piece on square down and left 1
            if board_dict[letters[letter_index-1]+numbers[num_index-1]]['color'] != square['color']:#if that piece is the opposite color
              legal_moves.append(letters[letter_index-1]+numbers[num_index-1])
      #TODO add en passant

    #ROOK
    if square['piece'] == 'rook':
      i = 1
      while letter_index-i >= 0:#rook has to stay on the board
        if board_dict[letters[letter_index-i]+num_cord] != None:#if the squares to the left are not empty
          if board_dict[letters[letter_index-i]+num_cord]['color'] != square['color']:#if that piece is of opposite color
            legal_moves.append(letters[letter_index-i]+num_cord)#capture is a legal move
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+num_cord)#else if the square(s) to the left are empty, it is legal
        i += 1
      
      i = 1
      while letter_index+i <= 7:#rook has to stay on the board
        if board_dict[letters[letter_index+i]+num_cord] != None:#if the squares to the right are not empty
          if board_dict[letters[letter_index+i]+num_cord]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letters[letter_index+i]+num_cord)#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index+i]+num_cord)#if square is empty, it is legal
        i += 1
      i = 1
      while num_index-i >= 0:#rook has to stay on the board
        if board_dict[letter_cord+numbers[num_index-i]] != None:#if the squares below the rook are not empty
          if board_dict[letter_cord+numbers[num_index-i]]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letter_cord+numbers[num_index-i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else: 
          legal_moves.append(letter_cord+numbers[num_index-i])#if square is empty, it is legal
        i += 1
      i = 1
      while num_index+i <= 7:
        if board_dict[letter_cord+numbers[num_index+i]] != None:#if the squares above the rook are not empty
          if board_dict[letter_cord+numbers[num_index+i]]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letter_cord+numbers[num_index+i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letter_cord+numbers[num_index+i])#if square is empty, it is legal
        i += 1

    #KNIGHT
    if square['piece'] == 'night':
      #possible coordinate moves: +1,+2; -1,+2; -2,+1; -2,-1; -1,-2; +1,-2; +2,-1; +2;+1
      #unfortunately, I'm not sure of a way to use loops for the knight moves, so it has to be hardcoded.
      #+1, +2
      if letter_index+1 <= 7 and num_index+2 <=7:#if the potential move is on the board
        if board_dict[letters[letter_index+1]+numbers[num_index+2]] != None:#if there is a piece there
          if board_dict[letters[letter_index+1]+numbers[num_index+2]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index+1]+numbers[num_index+2])#capture is legal
        else: 
          legal_moves.append(letters[letter_index+1]+numbers[num_index+2])#if empty, move is legal
      #-1, +2
      if letter_index-1 >= 0 and num_index+2 <=7:#if the potential move is on the board
        if board_dict[letters[letter_index-1]+numbers[num_index+2]] != None:#if there is a piece there
          if board_dict[letters[letter_index-1]+numbers[num_index+2]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index-1]+numbers[num_index+2])#capture is legal
        else: 
          legal_moves.append(letters[letter_index-1]+numbers[num_index+2])#if empty, move is legal
      #-2, +1
      if letter_index-2 >= 0 and num_index+1 <=7:#if the potential move is on the board
        if board_dict[letters[letter_index-2]+numbers[num_index+1]] != None:#if there is a piece there
          if board_dict[letters[letter_index-2]+numbers[num_index+1]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index-2]+numbers[num_index+1])#capture is legal
        else: 
          legal_moves.append(letters[letter_index-2]+numbers[num_index+1])#if empty, move is legal
      #-2, -1
      if letter_index-2 >= 0 and num_index-1 >= 0:#if the potential move is on the board
        if board_dict[letters[letter_index-2]+numbers[num_index-1]] != None:#if there is a piece there
          if board_dict[letters[letter_index-2]+numbers[num_index-1]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index-2]+numbers[num_index-1])#capture is legal
        else: 
          legal_moves.append(letters[letter_index-2]+numbers[num_index-1])#if empty, move is legal
      #-1, -2
      if letter_index-1 >= 0 and num_index-2 >= 0:#if the potential move is on the board
        if board_dict[letters[letter_index-1]+numbers[num_index-2]] != None:#if there is a piece there
          if board_dict[letters[letter_index-1]+numbers[num_index-2]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index-1]+numbers[num_index-2])#capture is legal
        else: 
          legal_moves.append(letters[letter_index-1]+numbers[num_index-2])#if empty, move is legal
      #+1, -2
      if letter_index+1 <= 7 and num_index-2 >= 0:#if the potential move is on the board
        if board_dict[letters[letter_index+1]+numbers[num_index-2]] != None:#if there is a piece there
          if board_dict[letters[letter_index+1]+numbers[num_index-2]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index+1]+numbers[num_index-2])#capture is legal
        else: 
          legal_moves.append(letters[letter_index+1]+numbers[num_index-2])#if empty, move is legal
      #+2, -1
      if letter_index+2 <= 7 and num_index-1 >= 0:#if the potential move is on the board
        if board_dict[letters[letter_index+2]+numbers[num_index-1]] != None:#if there is a piece there
          if board_dict[letters[letter_index+2]+numbers[num_index-1]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index+2]+numbers[num_index-1])#capture is legal
        else: 
          legal_moves.append(letters[letter_index+2]+numbers[num_index-1])#if empty, move is legal
      #+2, +1
      if letter_index+2 <= 7 and num_index+1 <=7:#if the potential move is on the board
        if board_dict[letters[letter_index+2]+numbers[num_index+1]] != None:#if there is a piece there
          if board_dict[letters[letter_index+2]+numbers[num_index+1]]['color'] != square['color']:#if the piece is of opposite color
            legal_moves.append(letters[letter_index+2]+numbers[num_index+1])#capture is legal
        else: 
          legal_moves.append(letters[letter_index+2]+numbers[num_index+1])#if empty, move is legal

    #BISHOP
    if square['piece'] == 'bishop':
      #up right diagonal
      i = 1
      while letter_index+i <= 7 and num_index+i <= 7:#while the potential move is on the board
        if board_dict[letters[letter_index+i]+numbers[num_index+i]] != None:#if there is a piece there
          if board_dict[letters[letter_index+i]+numbers[num_index+i]]['color'] != square['color']:#if it is opposite color
            legal_moves.append(letters[letter_index+i]+numbers[num_index+i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index+i]+numbers[num_index+i])#if square is empty, move is legal
        i += 1

      #down left diagonal
      i = 1
      while letter_index-i >= 0 and num_index-i >= 0:
        if board_dict[letters[letter_index-i]+numbers[num_index-i]] != None:
          if board_dict[letters[letter_index-i]+numbers[num_index-i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index-i]+numbers[num_index-i])
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+numbers[num_index-i])
        i += 1
      
      #up left diagonal
      i = 1
      while letter_index-i >= 0 and num_index+i <= 7:
        if board_dict[letters[letter_index-i]+numbers[num_index+i]] != None:
          if board_dict[letters[letter_index-i]+numbers[num_index+i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index-i]+numbers[num_index+i])
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+numbers[num_index+i])
        i += 1

      #down right diagonal
      i = 1
      while letter_index+i <= 7 and num_index-i >= 0:
        if board_dict[letters[letter_index+i]+numbers[num_index-i]] != None:
          if board_dict[letters[letter_index+i]+numbers[num_index-i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index+i]+numbers[num_index-i])
          break#stops loop because a piece cannot continue through another piece          
        else:
          legal_moves.append(letters[letter_index+i]+numbers[num_index-i])
        i += 1
      
    #QUEEN
    if square['piece'] == 'queen':
      #queen can move like a rook

      #left
      i = 1
      while letter_index-i >= 0:#queen has to stay on the board
        if board_dict[letters[letter_index-i]+num_cord] != None:#if the squares to the left are not empty
          if board_dict[letters[letter_index-i]+num_cord]['color'] != square['color']:#if that piece is of opposite color
            legal_moves.append(letters[letter_index-i]+num_cord)#capture is a legal move
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+num_cord)#else if the square(s) to the left are empty, it is legal
        i += 1

      #right
      i = 1
      while letter_index+i <= 7:#queen has to stay on the board
        if board_dict[letters[letter_index+i]+num_cord] != None:#if the squares to the right are not empty
          if board_dict[letters[letter_index+i]+num_cord]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letters[letter_index+i]+num_cord)#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index+i]+num_cord)#if square is empty, it is legal
        i += 1
      
      #down
      i = 1
      while num_index-i >= 0:#queen has to stay on the board
        if board_dict[letter_cord+numbers[num_index-i]] != None:#if the squares below the rook are not empty
          if board_dict[letter_cord+numbers[num_index-i]]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letter_cord+numbers[num_index-i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else: 
          legal_moves.append(letter_cord+numbers[num_index-i])#if square is empty, it is legal
        i += 1

      #up
      i = 1
      while num_index+i <= 7:#queen has to stay on the board
        if board_dict[letter_cord+numbers[num_index+i]] != None:#if the squares above the rook are not empty
          if board_dict[letter_cord+numbers[num_index+i]]['color'] != square['color']:#if that piece is opposite color
            legal_moves.append(letter_cord+numbers[num_index+i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letter_cord+numbers[num_index+i])#if square is empty, it is legal
        i += 1
      #queen can also move like a bishop

      #up right diagonal
      i = 1
      while letter_index+i <= 7 and num_index+i <= 7:#while the potential move is on the board
        if board_dict[letters[letter_index+i]+numbers[num_index+i]] != None:#if there is a piece there
          if board_dict[letters[letter_index+i]+numbers[num_index+i]]['color'] != square['color']:#if it is opposite color
            legal_moves.append(letters[letter_index+i]+numbers[num_index+i])#capture is legal
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index+i]+numbers[num_index+i])#if square is empty, move is legal
        i += 1

      #down left diagonal
      i = 1
      while letter_index-i >= 0 and num_index-i >= 0:
        if board_dict[letters[letter_index-i]+numbers[num_index-i]] != None:
          if board_dict[letters[letter_index-i]+numbers[num_index-i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index-i]+numbers[num_index-i])
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+numbers[num_index-i])
        i += 1
      
      #up left diagonal
      i = 1
      while letter_index-i >= 0 and num_index+i <= 7:
        if board_dict[letters[letter_index-i]+numbers[num_index+i]] != None:
          if board_dict[letters[letter_index-i]+numbers[num_index+i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index-i]+numbers[num_index+i])
          break#stops loop because a piece cannot continue through another piece
        else:
          legal_moves.append(letters[letter_index-i]+numbers[num_index+i])
        i += 1

      #down right diagonal
      i = 1
      while letter_index+i <= 7 and num_index-i >= 0:
        if board_dict[letters[letter_index+i]+numbers[num_index-i]] != None:
          if board_dict[letters[letter_index+i]+numbers[num_index-i]]['color'] != square['color']:
            legal_moves.append(letters[letter_index+i]+numbers[num_index-i])
          break#stops loop because a piece cannot continue through another piece          
        else:
          legal_moves.append(letters[letter_index+i]+numbers[num_index-i])
        i += 1
      
    #KING
    if square['piece'] == 'king': 
      for i in range(-1,2):
        for j in range(-1,2):
          if letter_index+i <= 7 and num_index+j <= 7 and letter_index+i >=0 and num_index+j >= 0:
            if board_dict[letters[letter_index+i]+numbers[num_index+j]] != None:
              if board_dict[letters[letter_index+i]+numbers[num_index+j]]['color'] != square['color']:
                legal_moves.append(letters[letter_index+i]+numbers[num_index+j])
            else:
              legal_moves.append(letters[letter_index+i]+numbers[num_index+j])
  return legal_moves  