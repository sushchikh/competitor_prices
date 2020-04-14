import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from datetime import datetime




######## ########    ###    ######## ##     ## ########  ########  ######
##       ##         ## ##      ##    ##     ## ##     ## ##       ##    ##
##       ##        ##   ##     ##    ##     ## ##     ## ##       ##
######   ######   ##     ##    ##    ##     ## ########  ######    ######
##       ##       #########    ##    ##     ## ##   ##   ##             ##
##       ##       ##     ##    ##    ##     ## ##    ##  ##       ##    ##
##       ######## ##     ##    ##     #######  ##     ## ########  ######


# ------------------------------------------------------------------------------------------------
# get only int value of incoming text
def price_cutter(text: str):
    output_message = ''
    for i in text:
        if i.isdigit() or i == '.' or i == ',':
            output_message += i
    return str(output_message)


########     ###    ########    ###
##     ##   ## ##      ##      ## ##
##     ##  ##   ##     ##     ##   ##
##     ## ##     ##    ##    ##     ##
##     ## #########    ##    #########
##     ## ##     ##    ##    ##     ##
########  ##     ##    ##    ##     ##

# ------------------------------------------------------------------------------------------------
# get data from xlsx-file
def get_data_from_file():
    """
    read xlsx-file, convert it to the dataframe, return dataframe
    """
    instr_df = pd.read_excel('./../data/Instrument_price.xlsx', engine='xlrd')
    instr_df_with_our_code = instr_df[instr_df['наш код'].notnull()]

    # TODO make code for take "makita" dataframe from file
    return instr_df_with_our_code


# TODO func must take "name" arg and make file with that arg in path
# ------------------------------------------------------------------------------------------------
# push data to xlsx-file, decorate it
def push_data_to_xlsx(data):
    today = datetime.today()
    name = './../xlsx/instrument_price_our_code_' + today.strftime("%d.%m.%Y") + '.xlsx'
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1', index=True)
    workbook = writer.book
    cell_format = workbook.add_format({
        # 'bold': True,
        # 'font_color': 'black',
        'align': 'center',
        'valign': 'center',
        # 'bg_color': '#ecf0f1'
    })
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.write('A1', 'code', cell_format)
    worksheet.write('B1', 'price', cell_format)
    # worksheet.freeze_panes(1, 0)
    writer.save()


########     ###    ########   ######  #### ##    ##  ######
##     ##   ## ##   ##     ## ##    ##  ##  ###   ## ##    ##
##     ##  ##   ##  ##     ## ##        ##  ####  ## ##
########  ##     ## ########   ######   ##  ## ## ## ##   ####
##        ######### ##   ##         ##  ##  ##  #### ##    ##
##        ##     ## ##    ##  ##    ##  ##  ##   ### ##    ##
##        ##     ## ##     ##  ######  #### ##    ##  ######


# ------------------------------------------------------------------------------------------------
# parsing all items in data, take price-value from instrument site, add it to the dataframe
def get_df_with_prices_instr(data):
    """
    data: pandas dataframe
    return: pandas dataframe with price for ich item
    """
    our_code_price_df = []  # meanwhile df is empty
    data.reset_index(inplace=True)
    our_code_price_dict = {}
    session = requests.Session()
    for i in tqdm(range(len(data['ссылка']))):
        try:
            response = session.get(data['ссылка'][i])
            if response.status_code == 200:
                soup = bs(response.content, 'html.parser')
                price_value = price_cutter(soup.select('body > div.wrap > div.container.container_mobile.page__container.sticky-inside.content > div.product-view > div:nth-child(1) > div.col.l3.s12.sticky > div.product-view__wrap.product-view__buy-wrap.side-bar.hide-on-small-only > div:nth-child(1) > div > div.product-view__prices > div.product-view__price-value')[0].get_text().strip())
            else:
                price_value = 0  # todo прописать правильное назначение ноля, если не смог спарсить
            our_code_price_dict[int(data['наш код'][i])] = [price_value]
            our_code_price_df = pd.DataFrame.from_dict(our_code_price_dict, orient='index')
        except Exception as e:
            with open('./../logs/log_1.txt', 'a') as f:
                f.write(f'error on parsing {data["cсылка"][i]}, - {e}')

    return our_code_price_df


# ------------------------------------------------------------------------------------------------
# parsing makita-ite for prices and push it to the dataframe
def get_df_with_prices_makita(data):
    pass
