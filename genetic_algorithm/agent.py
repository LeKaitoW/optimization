class Agent:


	def __init__(self, dimension, values):
		self.dimension = dimension
		self.values = values
		self.rate = self.sphere_function()
		self.encoding_values = []


	def sphere_function(self):
		F=0
		for i in range(self.dimension):
			F += pow(self.values[i],2)
		return F
