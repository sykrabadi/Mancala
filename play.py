# File: Player.py


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            print "move: {} score : {}".format(m, s)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
   
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0


    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        #returns the score and the associated moved
        move = -1
        alpha = -INFINITY
        beta  = INFINITY
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board) #don't want to actually make move
            #make a new board
            nb.makeMove(self, m) #test each move
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minAb(nb, ply-1, turn, alpha, beta)
            #print "move: {} score : {}".format(m, s)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(score, alpha)
        #return the best score and move so far
        return score, move

    def minAb(self, state, ply, turn, alpha, beta):
        """ Find the ABpruning value for the next move for this player
            at a given board configuation. Returns score."""
        #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN

        #termination case: check if game is over
        if state.gameOver():
            return turn.score(state)
        score = INFINITY
        #create opponent player
        opponent = Player(self.opp, self.type, self.ply)
        #iterate through possible legal moves given present position
        for m in state.legalMoves(self):
            if ply == 0:
                return turn.score(state)
            #copy board for testing
            nextBoard = deepcopy(state)
            #test move
            nextBoard.makeMove(self, m)
            score = min(score, opponent.maxAb(nextBoard, ply-1, turn, alpha, beta))
            #prune
            if score <= alpha:
                # print "pruning"
                return score
            else:
                beta = min(beta, score)
        return score

    def maxAb(self, state, ply, turn, alpha, beta):
        """ Find the ABpruning value for the next move for this player
            at a given board configuation. Returns score."""
        #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN

        #termination case: check if game is over
        if state.gameOver():
            return turn.score(state)
        score = -INFINITY
        #create opponent player
        opponent = Player(self.opp, self.type, self.ply)
        #iterate through possible legal moves given present position
        for m in state.legalMoves(self):
            if ply == 0:
                return turn.score(state)
            #copy board for testing
            nextBoard = deepcopy(state)
            #test move
            nextBoard.makeMove(self, m)   
            score = max(score, opponent.minAb(nextBoard, ply-1, turn, alpha, beta))
            #prune
            if score >= beta:
                # print "pruning"
                return score
            else:
                alpha = max(alpha, score)
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print board.scoreCups
            print "score is"
            print self.score(board)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.minimaxMove(board, self.ply)
            print "minimax would choose move", move, "with value", val
            val, move = self.alphaBetaMove(board, self.ply)
            print "ab pruning chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            #sets ply to be 7, uses ABpruning and our improved heuristic
            val, move = self.alphaBetaMove(board, 7)
            print "ab pruning chose move", move, " with value", val
            return move
        
        
        else:
            print "Unknown player type"
            return -1





class play(Player):
    

    def score(self, board):
        """ Evaluate the Mancala board for this player. the way we are doing our heuristic is by breaking
        everything down into three categories. The first category is how many marbles you have on your side
        as a percentage of how many marbles your opponent has. 
        The next category is how marbles you have in your mancala compared to how many your opponent has
        the lastly is how many cups of yours are empty and the opposing player has marbles in them. Then we place
        weights on all three to calculate a new heuristic.
        Furthermore, we also have base cases to ensure that we dont obtain a divide by 0 error but if that does happen
        we still use two out of the other three categories to calculate our heuristic. """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        
        #sets variable for total marbles for P1,P2, and board
        player1marbles = sum(board.P1Cups)
        player2marbles = sum(board.P2Cups)
        total_marbles = player1marbles + player2marbles
        #initializes variable for how many empty cups on the given player's side
        empty = 0
        
        #player one
        if self.num == 1:
            #counts how many empty cups are on player 1's side that are across from nonempty cups
            for x in range(0,6):
                if board.P1Cups[x] == 0 and board.P2Cups[5-x] != 0:
                    empty += 1
        
            #percentage of beneficially empty cups
            empty_portion = (float(empty)/5.0) * 100
            
            #if score cups are not empty, calculate % of the score that is Player 1's
            if board.scoreCups[0]+ board.scoreCups[1] != 0:
                endcups_portion = (float(board.scoreCups[0])/float(board.scoreCups[0]+ board.scoreCups[1]))*100
            else:
                endcups_portion = 0
            
            #if game is not over
            if total_marbles != 0:
                #calculate % of remaining marbles on Player 1's side
                boardcups_portion = (float(player1marbles)/float(total_marbles))*100
            else:
                boardcups_portion = 0
            #calculate total score to be returned: weighting each contributing factor appropriately
            total_score = endcups_portion * .5 + boardcups_portion * .25 + empty_portion * .25
            return total_score

        #player 2
        elif self.num == 2:
            #counts how many empty cups are on player 2's side that are across from nonempty cups
            for x in range(0,6):
                if board.P2Cups[x] == 0 and board.P1Cups[5-x] != 0:
                    empty += 1
        
            #percentage of beneficially empty cups
            empty_portion = ((float(empty))/5.0) * 100
            
            #if score cups are not empty, calculate % of the score that is Player 2's
            if board.scoreCups[0]+ board.scoreCups[1] != 0:
                endcups_portion = (float(board.scoreCups[1])/float(board.scoreCups[0]+ board.scoreCups[1]))*100
            else:
                endcups_portion = 0
            
            #if game is not empty
            if total_marbles != 0:
                #calculate % of remaining marbles on Player 2's side
                boardcups_portion = (float(player2marbles)/float(total_marbles))*100
            else:
                boardcups_portion = 0
            
            #calculate total score to be returned: weighting each contributing factor appropriately
            total_score = endcups_portion * .5 + boardcups_portion * .25 + empty_portion * .25
            return total_score
