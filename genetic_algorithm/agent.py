class Agent:


	def __init__(self, function, values):
		self.function = function
		self.values = values
		self.rate = self.sphere_function()
		self.encoding_values = []


	def sphere_function(self):
		F=0
		for i in range(len(self.values)):
			F += pow(self.values[i],2)
		return F
