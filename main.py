from Indicators import *
from Charts import *
import sys
import time
import datetime
import os.path

def main(args):
	#leitura dos dados de input
	if(os.path.isfile('adjusted.csv')):    #verifica se o ajuste já foi feito anteriormente
		data = pd.read_csv("adjusted.csv")
	else:								   #se não, lê o arquivo original e faz o tratamento
		data = pd.read_csv("input.csv")
		AdjustData(data)

	#processa parâmetros
	if(len(args) == 3):
		start = time.mktime(datetime.datetime.strptime(args[1], "%d-%m-%Y").timetuple())
		end = time.mktime(datetime.datetime.strptime(args[2], "%d-%m-%Y").timetuple())
	else:
		start = data.Timestamp[0]
		end = data.Timestamp[len(data.index)-1]	

	#objeto que armazenará os dados do problema
	indicators = IndicatorData(data, start, end)	

	#calcula valores para os indicadores
	indicators.CalculateMME(20)
	indicators.CalculateIFR(14)
	indicators.CalculateBB(20)

	#objeto responsável pelos plots
	chart = Graf(indicators)

	#plot dos indicadores
	chart.PlotMME()
	chart.PlotIFR()
	chart.PlotBB()

	#escrita do aqrquivo de output
	indicators.Solution.drop(['index'], axis=1).to_csv('indicators.csv', index = False)




if __name__ == "__main__":
	main(sys.argv)