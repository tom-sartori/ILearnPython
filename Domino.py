class Domino:

    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def isDouble(self):
        """
        :return: True if the domino is a double, False otherwise.
        """
        return self.left == self.right

    def turn(self):
        """
        Turn the domino.
        """
        memory = self.left
        self.left = self.right
        self.right = memory

    def contains(self, value: int):
        """
        :param: value: The value to check.
        :return: True if the domino contains the value, False otherwise.
        """
        return self.left == value or self.right == value

    def __str__(self):
        """
        :return: The string representation of the domino. Example: [1|2]
        """
        return "[" + str(self.left) + "|" + str(self.right) + "]"

    @staticmethod
    def createDominoList() -> []:
        """
        :return: A list of all the possible dominos, with a maximum value of 6.
        """
        domino_list = []

        max_value = 6
        for i in range(max_value + 1):
            for j in range(i, max_value + 1):
                domino_list.append(Domino(i, j))

        return domino_list

    @staticmethod
    def getMaxDouble(domino_list: []) -> int:
        """
        :param: domino_list: The list of dominos to check.
        :return: The maximum value of the double in the list. -1 if there is no double.
        """
        max_double = -1
        for domino in domino_list:
            if domino.isDouble():
                max_double = max(max_double, domino.left)

        return max_double
