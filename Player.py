from Board import BoardUtility
import random
import time
import math

class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def move_visual(self, gameboard, col, piece):
        game_board = gameboard.copy()
        row = BoardUtility.get_next_open_row(game_board, col)
        assert game_board[row][col] == 0
        game_board[row][col] = piece
        return game_board

    def makeTree(self, root, piece, dep, ismax):
        if (dep == -1):
            return
        if(BoardUtility.has_player_won(root['board'],self.piece) or BoardUtility.has_player_won(root['board'],3+(-1)*self.piece)):
            return root

        for column in BoardUtility.get_valid_locations(root['board']):
            temp = {'childrens': [], 'board': self.move_visual(root['board'], column, piece), 'move': column, 'val': None,
                    'is_valed': False, 'ismax': not ismax}
            temp = self.makeTree(temp, int(-1 * piece + 3), dep - 1, not ismax)
            if (temp != None):
                root['childrens'].append(temp.copy())
        return root

    def minimax(self, node, alpha, beta):
        if len(node['childrens']) == 0:
            return BoardUtility.score_position(node['board'], self.piece)
        if not node['ismax']:
            for i in range(len(node['childrens'])):
                val = self.minimax(node['childrens'][i], alpha, beta)

                beta = min(beta, val)
                if beta <= alpha:
                    return beta
            return beta
        if node['ismax']:
            for i in range(len(node['childrens'])):
                val = self.minimax(node['childrens'][i], alpha, beta)
                alpha = max(alpha, val)
                if beta <= alpha:
                    return alpha
            return alpha

    def temp(self, node, alpha, beta):
        if node['ismax']:
            for i in range(len(node['childrens'])):
                val = self.minimax(node['childrens'][i], alpha, beta)
                alpha = max(alpha, val)
                node['childrens'][i]['val'] = val
                node['childrens'][i]['is_valed'] = True

                # print(node['childrens'][0])
                if beta <= alpha:
                    return alpha,node
            return alpha,node
    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return random.choice(BoardUtility.get_valid_locations(board))


class HumanPlayer(Player):
    def play(self, board):
        move = int(input("input the next column index 0 to 8:"))
        return move


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def play(self, board):
        """
        Inputs :
           board : 7*9 numpy array. 0 for empty cell, 1 and 2 for cells containig a piece.
        return the next move(columns to play in) of the player based on minimax algorithm.
        """
        # Todo: implement minimax algorithm with alpha beta pruning
        root = {'childrens': [], 'board': board, 'move': -1, 'val': 0, 'is_valed': False, 'ismax':True}
        root = self.makeTree(root, self.piece, self.depth,True)
        b, Node = self.temp(root,-math.inf,math.inf)

        max_val = -math.inf
        move = -1

        for node in Node['childrens']:
            if (  node['val']!= max_val and node['val']==b ):
                max_val = node['val']
                move = node['move']
        return move


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic


    def play(self, board):
        """
        Inputs :
           board : 7*9 numpy array. 0 for empty cell, 1 and 2 for cells containig a piece.
        same as above but each time you are playing as max choose a random move instead of the best move
        with probability self.prob_stochastic.
        """
        # Todo: implement minimax algorithm with alpha beta pruning
        root = {'childrens': [], 'board': board, 'move': -1, 'val': 0, 'is_valed': False ,'ismax':True}
        root = self.makeTree(root, self.piece, self.depth,True)
        b, Node = self.temp(root,-math.inf,math.inf)


        max_val = -math.inf
        move = -1
        r = random.random()
        if (r >= self.prob_stochastic):
            for node in Node['childrens']:
                if (node['val'] > max_val and node['is_valed']):
                    max_val = node['val']
                    move = node['move']
            return move
        else:
            index = random.randrange(len(root['childrens']))
            return root['childrens'][index]['move']

