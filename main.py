from Indicators import *
import sys
import time
import datetime

def main(args):
	#process parameters
	if(len(args) == 2):
		start = time.mktime(datetime.datetime.strptime(args[0], "%d/%m/%Y").timetuple())
		end = time.mktime(datetime.datetime.strptime(args[1], "%d/%m/%Y").timetuple())


	#input data reading
	data = pd.read_csv("input.csv")
	indicators = IndicatorData(data)
	print(indicators.Data.head())




if __name__ == "__main__":
	main(sys.argv)