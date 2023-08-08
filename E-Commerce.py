#!/usr/bin/env python
# coding: utf-8

# # E-Commerce Analysis

# In[1]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


get_ipython().system('pip install pyarrow')


# In[3]:


all_data = pd.read_feather(r'/Users/bjfabusoye/Desktop/Sales_data.ftr')


# In[4]:


all_data.head(6)


# In[5]:


all_data.isnull().sum()


# In[6]:


all_data = all_data.dropna(how = "all")


# In[7]:


all_data.isnull().sum()


# In[ ]:





# In[8]:


filter1 = all_data.duplicated()


# In[9]:


all_data[filter1]


# In[10]:


all_data = all_data.drop_duplicates()


# In[ ]:





# ## Best Month for Sale

# In[11]:


all_data.head(2)


# In[12]:


all_data['Order Date'][0].split('/')[0]


# In[13]:


def return_month(x):
    return x.split('/')[0]


# In[14]:


all_data['Month'] = all_data['Order Date'].apply(return_month)


# In[15]:


all_data['Month'].unique()


# In[16]:


filter2 = all_data['Month'] == 'Order Date'


# In[17]:


all_data = all_data[~filter2]


# In[ ]:





# In[18]:


from warnings import filterwarnings
filterwarnings('ignore')


# In[19]:


all_data['Month'] = all_data['Month'].astype(int)


# In[20]:


all_data.dtypes


# In[21]:


all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype(int)
all_data['Price Each'] = all_data['Price Each'].astype(float)


# In[22]:


all_data.dtypes


# In[23]:


all_data['sales'] = all_data['Quantity Ordered'] * all_data['Price Each']


# In[24]:


all_data.groupby(['Month'])['sales'].sum()


# In[ ]:





# In[25]:


all_data.groupby(['Month'])['sales'].sum().plot(kind = 'bar')
plt.ylabel('Sales (in millions)')


# ##### December had the highest number of sales. 

# In[ ]:





# ## City With the Maximum Amount of Orders

# In[26]:


all_data.head(2)


# ##### to get the 1th index of each row in the column (Purchase Address)

# In[27]:


all_data['city'] = all_data['Purchase Address'].str.split(',').str.get(1)


# In[28]:


all_data['city']


# In[ ]:





# In[29]:


pd.value_counts(all_data['city'])


# In[30]:


freq = pd.value_counts(all_data['city'])


# In[34]:


freq.plot(kind = 'pie' , autopct = '%1.0f%%')
plt.ylabel(' ')


# ##### About a quarter of the total sales were from San Francisco.

# In[ ]:





# ## Top-Selling Product Analysis: Unveiling the Factors Behind Its Remarkable Success

# In[35]:


all_data.columns


# In[36]:


count_df = all_data.groupby(['Product']).agg({'Quantity Ordered' : 'sum' , 'Price Each' : 'mean'})


# In[37]:


count_df = count_df.reset_index()


# In[38]:


count_df


# In[39]:


products = count_df['Product'].values


# In[40]:


fig , ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.bar(count_df['Product'] , count_df['Quantity Ordered'], color = 'purple')
ax2.plot(count_df['Product'] , count_df['Price Each'] , color = 'black')

ax1.set_xticklabels(products , rotation = 'vertical', fontsize = 8)
ax1.set_ylabel('Order Count')
ax2.set_ylabel('Avg price of product')


# ##### The graph suggests that the more expensive an item is, the less purchases it will get in comparison to cheaper items.
# ##### AAA batteries are the most purchased and cheapest items. The Macbook Pro Laptop is one of the least purchased, yet the most expensive item.

# In[ ]:





# # Trend of the Most Sold Product 

# In[41]:


all_data['Product'].value_counts()[0:5].index


# In[42]:


most_sold_product = all_data['Product'].value_counts()[0:5].index


# In[43]:


filter3 = all_data['Product'].isin(most_sold_product)


# In[44]:


filter3


# In[45]:


all_data[filter3]


# In[46]:


most_sold_product_df = all_data[filter3]


# In[47]:


most_sold_product_df.head(6)


# In[48]:


most_sold_product_df.groupby(['Month' , 'Product']).size()


# In[49]:


most_sold_product_df.groupby(['Month' , 'Product']).size().unstack()


# In[50]:


pivot = most_sold_product_df.groupby(['Month' , 'Product']).size().unstack()


# In[51]:


pivot.plot(figsize = (8 , 6))
plt.ylabel('Order Count')


# ##### All top selling products seem to follow a similar trend through the year

# In[ ]:





# ## Products Most Often Sold Together 

# In[52]:


all_data.columns


# In[53]:


all_data['Order ID']


# In[54]:


all_data['Order ID'].duplicated(keep=False)


# In[55]:


filter4 = all_data['Order ID'].duplicated(keep=False)


# In[56]:


all_data[filter4]


# In[57]:


df_duplicated = all_data[filter4]


# In[58]:


dup_products = df_duplicated.groupby(['Order ID'])['Product'].apply(lambda x : ','.join(x)).reset_index().rename(columns={'Product' : 'grouped_products'})


# In[59]:


dup_products


# In[60]:


dup_products_df = df_duplicated.merge(dup_products ,how = 'left', on = 'Order ID')


# In[61]:


dup_products_df


# In[62]:


no_dup_df = dup_products_df.drop_duplicates(subset=['Order ID'])


# In[63]:


no_dup_df.shape


# In[64]:


no_dup_df['grouped_products'].value_counts()


# In[65]:


no_dup_df['grouped_products'].value_counts()[0:5].plot(kind = 'pie' , autopct = '%1.0f%%')
plt.ylabel('')


# ##### The iPhone and the Lightning Charging Cable were most often bought together. 

# In[ ]:




