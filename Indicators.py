import pandas as pd

class IndicatorData:

	def __init__(self, data):
		self.Data = data
		self.Solution = pd.DataFrame(columns = ['timestamp', 'mmefull', 'mme20', 'mme50', 'ifr', 'bb'])
		self.Solution.timestamp = data.Timestamp

	def CalculateMME(periods):

