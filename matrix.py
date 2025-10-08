from copy import deepcopy

class Matrix:
    def __init__(self, matrix: [[float]]):
        if type(matrix) != list and type(matrix[0]) != list and type(matrix[0][0]) not in [float, int]:
            raise "matrix er ikke en nested list af floats"
        self.matrix = matrix

    def transponere(self):
        pass

    def rækker(self):
        return len(self.matrix)

    def søjler(self):
        return len(self.matrix[0])

    def få_søjler(self):
        for i in range(self.søjler()):
            søjle = []
            for j in range(self.rækker()):
                søjle.append(self.matrix[j][i])
            yield søjle


    def __repr__(self):
        s = "Matrix(\n"
        for række in self.matrix:
            s = s + f"  {række}\n"
        s = s + ")"
        return s

    def __add__(self, other):
        matrix = deepcopy(self.matrix)

        # tjekker om det er et tal
        if type(other) in [float, int]:
            for række in range(self.rækker()):
                for søjle in range(self.søjler()):
                    matrix[række][søjle] = matrix[række][søjle] + other
            return Matrix(matrix)

        if type(other) != __class__:
            raise "Kan kun lægge matrix sammen med et andet matrix eller et float eller int"

        # tjekkes om det er et matrix
        if other.rækker() != self.rækker() and other.søjler() != self.søjler():
            raise "Matricer er ikke af samme type"

        for række in range(self.rækker()):
            for søjle in range(self.søjler()):
                matrix[række][søjle] = matrix[række][søjle] + other.matrix[række][søjle]
        return Matrix(matrix)

    def __mul__(self, other):
        # tjekker om det er en skalar
        if type(other) in [float, int]:
            matrix = deepcopy(self.matrix)
            for m in range(self.rækker()):
                for n in range(self.søjler()):
                    matrix[m][n] = matrix[m][n] * other
            return matrix

        if self.søjler() != other.rækker():
            raise "kan ikke ganges sammen"


        matrix = []
        for _ in range(self.rækker()):
            matrix.append([])

        for p, vektor_søjle in enumerate(other.få_søjler()): # laver andet matrix til vektor søjler og iterer igennem dem
            # hver række element ganges med henholdsvis hver vektor_søjle element
            for (m, række) in enumerate(self.matrix):
                matrix[m].append(0)
                for n, element in enumerate(række):
                    matrix[m][p] += vektor_søjle[n] * self.matrix[m][n]

        return Matrix(matrix)

    def __getitem__(self, index):
        return self.matrix[index]