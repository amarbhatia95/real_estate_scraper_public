import numpy as np
import pandas as pd
from datetime import datetime
import json


def standardize_dicts(obj):
    '''Helper function to take in list of dictionaries, unnest those dictionaries for pandas and return list'''
    sample_dict = {}
    homes = []

    for i in range(len(obj)):
        for k, v in obj[i].items():
            if not type(v) == dict:
                sample_dict[k] = v
            else:
                for a, b in v.items():
                    if not type(b) == dict:
                        sample_dict[a] = b
                    else:
                        for c, d in b.items():
                            if not type(d) == dict:
                                sample_dict[c] = d
                            else:
                                for e, f in d.items():
                                    sample_dict[e] = f
        # print(sample_dict['zpid'])
        homes.append(sample_dict.copy())

    return homes

def process_soups(soups, codes=[95070, 95129]):
    '''Read Soups Dict'''
    homes_list = []
    for code in codes:
        iters = len(soups[code])
        for i in range(iters):
            print(i)
            obj = json.loads(soups[code][i].find_all('script', {'type': 
                'application/json'})[1].string.strip('<>--!'))['cat1']['searchResults']['listResults']
            homes = standardize_dicts(obj)
            homes_list.append(homes)
    
    homes_list = [item for l in homes_list for item in l]
    
    return homes_list
        

def create_df(list_of_homes):
    return pd.DataFrame(list_of_homes)

def create_csv(dataframe):
    title = 'homes '
    time = datetime.now().strftime('%Y-%m-%d-%H_%M')
    file_type = '.csv'
    name = title + time + file_type

    return dataframe.to_csv(name)