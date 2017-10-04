
# coding: utf-8

# In[43]:

import pandas as pd
import numpy as np


# In[44]:

df_initial=pd.read_excel('Data/payments.xlsx', 'PAYMENTS', header=0, index_col=None,na_values=['NA'])
df_initial.head(20)


# In[45]:

df_initial['dt']=df_initial.dt.apply(lambda x: pd.to_timedelta(x, unit='D') + pd.Timestamp('1960-1-1'))


# In[46]:

df_initial.head(20)


# In[47]:

df_initial['wk_index']=df_initial.dt.apply(lambda x: x.weekday())
df_initial.head(10)


# In[48]:

df_initial['weekday'] = np.where(df_initial['wk_index']==4, 'Friday', np.where(df_initial['wk_index']==5, 'Saturday', np.where(df_initial['wk_index']==6, 'Sunday', np.where(df_initial['wk_index']==0, 'Monday', np.where(df_initial['wk_index']==1, 'Tuesday', np.where(df_initial['wk_index']==2, 'Wednesday', np.where(df_initial['wk_index']==3, 'Thursday', '')))))))
df_initial.head(10)


# In[49]:

df_initial['id_lagged'] = df_initial.lead_id.shift(periods=1, freq=None, axis=0)
df_initial['id_lagged'].fillna(0, inplace=True)
df_initial.id_lagged = df_initial.id_lagged.astype(int)
df_initial.dtypes


# In[50]:

df_initial['help'] = np.where((df_initial['amount']!=0) , -100, np.where((df_initial['wk_index']==5) | (df_initial['wk_index']==6), 0, 1 ))
df_initial['cumhelp']=[0]*len(df_initial)
df_initial.head(10)


# In[95]:

amt_not_zero = np.where(df_initial.help == -100, df_initial.help.index, -1)
amt_not_zero_pos = np.where(amt_not_zero != -1)[0]
amt_not_zero_pos = np.append(amt_not_zero_pos, len(df_initial)-1)
amt_not_zero_pos


# In[98]:

def days_not_returned(df):
    for i in range(0,len(amt_not_zero_pos)-1):
        if (amt_not_zero_pos[i+1]-amt_not_zero_pos[i] >1):
            df.iloc[amt_not_zero_pos[i]+1:amt_not_zero_pos[i+1], 7]=df.iloc[amt_not_zero_pos[i]+1:amt_not_zero_pos[i+1], 6].cumsum()
    
    if (df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 2] != 0.):
        df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 7] = 0
    elif ((df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 3] == 5) | (df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 3] == 6)):
        df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 7] = df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1]-1, 7]
    else:
        df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1], 7] = df.iloc[amt_not_zero_pos[len(amt_not_zero_pos)-1]-1, 7]+1
        
    return df


# In[99]:

days_not_returned(df_initial)


# In[112]:

del df_initial['wk_index']
del df_initial['id_lagged']
del df_initial['help']
df_initial.rename(columns={"cumhelp":"days_not_returned"})


# In[114]:

df_initial.to_excel("Files/result.xlsx", sheet_name="PAYMENTS")


# In[ ]:



