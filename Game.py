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
        self.isPlayer1ToPlay: bool = True  # Will be set in self.newGame().

        self.newGame()

    def __getLeftExtremity(self) -> Domino or None:
        """
        :return: The left extremity of the played dominos.
        """
        if len(self.domino_played_list):
            return self.domino_played_list[0].left
        else:
            return None

    def __getRightExtremity(self) -> Domino or None:
        """
        :return: The right extremity of the played dominos.
        """
        if len(self.domino_played_list):
            return self.domino_played_list[-1].right
        else:
            return None

    def __canPlay(self, domino: Domino, side: Side):
        """
        :param: domino: The domino to play.
        :param: side: The side to play the domino.
        :return: True if the domino can be played, False otherwise.
        """
        if side == Side.LEFT:
            return (not self.__getLeftExtremity()) or self.__getLeftExtremity() == domino.right
        elif side == Side.RIGHT:
            return (not self.__getRightExtremity()) or self.__getRightExtremity() == domino.left
        else:
            return False

    def __currentPlayerCanPlay(self) -> bool:
        """
        :return: True if the current player can play, False otherwise.
        """
        for domino in self.__getCurrentPlayerList():
            if domino.contains(self.__getLeftExtremity()) or domino.contains(self.__getRightExtremity()):
                return True
        return False

    def __getCurrentPlayerList(self) -> [Domino]:
        """
        :return: The list of dominos of the current player.
        """
        if self.isPlayer1ToPlay:
            return self.player1_list
        else:
            return self.player2_list

    def put(self, domino: Domino, side: Side) -> bool:
        """
        :param: domino: The domino to play.
        :param: side: The side to play the domino.
        :return: True if the domino has been played, False otherwise.
        """
        if self.__canPlay(domino, side):
            self.__removeDominoFromCurrentPlayer(domino)
            if side == Side.LEFT:
                self.domino_played_list.insert(0, domino)
            elif side == Side.RIGHT:
                self.domino_played_list.append(domino)
            return True
        else:
            return False

    def currentPlayerTakeACard(self):
        """
        The current player takes a card from the stock. So it adds a card to its list of dominos.
        """
        if len(self.domino_stock_list):
            domino = self.domino_stock_list[0]
            self.domino_stock_list = self.domino_stock_list[1::]
            self.__getCurrentPlayerList().append(domino)

    def __shuffleDominoStock(self):
        """
        Shuffle the domino stock.
        """
        random.shuffle(self.domino_stock_list)

    def __setFirstPlayer(self):
        """
        Set the first player to play. The player with the highest double will play first.
        If there is no double, a random player is chosen.
        """
        max_double_player_1 = Domino.getMaxDouble(self.player1_list)
        max_double_player_2 = Domino.getMaxDouble(self.player2_list)

        if max_double_player_1 == -1 and max_double_player_2 == -1:
            self.isPlayer1ToPlay = bool(random.getrandbits(1))
        else:
            self.isPlayer1ToPlay = max_double_player_1 > max_double_player_2

    def newGame(self):
        """
        Start a new game. The stock is shuffled and the players are given 6 dominos.
        """
        self.domino_stock_list = Domino.createDominoList()
        self.__shuffleDominoStock()

        self.domino_played_list = []
        self.domino_played_list.append(self.domino_stock_list[0])
        self.domino_stock_list = self.domino_stock_list[1::]

        nb_cards = 6
        self.player1_list = self.domino_stock_list[:nb_cards]
        self.player2_list = self.domino_stock_list[nb_cards:nb_cards * 2]
        self.domino_stock_list = self.domino_stock_list[nb_cards * 2::]

        self.__setFirstPlayer()

    def __getCurrentDomino(self, index: int) -> Domino:
        """
        :param: index: The index of the domino to get in the current player list of dominos.
        :return: The domino at the given index.
        """
        return self.__getCurrentPlayerList()[index]

    def __removeDominoFromCurrentPlayer(self, domino: Domino):
        """
        Remove the given domino from the current player list of dominos.
        """
        self.__getCurrentPlayerList().remove(domino)

    def __getScorePlayer(self, player: int) -> int:
        """
        :param: player: The player to get the score. 1 or 2.
        :return: The score of the given player. Make a sum of the values of the dominos.
        """
        score = 0
        player_domino_list: [Domino] = []
        if player == 1:
            player_domino_list = self.player1_list
        elif player == 2:
            player_domino_list = self.player2_list

        for domino in player_domino_list:
            score += domino.left + domino.right
        return score

    def __getWinner(self) -> int:
        """
        :return: The winner of the game. 1 or 2.
        """
        if not len(self.player1_list):
            return 1
        elif not len(self.player2_list):
            return 2
        else:
            return 1 if self.__getScorePlayer(1) < self.__getScorePlayer(2) else 2

    def play(self):
        """
        Play the game. The game is played until one of the players has won.
        """
        print('Welcome to this game!\n')
        print(self)

        while len(self.domino_stock_list) and len(self.player1_list) and len(self.player2_list):
            print('Player ' + ('1' if self.isPlayer1ToPlay else '2'))

            if self.__currentPlayerCanPlay():
                index_domino: int = -1
                while index_domino < 0 or len(self.__getCurrentPlayerList()) <= index_domino:
                    index_domino = utils.askUserForNumber('\tEnter the index of the domino you want : ')
                # 0 <= index_domino < len(self.__getCurrentPlayerList()):
                domino: Domino = self.__getCurrentDomino(index_domino)

                if utils.askUserForBool('\tDo you wanna turn the domino ? (y or n) : '):
                    domino.turn()

                side: Side = utils.askUserForSide('\tEnter the side where you wanna add the domino (l or r) : ')

                if not self.put(domino, side):
                    print('\tThis move is invalid. You take a card. ')
                    self.currentPlayerTakeACard()

            else:
                print('\tYou can not play. You take a card. ')
                self.currentPlayerTakeACard()

            print()
            self.isPlayer1ToPlay = not self.isPlayer1ToPlay
            print(self)

        print('The player ' + self.__getWinner().__str__() + ' has won. ')
        if utils.askUserForBool('The party is over. Do you wanna play again ? (y or n) : '):
            self.newGame()
            self.play()
        else:
            print("See you!")

    def __str__(self):
        """
        :return: A string representation of the game.
        """
        result = 'Dominos in stock : '
        result += utils.toString(self.domino_stock_list)

        result += "Player 1 dominos : "
        result += utils.toString(self.player1_list)

        result += "Player 2 dominos : "
        result += utils.toString(self.player2_list)

        result += "Played dominos : "
        result += utils.toString(self.domino_played_list)

        return result
