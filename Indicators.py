import pandas as pd
import numpy as np

class IndicatorData:

	def __init__(self, data, start, end):
		self.Data = data		
		self.Solution = pd.DataFrame(columns = ['timestamp'])
		self.Solution.timestamp = data[(data.Timestamp >= start) & (data.Timestamp <= end)].Timestamp.copy()
		self.Solution.reset_index(inplace=True)
		self.Start = start
		self.End = end

	def CalculateMME(self, periods):
		column = 'mme' + str(periods)
		# multiplicador para ponderação
		k = 2 / (periods + 1)

		start = max(self.Solution['index'][0]-periods, 0)
		end = self.Solution['index'][len(self.Solution.index)-1]

		#cálculo da média móvel simples para alimentar a primeira média móvel expoencial
		mms = self.Data.loc[start:start+periods-1, 'Close'].sum() / periods

		mme_prev = mms

		start = start+periods-1
		
		for i in range(start, end + 1):
			close = self.Data.at[i, 'Close']
			#cálculo da mme atual
			mme = ((close - mme_prev) * k) + mme_prev
			ts = self.Data.at[i, 'Timestamp']
			if(ts >= self.Start):
				self.Solution.loc[self.Solution['index']==i, column] = mme


	def CalculateIFR(self, periods):	
		column = 'ifr' + str(periods)			
		start = max(self.Solution['index'][0]-100, 0)
		end = self.Solution['index'][len(self.Solution.index)-1]	
		#arrays que armazenam os valores de fechamento dos ultimos n candles de alta e baixa	
		up = np.empty(0)
		down = np.empty(0)

		for i in range(start+1, end + 1):

			close = self.Data.Close[i]
			prev = self.Data.Close[i-1]
			ts = self.Data.Timestamp[i]

			if(close > prev):
				#populando o vetor de alta
				up = np.append(up, close)						

				if(len(up) > periods):
					#remove-se o dado mais antigo
					up = np.delete(up, 0)
			
			elif(close < prev):
				#populando o vetor de baixa
				down = np.append(down, close)						

				if(len(down) > periods):
					#remove-se o dado mais antigo
					down = np.delete(down, 0)

			if((ts >= self.Start) & (len(up) >= periods) & (len(down) >= periods)):

				ifr = 100 - (100 / (1 + (np.mean(up) / np.mean(down))))

				self.Solution.loc[self.Solution['index']==i, column] = ifr


	def CalculateBB(self, periods):
		column_sup = 'bb' + str(periods) + 'sup'
		column_inf = 'bb' + str(periods) + 'inf'
		start = max(self.Solution['index'][0]-periods, 0)
		end = self.Solution['index'][len(self.Solution.index)-1]
		#array que armazena os fechamentos dos últimos n candles
		closes = np.empty(0)

		#popula-se o array com dados anteriores ao periodo
		for i in range(start, start + periods-1):
			closes = np.append(closes, self.Data.Close[i])


		for i in range(start+periods-1, end+1):
			ts = self.Data.Timestamp[i]
			close = self.Data.Close[i]
			closes = np.append(closes, close)
			sd = np.std(closes)
			mean = np.mean(closes)
			closes = np.delete(closes, 0)
			#cálculo das bandas
			if(ts >= self.Start):
				self.Solution.loc[self.Solution['index']==i, column_sup] = mean + 2*sd
				self.Solution.loc[self.Solution['index']==i, column_inf] = mean - 2*sd








def AdjustData(data):
	for index, row in data.iterrows():
		if(not row.Close>0):
			data.drop(index)
		else:
			break

	data.reset_index(drop=True, inplace=True)

	dataux = data[(data.Close>0) == False]

	for i in dataux.index:
		data.at[i, "Close"] = data.at[i-1, "Close"]

	data.to_csv('adjusted.csv', index = False)
