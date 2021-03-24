from Error import *

class Gauss:
    def __init__(self, list_arg, mode):
        self.mode = mode
        self.size = list_arg[0]
        self.i_radiator = list_arg[1]
        self.j_radiator = list_arg[2]
        if self.mode == False:
            self.i_point = list_arg[3]
            self.j_point = list_arg[4]
        self.A_matrix = list()
        self.X_vector = list()
        self.X_result = list()
        self.const_h = 0.25
        self.const_f = -300
        if self.size <= 0:
            error_message("The size of the room must be greater than 0.")
        elif (self.i_radiator < 1 or self.i_radiator > self.size - 2) or (self.j_radiator < 1 or self.j_radiator > self.size - 2) :
            error_message("The coordinates of the radiator must be between 0 and %s." % (self.size - 2))
        elif (self.mode == False and ((self.i_point < 1 or self.i_point > self.size - 2) or (self.j_point < 1 or self.j_point > self.size - 2))):
            error_message("The coordinates of the point in the room must be between 0 and %s." % self.size)

    def build_A_matrix(self):
        matrix_size = self.size * self.size
        for y in range(0, self.size):
            for x in range(0, self.size):
                if (y == 0 or y == self.size - 1 or x == 0 or x == self.size - 1):
                    self.A_matrix.append(self.cond_limite(x, y, matrix_size))
                else:
                    self.A_matrix.append(self.cond_eq(x, y, matrix_size))

    def build_X_vector(self):
        for j in range(self.size):
            for i in range(self.size):
                if (i == self.i_radiator and j == self.j_radiator):
                    self.X_vector.append(self.const_f)
                else:
                    self.X_vector.append(0)

    def cond_limite(self, x, y, matrix_size):
        line = list()
        diag = x + y * self.size
        for cpt in range(matrix_size):
            if (cpt != diag):
                line.append(0)
            else:
                line.append(1)
        return line
    
    def cond_eq(self, x, y, matrix_size):
        line = list()
        diag = x + y * self.size
        for cpt in range(matrix_size):
            if (cpt == x - 1 + y * self.size or cpt == x + 1 + y * self.size or cpt == x + (y - 1) * self.size or cpt == x + (y + 1) * self.size):
                line.append(int(1 / self.const_h))
            elif (cpt == x + y * self.size):
                line.append(int(- 4 / self.const_h))
            else:
                line.append(0)
        return line

    def swap_lines(self, matrice, i, j):
        tmp = matrice[i]
        matrice[i] = matrice[j]
        matrice[j] = tmp

    def matrice_calc(self, matrice, i, j, coeff):
        if type(matrice[0]) != list:
            matrice[i] = matrice[i] + coeff * matrice[j]
        else:
            n = len(matrice[0])
            for k in range(n):
                matrice[i][k] = matrice[i][k] + coeff * matrice[j][k]

    def find_max(self, matrice, j):
        n = len(matrice)
        imax = j
        for i in range(j + 1, n ):
            if abs(matrice[i][j]) > abs(matrice[j][j]):
                imax = i
        return imax

    def triangle(self, matrice, vector):
        n = len(vector)
        x = [0 for i in range(n)]
        x[n - 1] = vector[n - 1] / matrice[n - 1][n - 1]
        for i in range(n - 2, -1, -1):
            s = 0
            for j in range(i + 1, n):
                s = s + matrice[i][j] * x[j]
            x[i] = (vector[i] - s) / matrice[i][i]
        return x

    def calc_X_result(self):
        matrice = self.A_matrix
        vector = self.X_vector
        n = len(matrice)
        i = 0
        for i in range(n-1):
            pivot = self.find_max(matrice, i)
            self.swap_lines(matrice, i, pivot)
            self.swap_lines(vector, i, pivot)
            for k in range(i + 1, n ):
                x = float(matrice[k][i] / matrice[i][i])
                self.matrice_calc(matrice, k, i, -x)
                self.matrice_calc(vector, k, i, -x)
        self.X_result =  self.triangle(matrice, vector)
         
    def display_A_matrix(self):
        matrix_size = self.size * self.size
        for line in self.A_matrix:
            i = 0
            for j in line:
                i += 1
                if (i < matrix_size):
                    print("%d\t" % j, end="")
                else:
                    print("%d" % j)
        
    def display_X_vector(self):
        if self.mode == True:
            for res in self.X_result:
                tmp = round(res, 2) * 100
                if (tmp % 10 == 5):
                    tmp += 1
                tmp /= 100
                if (tmp > -0.04 and tmp < 0.01):
                    tmp = abs(tmp)
                print ('%.1f' % tmp)
        else:
            tmp = round(self.X_result[self.i_point + self.j_point * self.size], 3) * 100
            if (tmp % 10 == 5):
                tmp += 1
            tmp /= 100
            if (tmp > -0.04 and tmp < 0.01):
                tmp = abs(tmp)
            print ('%.1f' % tmp)