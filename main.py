import web_crawler as wc
import process_data as pcd
import pandas as pd
import pickle

initial_list = pd.read_csv('zip_codes.csv', header=None)
codes = [val for val in initial_list[0]][:10]
codes = [95070, 95129]

soups = {}


driver = wc.init_driver('./chromedriver')
wc.navigate_to_page(driver, 'https://www.realtor.com/')
for code in codes:
    soup = wc.navigate_to_code(driver, code)
    soups.update(soup)
homes_list = pcd.process_soups(soups, codes)
df = pcd.create_df(homes_list)
pcd.create_csv(df)

wc.terminate_driver(driver)
