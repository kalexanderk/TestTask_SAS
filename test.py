
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[2]:

df_initial=pd.read_excel('Data/payments.xlsx', 'PAYMENTS', header=0, index_col=None,na_values=['NA'])
df_initial.head(20)


# In[3]:

df_initial['dt']=df_initial.dt.apply(lambda x: pd.to_timedelta(x, unit='D') + pd.Timestamp('1960-1-1'))


# In[4]:

df_initial.head(20)


# In[5]:

df_initial['wk_index']=df_initial.dt.apply(lambda x: x.weekday())
df_initial.head(10)


# In[6]:

df_initial['weekday'] = np.where(df_initial['wk_index']==4, 'Friday', np.where(df_initial['wk_index']==5, 'Saturday', np.where(df_initial['wk_index']==6, 'Sunday', np.where(df_initial['wk_index']==0, 'Monday', np.where(df_initial['wk_index']==1, 'Tuesday', np.where(df_initial['wk_index']==2, 'Wednesday', np.where(df_initial['wk_index']==3, 'Thursday', '')))))))
df_initial.head(10)


# In[7]:

df_initial['id_lagged'] = df_initial.lead_id.shift(periods=1, freq=None, axis=0)
df_initial['id_lagged'].fillna(0, inplace=True)
df_initial.id_lagged = df_initial.id_lagged.astype(int)
df_initial.dtypes


# In[8]:

def find_days_not_returned(df):
    df['days_not_returned']=0
    for i, row in df.iterrows():
        if (row['lead_id']==row['id_lagged']) & (row['amount']==0):
            if (row['wk_index']==5) | (row['wk_index']==6):
                df['days_not_returned'][i]=coun
            else:
                coun+=1
                df['days_not_returned'][i]=coun
        elif (row['lead_id']!=row['id_lagged']) | (row['amount']>0):
            if row['amount'] != 0:
                coun=0
                df['days_not_returned'][i]=coun
            if row['amount'] == 0:
                coun=1
                df['days_not_returned'][i]=coun
    return 0;
        


# In[9]:

df_test = df_initial[0:500]


# In[10]:

coun=0
find_days_not_returned(df_initial)
del df_initial['wk_index']
del df_initial['id_lagged']


# In[11]:
#saving the result
df_initial.to_excel("Files/result.xlsx", sheet_name="PAYMENTS")

