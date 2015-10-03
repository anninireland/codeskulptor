"""
Solitaire Mancala Game
Built by Lisa Cavern as part of Principles of Computing (Rice Universtiy) on Coursera 
https://www.coursera.org/course/principlescomputing1

Goal: Move all seeds from given houses into the store.
In the GUI, you may ask computer AI to make move or click on a house to attempt a legal move

In Solitaire Mancala, the player has six houses and a store. 
At the start of a game, a variable number of seeds are placed in each 
house (as opposed to the three seeds per house in two-player Mancala). 
As in two-player Mancala, the player may select a house and gather all 
of the seeds in that house. The player then places the seeds one at time 
in the houses to the right of the selected house. 
The last seed MUST be placed in the store.

Note: 
GUI for this game was NOT developed by Lisa Cavern, but provided 
as part of the template for the game. Original template is here: 
http://www.codeskulptor.org/#poc_mancala_template.py

"""

class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = configuration[::-1]

    def __str__(self):
        """
        Return string representation for Mancala board
        """
        #return ''.join(str(e) for e in self._board)
        return str(self._board)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[-1-house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        all_empty = True
    
        for h in range(1,len(self._board)):
            if self.get_num_seeds(h) != 0:
                all_empty = False
        return all_empty
               
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        Return True if moving the seeds from house house_num is legal. 
        Otherwise, return False. 
        If house_num is zero, is_legal_move should return False.
        """
        if house_num == 0:
            return False
        elif self.get_num_seeds(house_num) == house_num:
            return True
        else:
            return False

    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num) == True:
            # get copy of board
            temp_board = self._board[::-1]
            
            # set house_num to 0
            temp_board[house_num] = 0
            
            # add 1 to each lower house and store 
            for e in range(house_num):
                temp_board[e] += 1
            self.set_board(temp_board[::])

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        next_move = 0
        for h in range(1,len(self._board)):
            if self.is_legal_move(h):
                next_move = h
                break
        return next_move
        
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        moves_plan = []
        current_board = self._board[:]
        while self.choose_move() != 0:
            next_move = self.choose_move()
            moves_plan.append(next_move)
            self.apply_move(next_move)
            current_board = self._board[:]
        return moves_plan

# import user40_U3Iq1wUVB9_8 as poc_mancala_testsuite
# poc_mancala_testsuite.run_suite(SolitaireMancala)

# Import and run GUI to visualise game
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())
