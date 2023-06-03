from tabula import read_pdf
import tabula
import pandas as pd
import sys
import re
import linkGrabber
import datetime

def get_link(date):
	links=linkGrabber.Links('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/')
	date=datetime.datetime.today().strftime(date)
	link= links.find(href=re.compile(date),limit=1)
	link=link[0]
	link=link['href']
	link='https://www.who.int'+ link[0:-18]
	return link


def country_list():
	country_input=input("Enter the countries you wish to see, separated only by a comma: ")
	country_list = country_input.split(',')
	print("You will view the following countries: ", country_list)
	return country_list


def set_page(link,country_list,page_number):
#	print('Time 0:', datetime.datetime.now())
	raw_data=read_pdf(link,pages=page_number)[0]
#	print('Time 1:', datetime.datetime.now())
	raw_data=raw_data[raw_data.columns[[0,1,2,3]]]
	raw_data.columns=['Country/Region','Total Cases','Total New Cases','Total Deaths']
	for i in range(0,raw_data.shape[0]):
		country_data=raw_data.loc[i]
		measure=0
		removed=False
		if type(country_data['Total Cases'])==float or type(country_data['Country/Region'])==float or type(country_data['Total Deaths'])==float or type(country_data['Total New Cases'])==float:
			raw_data.drop(i,axis='rows',inplace=True)
			full_data=raw_data
			removed=True
		if removed==False:
			for x in range(0,len(country_list)):			
				if country_list[x] not in country_data['Country/Region']:
					measure+=1
					if measure==len(country_list):
						raw_data.drop(i,axis='rows',inplace=True)
						full_data=raw_data
						break
	full_data=raw_data
	return full_data


def data_together(link,countries_selected):
	df_list=list()
	for x in range(1,19):
		try:
			data_checked=set_page(link,countries_selected,x)
			if isinstance(data_checked, pd.DataFrame):
				if not data_checked.empty:
					data_checked.rename(index=date_range[x],inplace=True)
					df_list.append(data_checked)
		except IndexError:
			pass
		except:
			print("Unexpected error:", sys.exc_info()[0])
	return df_list

def join_data(list):
	try:
		data=pd.concat(list) #axis=1, sort=False
		return data

	except ValueError:
		print('No data in pdf yet')

	except:
		print("Unexpected error:", sys.exc_info()[0])

#date_range=((pd.date_range(start="20200303",end=datetime.datetime.today().strftime('%Y%m%d'))).strftime('%Y%m%d')).to_list()
date_range=((pd.date_range(start="20200604",end=datetime.datetime.today().strftime('%Y%m%d'))).strftime('%Y%m%d')).to_list()
country_list=country_list()
day_list=list()
for x in range(0,(len(date_range))):
	link=get_link(date_range[x])
	data_list=data_together(link,country_list)
	print(data_list)
	data=join_data(data_list)
#	data.index=[date_range[x]]
#	print(date_range[x], '----------\n', data, '\n----------')
	day_list.append(data)
#print(day_list)
#print(type(day_list))
