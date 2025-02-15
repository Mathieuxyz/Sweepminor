import random
import numpy as np

def bombmap(x: int, y: int, bo: int, start_i: int, start_j: int) -> np.ndarray:
    import random
    import numpy as np

    matrix = np.zeros((y, x))

    for n in range(bo):
        X = random.randint(0, x - 1)
        Y = random.randint(0, y - 1)
        
        # Vérifie que la case (start_i, start_j) n'est pas une bombe
        while matrix[Y][X] == 9 or (X == start_i and Y == start_j):
            X = random.randint(0, x - 1)
            Y = random.randint(0, y - 1)

        matrix[Y][X] = 9
    return matrix


def callout(matrix: np.ndarray) -> np.ndarray:
    for i in range(matrix.shape[0]):  
        for j in range(matrix.shape[1]):
            if matrix[i][j] != 9:  
                for k in range(-1, 2):  # Parcourt les voisins
                    for l in range(-1, 2):  
                        if 0 <= i + k < matrix.shape[0] and 0 <= j + l < matrix.shape[1]:
                            if matrix[i + k][j + l] == 9:  
                                matrix[i][j] += 1  
    return matrix
