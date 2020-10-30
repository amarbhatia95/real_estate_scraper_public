import web_crawler as wc
import process_data as pcd

soups = {}


driver = wc.init_driver('./chromedriver')
wc.navigate_to_page(driver, 'https://www.realtor.com/')
codes = [95070, 95129]
for code in codes:
    soup = wc.navigate_to_code(driver, code)
    soups.update(soup)
homes_list = pcd.process_soups(soups, codes)
df = pcd.create_df(homes_list)
pcd.create_csv(df)

wc.terminate_driver(driver)

