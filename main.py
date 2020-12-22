from Indicators import *
from Charts import *
import sys
import time
import datetime

def main(args):
	#input data reading
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




if __name__ == "__main__":
	main(sys.argv)