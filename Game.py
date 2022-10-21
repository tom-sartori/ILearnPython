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

    def __currentPlayerCanPlay(self) -> bool:
        for domino in self.__getCurrentPlayerList():
            if domino.contains(self.__getLeftExtremity()) or domino.contains(self.__getRightExtremity()):
                return True
        return False

    def __getCurrentPlayerList(self) -> [Domino]:
        if self.isPlayer1ToPlay:
            return self.player1_list
        else:
            return self.player2_list

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

    def currentPlayerTakeACard(self):
        if len(self.domino_stock_list):
            domino = self.domino_stock_list[0]
            self.domino_stock_list = self.domino_stock_list[1::]
            self.__getCurrentPlayerList().append(domino)

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
        self.domino_played_list.append(self.domino_stock_list[0])
        self.domino_stock_list = self.domino_stock_list[1::]

        nb_cards = 6
        self.player1_list = self.domino_stock_list[:nb_cards]
        self.player2_list = self.domino_stock_list[nb_cards:nb_cards * 2]
        self.domino_stock_list = self.domino_stock_list[nb_cards * 2::]

        self.__setFirstPlayer()

    def __getCurrentDomino(self, index: int) -> Domino:
        return self.__getCurrentPlayerList()[index]

    def __removeDominoFromCurrentPlayer(self, domino: Domino):
        self.__getCurrentPlayerList().remove(domino)

    def __getScorePlayer(self, player: int) -> int:
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
        if not len(self.player1_list):
            return 1
        elif not len(self.player2_list):
            return 2
        else:
            return 1 if self.__getScorePlayer(1) < self.__getScorePlayer(2) else 2

    def play(self):
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
        result = 'Dominos in stock : '
        result += utils.toString(self.domino_stock_list)

        result += "Player 1 dominos : "
        result += utils.toString(self.player1_list)

        result += "Player 2 dominos : "
        result += utils.toString(self.player2_list)

        result += "Played dominos : "
        result += utils.toString(self.domino_played_list)

        return result
