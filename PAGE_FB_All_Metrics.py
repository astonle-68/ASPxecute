# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:14:10 2024

@author: Windows
"""

import pandas as pd
import requests
import json
import datetime as dt
import pyarrow as pa
import pyarrow.parquet as pq

# https://developers.facebook.com/docs/graph-api/reference/v19.0/insights#parameters
#%%
lst_metric = 'page_tab_views_login_top_unique,page_tab_views_login_top,page_tab_views_logout_top,\
    page_total_actions,page_cta_clicks_logged_in_total,page_cta_clicks_logged_in_unique,\
    page_call_phone_clicks_logged_in_unique,page_get_directions_clicks_logged_in_unique,\
    page_website_clicks_logged_in_unique,page_post_engagements,page_consumptions_unique,\
    page_consumptions_by_consumption_type,page_consumptions_by_consumption_type_unique' # ok
                
df_api = pd.read_excel(r'''D:/MOHO's OTHER PROJECT/00- Google Analytics and Meta Business Suite/Metrics_FB_New.xlsx''')

                  
lst_api = df_api['API_Name'].tolist()#  [:10]   # total 199 metrics

lst_check = []
for i in lst_api:
    if "*" in i:
        lst_check.append(i)
        
lst_metric = []
for i in lst_api:
    i = i.replace('*', '').strip()
    lst_metric.append(i)
    
    
# lst_metric = ','.join(lst_metric)

lst_result = []
lst_fail = []
lst_success = []
for i in lst_metric:

    url = 'https://graph.facebook.com/401290640238099?fields=insights.metric('\
        + str(i) +  ').limit(1000)'  #+ "&since=2024-06-23" + "&until=2024-06-23" # ok
       
        
    total_reaction = []
    
    data = requests.get(url, headers = {'Authorization': 'Bearer ' + 'EAASaElrY2moBO1ZAjZB0hrxHulz13E2P9CVU637wbxfdhm2VUVD4yp9dlaLo31l8qpLz0FO2RxZBcD4kOOo9o5fCdBQ2NesL7T3uBBkE5QkfLMIGvZCsuMyWrHAlfZAjWOYASUUN8V4R1POUqQ0p7jqvQ0WWf9wkhZAxZANi8OjBeqSi5sZB22BT1sf8RdZBGxGqf',
                                        'Content-Type': 'application/json'})
    
    tot_reaction=json.loads(data.text) 
    total_reaction.append(tot_reaction)
    df = pd.json_normalize(total_reaction)

    try:
        spike_cols = [col for col in df.columns if 'data' in col][0]  
        
        
        df = df[[spike_cols]]
        df3 = pd.json_normalize(df[spike_cols])
        df3 = df3.stack().reset_index() 
        df3 = pd.json_normalize(df3[0])    
            
        df3 = df3.loc[df3['period'] == 'day']
        
        
        lst_df = []
        for i in list(dict.fromkeys(df3['name'].tolist())):
            df1 = df3.loc[df3['name'] == i]
            spike_col = [col for col in df1.columns if 'value' in col][0]
            df1 = pd.json_normalize(df1[spike_col])
            df1 = df1.stack().reset_index() 
            df1 = pd.json_normalize(df1[0])  
            df1.columns = [x.replace('value', i + '_').strip() for x in df1.columns]
            df1.columns = [x.replace('_.', '_').strip() for x in df1.columns]
            lst_df.append(df1)
            continue
            
        
        from functools import reduce
        result = reduce(lambda df1,df2: pd.merge(df1,df2,on='end_time'), lst_df)
        lst_result.append(result)
    except:
        lst_fail.append(i)  
        lst_success.append(i)
        print('- Metrics fail: {}'.format(i))
        pass

final = reduce(lambda df1,df2: pd.merge(df1,df2,on='end_time'), lst_result)

print('Total metrics FAIL: {}'.format(len(lst_fail))) # 111

path = '''D:/MOHO's OTHER PROJECT/00- Google Analytics and Meta Business Suite/Page_FB_Metrics/Page_FB_Data.parquet'''
df_all = pd.read_parquet(path)

df_all = pd.concat([final, df_all])

df_all.drop_duplicates(subset =['end_time'], keep = 'first', inplace = True)

table = pa.Table.from_pandas(df_all)
pq.write_table(table, path)

print('                 ')
print('   --  PAGE FB COMPLETED  --    ')
#%%
#%% TESTING DATA
# path = '''D:/MOHO's OTHER PROJECT/00- Google Analytics and Meta Business Suite/Page_FB_Metrics/Page_FB_Data.parquet'''
# df = pd.read_parquet(path)

# lst_check = []
# for i in list(df.columns):
#     if 'fan' in i:
#         lst_check.append(i)
# print(lst_check)   
# check = df[lst_check]












# #%%
# #%% Test lst_fail

# lst_metric = 'page_impressions_by_age_gender_unique'

# url = 'https://graph.facebook.com/401290640238099?fields=insights.metric('\
#     + str(lst_metric) +  ').limit(1000)'  #+ "&since=2024-03-19" + "&until=2024--19" # ok
   
    
# total_reaction = []

# data = requests.get(url, headers = {'Authorization': 'Bearer ' + 'EAASaElrY2moBO1ZAjZB0hrxHulz13E2P9CVU637wbxfdhm2VUVD4yp9dlaLo31l8qpLz0FO2RxZBcD4kOOo9o5fCdBQ2NesL7T3uBBkE5QkfLMIGvZCsuMyWrHAlfZAjWOYASUUN8V4R1POUqQ0p7jqvQ0WWf9wkhZAxZANi8OjBeqSi5sZB22BT1sf8RdZBGxGqf',
#                                     'Content-Type': 'application/json'})

# tot_reaction=json.loads(data.text) 
# total_reaction.append(tot_reaction)
# df = pd.json_normalize(total_reaction)
# print(df)

# spike_cols = [col for col in df.columns if 'data' in col][0]  


# df = df[[spike_cols]]
# df3 = pd.json_normalize(df[spike_cols])
# df3 = df3.stack().reset_index() 
# df3 = pd.json_normalize(df3[0])    
    
# df3 = df3.loc[df3['period'] == 'day']

# print(df3['name'])

# lst_df = []
# for i in list(dict.fromkeys(df3['name'].tolist())):
#     df1 = df3.loc[df3['name'] == i]
#     spike_col = [col for col in df1.columns if 'value' in col][0]
#     df1 = pd.json_normalize(df1[spike_col])
#     df1 = df1.stack().reset_index() 
#     df1 = pd.json_normalize(df1[0])  
#     df1.columns = [x.replace('value', i + '_').strip() for x in df1.columns]
#     df1.columns = [x.replace('_.', '_').strip() for x in df1.columns]
#     lst_df.append(df1)
#     continue
    

# from functools import reduce
# result = reduce(lambda df1,df2: pd.merge(df1,df2,on='end_time'), lst_df)

# result.columns


# importance_metrics = 'page_impressions_by_age_gender_unique'

# result.columns = [x.replace('page_impressions_by_age_gender_unique', '').strip() for x in result.columns]




