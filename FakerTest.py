from faker import Faker
import pandas as pd 
from random import randint 
fake = Faker()

 
def input_data(x):
   
    # pandas dataframe
    data = pd.DataFrame()
    for i in range(0, x):
        data.loc[i,'id']= randint(1, 100)
        data.loc[i,'name']= fake.name()
        data.loc[i,'address']= fake.address()
       # data.loc[i,'drivinglicense']=fake.drivinglicense()
        data.loc[i,'latitude']= str(fake.latitude())
        data.loc[i,'longitude']= str(fake.longitude())
    return data
   

# print(input_data(10))

csvdf = pd.read_csv('SampleData/credit_score_cleaned_train.csv')
print(csvdf.dtypes)
