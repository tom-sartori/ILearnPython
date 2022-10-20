import random

import utils
from Domino import Domino
from Side import Side


class Game:

    def __init__(self):
        self.domino_stock_list: [Domino] = None
        self.domino_played_list: [Domino] = None
        self.player1_list: [Domino] = None
        self.player2_list: [Domino] = None
        self.isPlayer1ToPlay: bool = True   # Will be set in self.newGame().

        self.newGame()

    def __getLeftExtremity(self) -> Domino or None:
        if len(self.domino_played_list):
            return self.domino_played_list[0].left
        else:
            return None

    def __getRightExtremity(self) -> Domino or None:
        if len(self.domino_played_list):
            return self.domino_played_list[-1].right
        else:
            return None

    def __canPlay(self, domino: Domino, side: Side):
        if side == Side.LEFT:
            return (not self.__getLeftExtremity()) or self.__getLeftExtremity() == domino.right
        elif side == Side.RIGHT:
            return (not self.__getRightExtremity()) or self.__getRightExtremity() == domino.left
        else:
            return False

    def put(self, domino: Domino, side: Side) -> bool:
        if self.__canPlay(domino, side):
            self.__removeDominoFromCurrentPlayer(domino)
            if side == Side.LEFT:
                self.domino_played_list.insert(0, domino)
            elif side == Side.RIGHT:
                self.domino_played_list.append(domino)
            return True
        else:
            return False

    def takeACard(self):
        if len(self.domino_stock_list):
            domino = self.domino_stock_list[0]
            self.domino_stock_list = self.domino_stock_list[1::]
            if self.isPlayer1ToPlay:
                self.player1_list.append(domino)
            else:
                self.player2_list.append(domino)

    def __shuffleDominoStock(self):
        random.shuffle(self.domino_stock_list)

    def __setFirstPlayer(self):
        max_double_player_1 = Domino.getMaxDouble(self.player1_list)
        max_double_player_2 = Domino.getMaxDouble(self.player2_list)

        if max_double_player_1 == -1 and max_double_player_2 == -1:
            self.isPlayer1ToPlay = bool(random.getrandbits(1))
        else:
            self.isPlayer1ToPlay = max_double_player_1 > max_double_player_2

    def newGame(self):
        self.domino_stock_list = Domino.createDominoList()
        self.__shuffleDominoStock()
        self.domino_played_list = []

        nb_cards = 6
        self.player1_list = self.domino_stock_list[:nb_cards]
        self.player2_list = self.domino_stock_list[nb_cards:nb_cards * 2]
        self.domino_stock_list = self.domino_stock_list[nb_cards * 2::]

        self.__setFirstPlayer()

    def __getCurrentDomino(self, index: int) -> Domino:
        if self.isPlayer1ToPlay:
            return self.player1_list[index]
        else:
            return self.player2_list[index]

    def __removeDominoFromCurrentPlayer(self, domino: Domino):
        if self.isPlayer1ToPlay:
            self.player1_list.remove(domino)
        else:
            self.player2_list.remove(domino)

    def play(self):
        print('Welcome to this game!\n')
        print(self)
        consecutive_fail: int = 0   # If users make three consecutive fails, the party stops.

        while len(self.domino_stock_list) and consecutive_fail < 3:
            print('Player ' + ('1' if self.isPlayer1ToPlay else '2'))

            index_domino: int = utils.askUserForNumber('\tEnter the index of the domino you want : ')
            domino: Domino = self.__getCurrentDomino(index_domino)

            if utils.askUserForBool('\tDo you wanna turn the domino ? (y or n) : '):
                domino.turn()

            side: Side = utils.askUserForSide('\tEnter the side where you wanna add the domino (l or r) : ')

            if not self.put(domino, side):
                print('\tThis move is invalid. You take a cart. ')
                consecutive_fail += 1
                self.takeACard()
            else:
                # Valid move.
                consecutive_fail = 0
            print()
            self.isPlayer1ToPlay = not self.isPlayer1ToPlay
            print(self)

        if utils.askUserForBool('The party is over. Do you wanna play again ? (y or n) : '):
            self.newGame()
            self.play()
        else:
            print("See you!")

    def __str__(self):
        result = 'Dominos in stock : '
        result += utils.toString(self.domino_stock_list)

        result += "Player 1 dominos : "
        result += utils.toString(self.player1_list)

        result += "Player 2 dominos : "
        result += utils.toString(self.player2_list)

        result += "Played dominos : "
        result += utils.toString(self.domino_played_list)

        return result
