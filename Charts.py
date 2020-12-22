import matplotlib.pyplot as plt
from Indicators import *
from datetime import datetime

class Graf:

	def __init__(self, Indicator):
		self.Data = Indicator.Solution.copy()
		self.Interval = str(datetime.fromtimestamp(self.Data.timestamp[0])) + ' - ' + str(datetime.fromtimestamp(self.Data.timestamp[len(self.Data.index)-1]))
		


	def PlotMME(self):
		plt.title('MME-20 BTC - ' + self.Interval)
		plt.plot(self.Data.mme20)
		plt.gca().axes.get_xaxis().set_visible(False)
		plt.savefig("mme.png")
		plt.clf()

	def PlotIFR(self):
		plt.title('IFR-14 BTC - ' + self.Interval)
		plt.plot(self.Data.ifr14)
		plt.gca().axes.get_xaxis().set_visible(False)
		plt.savefig("ifr14.png")
		plt.clf()

	def PlotBB(self):
		plt.title('BB-20 BTC - ' + self.Interval)
		plt.plot(self.Data.timestamp, self.Data.bb20inf)
		plt.plot(self.Data.timestamp, self.Data.bb20sup)
		plt.gca().axes.get_xaxis().set_visible(False)
		plt.savefig("bb20.png")
		plt.clf()
