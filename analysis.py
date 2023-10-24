import pandas as pd
import os
import matplotlib.pyplot as plt 


#merge sales data into a single file

files=[file for file in os.listdir('C:\\Users\\Firas\\Desktop\\py project\sales_analysis\\Sales_Data')]

sales_df=pd.DataFrame()

for csv_file in files :
    df=pd.read_csv('C:\\Users\\Firas\\Desktop\\py project\sales_analysis\\Sales_Data\\'+ csv_file)
    sales_df=pd.concat([sales_df,df])

sales_df.to_csv("all_sales_data.csv")
all_sales_data=pd.read_csv("all_sales_data.csv")


#clean the Data by Dropping all Nan if existing and 'Or'

#nan_df=all_sales_data[all_sales_data.isna().any(axis=1)]
#print(nan_df.head)

all_sales_data= all_sales_data.dropna()
all_sales_data=all_sales_data[all_sales_data["Order Date"].str[0:2]!='Or']

all_sales_data["Quantity Ordered"]= pd.to_numeric(all_sales_data["Quantity Ordered"])
all_sales_data["Price Each"]= pd.to_numeric(all_sales_data["Price Each"])


#catigorize data by months from Order date
all_sales_data["Month"]= all_sales_data["Order Date"].str[0:2]
all_sales_data["Month"]=pd.to_numeric(all_sales_data["Month"])

#calculate the money made on each sale  

all_sales_data['Money on Sale']= all_sales_data["Quantity Ordered"]*all_sales_data["Price Each"]
all_sales_data['Money on Sale']= pd.to_numeric(all_sales_data['Money on Sale'])
#print(all_sales_data.head())

monthly_sales=all_sales_data.groupby('Month').sum()['Money on Sale']
print(monthly_sales)
#result=monthly_sales.to_list

def get_adress(adress , c ):
    return adress.split(',')[c]

#add a city column
all_sales_data['City']=all_sales_data['Purchase Address'].apply(lambda x : get_adress(x,1) + ' ' + get_adress(x,2).split(' ')[1])
city_sales=pd.to_numeric(all_sales_data.groupby('City').sum()['Money on Sale'])

#print(city_sales)
months=range(1,13)

#plt.bar(months,monthly_sales)
#plt.xticks(months)
#plt.xlabel("Months")
#plt.ylabel("Sales in USD")
#plt.show()

#Let's find out the best time to advertise
all_sales_data['Order Date']=pd.to_datetime(all_sales_data['Order Date'])
all_sales_data['Hour']=all_sales_data['Order Date'].dt.hour
all_sales_data['Minute']=all_sales_data['Order Date'].dt.minute


hours=[hour for hour , df in all_sales_data.groupby('Hour')]

plt.plot(hours , all_sales_data.groupby('Hour').count())
plt.xticks(hours)
plt.grid()
plt.show()