class Domino:

    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def isDouble(self):
        return self.left == self.right

    def turn(self):
        memory = self.left
        self.left = self.right
        self.right = memory

    def contains(self, value: int):
        return self.left == value or self.right == value

    def __str__(self):
        return "[" + str(self.left) + "|" + str(self.right) + "]"

    @staticmethod
    def createDominoList() -> []:
        domino_list = []

        max_value = 6
        for i in range(max_value + 1):
            for j in range(i, max_value + 1):
                domino_list.append(Domino(i, j))

        return domino_list

    @staticmethod
    def getMaxDouble(domino_list: []) -> int:
        max_double = -1
        for domino in domino_list:
            if domino.isDouble():
                max_double = max(max_double, domino.left)

        return max_double
