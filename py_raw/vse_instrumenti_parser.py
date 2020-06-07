import pandas as pd
from tqdm import tqdm
from selenium import webdriver
import yaml
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


# ------------------------------------------------------------------------------------------------
def price_cutter(text):
    output_message = ''
    for i in text:
        if i.isdigit():
            output_message += i
    return output_message


# ------------------------------------------------------------------------------------------------
# get data from xlsx-file
def get_data_from_file():
    """
    read xlsx-file, convert it to the dataframe, return dataframe
    """
    # vse_bosch_df = pd.read_excel('./../data/vse_instrumenti_bosch.xlsx', engine='xlrd')  #  path for workout
    vse_bosch_df = pd.read_excel('~/5/competitor_prices/data/vse_instrumenti_bosch.xlsx', engine='xlrd')
    vse_bosch_witout_null_df = vse_bosch_df[vse_bosch_df['наш код'].notnull()]
    vse_bosch_witout_null_df.reset_index(inplace=True)

    # vse_metabo_df = pd.read_excel('./../data/vse_instrumenti_metabo.xlsx', engine='xlrd')
    vse_metabo_df = pd.read_excel('~/5/competitor_prices/data/vse_instrumenti_metabo.xlsx', engine='xlrd')
    vse_metabo_without_null_df = vse_metabo_df[vse_metabo_df['наш код'].notnull()]
    vse_metabo_without_null_df.reset_index(inplace=True)

    # vse_makita_df = pd.read_excel('./../data/vse_instrumenti_makita.xlsx', engine='xlrd')
    vse_makita_df = pd.read_excel('~/5/competitor_prices/data/vse_instrumenti_makita.xlsx', engine='xlrd')
    vse_makita_without_null_df = vse_makita_df[vse_makita_df['наш код'].notnull()]
    vse_makita_without_null_df.reset_index(inplace=True)

    result_df = vse_bosch_witout_null_df.append(vse_metabo_without_null_df, ignore_index=True)
    result_df = result_df.append(vse_makita_without_null_df, ignore_index=True)

    return result_df


# ------------------------------------------------------------------------------------------------
# parsing
def get_prices_code_dict(browser, df):
    code_price_dict = {}
    for i in tqdm(range(len(df['ссылка']))):  # len(df['ссылка'])
        try:
            browser.get(df['ссылка'][i])
            item_price = browser.find_element_by_css_selector('#b-product-info > div.right-block.card-right-aside > div.card-basket-block-new > div.ns.price-wrapper > div > span.price-value')
            code_price_dict[int(df['наш код'][i])] = price_cutter(item_price.text)
        except:
            continue

    our_code_price_df = pd.DataFrame.from_dict(code_price_dict, orient='index')

    return our_code_price_df


# ------------------------------------------------------------------------------------------------
# push dataframe to csv
def push_data_to_csv(name, data):
    file_path = '/home/krot/5/competitor_prices/xlsx/' + str(name) + '.csv'
    data.to_csv(file_path, sep=';', header=False)


# ------------------------------------------------------------------------------------------------
def get_login_password_from_yaml():
    try:
        with open('/home/krot/5/competitor_prices/data/lpt.yaml', 'r') as f:
            lpt = yaml.safe_load(f.read())
            server_address = lpt['server_address']
            login = lpt['server_login']
            password = lpt['server_password']
        return server_address, login, password
    except FileNotFoundError as e:
        error_message = ('get_token_from_yaml - ' + str(e) + ' no token-file')
        print(error_message)


# ------------------------------------------------------------------------------------------------
# push file to ftp
def push_file_to_ftp():
    server_address, login, password = get_login_password_from_yaml()
    local_server = '192.168.1.22'
    # os.system(f"sshpass -p {password} scp /home/krot/5/competitor_prices/xlsx/vse_instrumenti.csv {login}@{server_address}:/home/i/infotd5v/infotd5v.beget.tech/public_html/import_1c/competitor_prices")
    try:
        os.system(f"sshpass -p {password} scp /home/krot/5/competitor_prices/xlsx/vse_instrumenti.csv {login}@{server_address}:~/Python_main/competitor_prices/xlsx/")
    except:
        pass
    try:
        os.system(f"sshpass -p {password} scp /home/krot/5/competitor_prices/xlsx/vse_instrumenti.csv {login}@{local_server}:~/Python_main/competitor_prices/xlsx/")
    except:
        pass


##     ##    ###    #### ##    ##
###   ###   ## ##    ##  ###   ##
#### ####  ##   ##   ##  ####  ##
## ### ## ##     ##  ##  ## ## ##
##     ## #########  ##  ##  ####
##     ## ##     ##  ##  ##   ###
##     ## ##     ## #### ##    ##

if __name__ == "__main__":
    # options = Options()
    # options.headless = True
    # browser = webdriver.Firefox(options=options)

    browser = webdriver.Chrome()
    df = get_data_from_file()
    print(len(df))
    browser.implicitly_wait(3)
    code_price_df = get_prices_code_dict(browser, df)
    push_data_to_csv('vse_instrumenti', code_price_df)
    browser.quit()
    push_file_to_ftp()
