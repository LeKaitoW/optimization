import math

class Agent:

    def __init__(self, function, values):
        self.counter = 0
        self.functions = {
            'sphere': self.sphere_function,
            'Rozen': self.Rozenbrock_function,
            'Rastr' : self.Rastr_function,
            'Shekel' : self.Shekel_function
        }
        self.values = values
        self.rate = self.functions[function]()
        #self.rate = self.sphere_function()

    def sphere_function(self):
        F = 0
        for i in range(len(self.values)):
            F += pow(self.values[i], 2)
        return F

    def Rozenbrock_function(self):
        x_0 = 2
        F_0 = 390
        F = 0
        for i in range(len(self.values) - 1):
            zi = self.values[i] - x_0
            zi1 = self.values[i+1] - x_0
            F += 100 * (pow(pow(zi, 2) - zi1, 2) + pow(zi - 1, 2))
        F += F_0
        return F

    def Rastr_function(self):
        F = 0
        x_0 = 2
        F_0 = -330
        for i in range(len(self.values)):
            z = self.values[i] - x_0
            F+=(pow(z,2) - 10*math.cos(2*z*math.pi)+10)
        F+=F_0
        return -F

    def Shekel_function(self):
        M = 3
        if (self.counter == 0):



