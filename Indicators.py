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

		mms = self.Data.loc[start:start+periods-1, 'Close'].sum() / periods

		mme_prev = mms

		start = start+periods-1

		print(end - start)
		
		for i in range(start, end + 1):
			close = self.Data.at[i, 'Close']
			mme = ((close - mme_prev) * k) + mme_prev
			ts = self.Data.at[i, 'Timestamp']
			if(ts >= self.Start):
				self.Solution.loc[self.Solution['index']==i, column] = mme


	def CalculateIFR(self, periods):	
		column = 'ifr' + str(periods)	
		UD = pd.DataFrame(columns = ['timestamp', 'u', 'd'])
		UD.timestamp = self.Solution.timestamp.copy()
		UD.set_index('timestamp', inplace = True)
		start = max(self.Solution['index'][0]-100, 0)
		end = self.Solution['index'][len(self.Solution.index)-1]		
		nup = 0
		ndown = 0		
		mean_u = 0.0
		mean_d = 0.0

		for i in range(start+1, end + 1):

			close = self.Data.Close[i]
			ts = self.Data.Timestamp[i]

			if(close > self.Data.Close[i-1]):

				mean_u += close / periods

				if(nup == 0):
					firstup = close

				if(nup < periods):
					nup += 1

				else:
					mean_u -= firstup / periods
					firstup = close
			
			elif(close < self.Data.Close[i-1]):

				mean_d += close / periods	

				if(ndown == 0):
					firstdown = close

				if(ndown < periods):
					ndown += 1

				else:
					mean_d -= firstdown / periods
					firstdown = close

			if((ts >= self.Start) & (nup >= periods) & (ndown >= periods)):
				ifr = 100 - (100 / (1 + (mean_u / mean_d)))
				self.Solution.loc[self.Solution['index']==i, column] = ifr


	def CalculateBB(self, periods):
		column_sup = 'bb' + str(periods) + 'sup'
		column_inf = 'bb' + str(periods) + 'inf'
		start = max(self.Solution['index'][0]-periods, 0)
		end = self.Solution['index'][len(self.Solution.index)-1]

		closes = np.empty(0)
		for i in range(start, start + periods-1):
			closes = np.append(closes, self.Data.Close[i])


		for i in range(start+periods-1, end+1):
			ts = self.Data.Timestamp[i]
			close = self.Data.Close[i]
			closes = np.append(closes, close)
			sd = np.std(closes)
			mean = np.mean(closes)
			closes = np.delete(closes, 0)

			if(ts >= self.Start):
				self.Solution.loc[self.Solution['index']==i, column_sup] = mean + 2*sd
				self.Solution.loc[self.Solution['index']==i, column_inf] = mean - 2*sd








	def AdjustData(self):
		for index, row in self.Data.iterrows():
			if(not row.Close>0):
				self.Data.drop(index)
			else:
				break

		print("opassoiu")

		self.Data.reset_index(drop=True, inplace=True)
		print("opassoiu")

		dataux = self.Data[(self.Data.Close>0) == False]
		print("opassoiu")

		for i in dataux.index:
			self.Data.at[i, "Close"] = self.Data.at[i-1, "Close"]
