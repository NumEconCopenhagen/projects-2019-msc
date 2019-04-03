#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'dataproject'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Data Analysis Project

#%%
# Importing packages
import pandas as pd # Data structure and analysis package
import numpy as np # Computing package
import seaborn as sns # Additional graphs and layout
import matplotlib.pyplot as plt # Plots
import pydst # Statistics Denmark (DST)
from datetime import datetime # Formating dates
import ipywidgets as widgets # interactive plots
from IPython.display import display # display multiple outputs from a single cell

#%% [markdown]
# ## 1. Importing and cleaning data

#%%
Dst = pydst.Dst(lang='en') # Set language to English


#%%
Dst.get_subjects() # Get overview of Statistics Denmark's subjects

#%% [markdown]
# In our future analysis we drill down into Denmark's current account which is found in Statistics Denmark's table 'BB1S'. 

#%%
Var = Dst.get_variables(table_id = 'BB1S')

#%% [markdown]
# Before going into a deeper analysis, we would like to get an overview of the data.

#%%
Var[:]

#%% [markdown]
# For future analysis we look deeper into the acronyms by changing the index. We notice that the acronyms of the fifth element (index 4) is simply the time values and therefore we do not include these.

#%%
Var0 = pd.DataFrame(Var['values'][0])
for i in range(1,4):
    Var0 = Var0.append(Var['values'][i])
Var0

#%% [markdown]
# First we choose to look at the following dataframe, df1.

#%%
df1= Dst.get_data(table_id = 'BB1S', variables={'TID':['*'], 
                                               'SÆSON':['2'], 'LAND':['*'], 'POST':['*'], 'INDUDBOP':['N']})
df1.head(5)

#%% [markdown]
# We notice that the dataframe, df1, is not sorted in accordance to dates as the dataset starts in 2005. To get an overview of the dataframe we group by accounts and geographical area and colour the negative values red.
#%% [markdown]
# ## 2. Descriptive statistics

#%%
def colourmap(x):
    '''
    Colour negative values red
    Black otherwise
    '''
    if x < 0:
        color = 'red'
    else:
        color = 'black'
    return r'color: %s' % color
df1.sort_values(['TID'], inplace=True)
Descriptive = df1.groupby(['POST','LAND']).describe().style.applymap(colourmap)
Descriptive

#%% [markdown]
# We notice that the current account is overall positive, but negative within the EU-28. Specifically, Denmark has a deficit in regards to services, primary and secondary income when trading with the other EU member states (EU-28). Vi skal lige soge hvor datasættet starter og slutter.
#%% [markdown]
# Moving on, we are only interested in the current account to the whole world (REST OF THE WORLD). Therefore, we specify 'Land'='W1'.

#%%
df= Dst.get_data(table_id = 'BB1S', variables={'TID':['*'], 
                                               'SÆSON':['2'], 'LAND':['W1'], 'POST':['*'], 'INDUDBOP':['N']})
df.sort_values(['TID'], inplace=True)
df.head(5)

#%% [markdown]
# The dataframe looks nice, but in order to plot the accounts, we need to format our time column accordingly. Further, "REST OF THE WORLD" does not seem to be an appropriate name for the whole world. Therefore, we change the name to "Whole world".

#%%
df['LAND'] = df['LAND'].str.replace('REST OF THE WORLD', 'Whole world')
df['TID'] = df['TID'].str.replace('M', '-')
df['TID'] = pd.to_datetime(df['TID'])
display(df.head(5))
display(df.tail(5))

#%% [markdown]
# From the table above we see that our dataset contains monthly data covering the period from the first month of 2005 until and including the first month of 2019. Futher, we define our accounts.

#%%
PI  = df.loc[df['POST'] == 'PRIMARY INCOME', :]
S   = df.loc[df['POST'] == 'SERVICES', :]
SI  = df.loc[df['POST'] == 'SECONDARY INCOME', :]
G   = df.loc[df['POST'] == 'GOODS (FOB)', :]
CA  = df.loc[df['POST'] == 'CURRENT ACCOUNT', :]

Variables = pd.DataFrame(df['POST'].unique())
Variables.columns = ['Accounts']
Variables['Acronyms'] = ('PI','S','SI', 'G', 'CU')

display(Variables.style.hide_index())

#%% [markdown]
# To analyse deeper we plot our accounts. The *current account* identity is as follows:
# 
# $$CA = PI + S + SI + G$$

#%%
plt.style.use('seaborn')
fig, axs = plt.subplots(3,2,figsize=(15,10))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.4)



plt.subplot(3, 2, 1)
plt.plot(PI['TID'],PI['INDHOLD'])
plt.xlabel('Time')
plt.ylabel('Primary Income')
plt.title('Primary Income')

plt.subplot(3, 2, 2)
plt.plot(S['TID'],S['INDHOLD'])
plt.xlabel('Time')
plt.ylabel('Services')
plt.title('Services')

plt.subplot(3, 2, 3)
plt.plot(SI['TID'],SI['INDHOLD'])
plt.xlabel('Time')
plt.ylabel('Secondary Income')
plt.title('Secondary Income')

plt.subplot(3, 2, 4)
plt.plot(G['TID'],G['INDHOLD'])
plt.xlabel('Time')
plt.ylabel('Goods (FOB)')
plt.title('Goods (FOB)')


plt.subplot(3, 1, 3)
plt.plot(CA['TID'],CA['INDHOLD'])
plt.xlabel('Time')
plt.ylabel('Current Account')
plt.title('Current Account')



plt.show('Historical plot')

#%% [markdown]
# In general this is in line with our previous findings. However, as the vertical axis change between figures, it is difficult to compare the accounts. In order to solve this problem, we make an interactive plot displaying all accounts in one graph.

#%%
def myplot_1(services, secondary_income, goods, primary_income):
    if (services==1 and secondary_income==1 and goods==1 and primary_income==1): #alle fem
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and secondary_income==1 and goods==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and secondary_income==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and goods==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (secondary_income==1 and goods==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and secondary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and goods==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (services==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (secondary_income==1 and goods==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (secondary_income==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif (goods==1 and primary_income==1):
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif services==1:
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot2 = plt.plot(PI['TID'], S['INDHOLD'], 'b', label='Services')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif secondary_income==1:
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot3 = plt.plot(PI['TID'], SI['INDHOLD'], 'g', label='Secondary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif goods==1:
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot4 = plt.plot(PI['TID'], G['INDHOLD'], 'y', label='Goods')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    elif primary_income==1:
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plot5 = plt.plot(PI['TID'], PI['INDHOLD'], 'r', label='Primary income')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
    else:
        plot1 = plt.plot(PI['TID'], CA['INDHOLD'], 'black', label='Current account')
        plt.xlabel('Time')
        plt.ylabel('Billion DKK')
        plt.title('Accounts compared to current account')
        plt.legend()
plt.show(myplot_1)

widgets.interactive(myplot_1, services=True, secondary_income=True, goods=True, primary_income=True)

#%% [markdown]
# We see that the surplus of the current account has increased over the years. We are curious to see how much the current account has accumulated to over the period since 2005, hence we use itertools to accumulate the current account.

#%%
import itertools as it
ACC_CA = pd.DataFrame(list(it.accumulate(CA['INDHOLD'])))
ACC_CA.columns = ['Accumulated_CA']
ACC_CA.head(5)

#%% [markdown]
# To get the dates correct, we merge the accumulated current account, with the dates by creating a new DataFrame merged by index. This also allow Us to plot a figure with the correct dates.

#%%
ca_index = pd.DataFrame()
ca_index['Index'] = CA['INDHOLD'].index
ca_index['TID'] = list(CA['TID'])
ca_index['ACC_CA'] = ACC_CA
ca_index = ca_index.set_index('Index')
ca_index.head()

#%% [markdown]
# We are now able to plot the accumulated current account since 2005.

#%%
sns.lineplot(ca_index['TID'],ca_index['ACC_CA'])
plt.xlabel('Time')
plt.ylabel('Billion DKK')
plt.title('Accumulated current account since 2005')
plt.show()

#%% [markdown]
# We see that in the period 2005(1) to 2019(1) the current account accumulates to just above DKK 1600 billion.  
#%% [markdown]
# ## 3. Conclusion
#%% [markdown]
# In general the Danish current account is increasing in the period 2005(1) to 2019(1). However, the current account is on average negative against the the EU-28. This deficit is countered by the surplus from the Danish current account against countries outside the EU-28 resulting in an overall surplus. In the period 2005(1) to 2019(1) the surplus of the current account accumulates to just above DKK 1600 billion.

