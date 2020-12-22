from Indicators import *
from Charts import *
import sys
import time
import datetime
import os.path

def main(args):
	#input data reading
	if(os.path.isfile('adjusted.csv')):
		data = pd.read_csv("adjusted.csv")
	else:
		data = pd.read_csv("input.csv")
		AdjustData(data)

	#process parameters
	if(len(args) == 3):
		start = time.mktime(datetime.datetime.strptime(args[1], "%d-%m-%Y").timetuple())
		end = time.mktime(datetime.datetime.strptime(args[2], "%d-%m-%Y").timetuple())
	else:
		start = data.Timestamp[0]
		end = data.Timestamp[len(data.index)-1]	
	indicators = IndicatorData(data, start, end)	
	indicators.CalculateMME(20)
	indicators.CalculateIFR(14)
	indicators.CalculateBB(20)
	print(indicators.Solution.head())
	chart = Graf(indicators)
	chart.PlotMME()
	chart.PlotIFR()
	chart.PlotBB()
	indicators.Solution.drop(['index'], axis=1).to_csv('indicators.csv', index = False)




if __name__ == "__main__":
	main(sys.argv)