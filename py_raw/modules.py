import pandas as pd
import requests
import smtplib
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from email.message import EmailMessage


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


# ------------------------------------------------------------------------------------------------
# send files to email
def email_sender():
    email_pass = 'tvcabitgcvuqalje'
    email_user = 'a.sushchikh@gmail.com'
    # contacts_list = ['info@td-stroybat.ru']
    contacts_list = ['a89638857493@gmail.com']

    msg = EmailMessage()
    msg['Subject'] = 'Instrument, Makita prices'
    msg['From'] = 'email_user'
    msg['To'] = ', '.join(contacts_list)
    msg.set_content(
        ' ')
    files_xlsx = []

    files_xlsx.append('./../xlsx/instrument_prices.csv')
    files_xlsx.append('./../xlsx/makita_prices.csv')

    for file in files_xlsx:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)


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
    #instr_df = pd.read_excel('./../data/Instrument_price.xlsx', engine='xlrd')  #  path for workout
    instr_df = pd.read_excel('~/Python_main/competitor_prices/data/Instrument_prices.xlsx', engine='xlrd')
    instr_df_with_our_code = instr_df[instr_df['наш код'].notnull()]

    #makita_df = pd.read_excel('./../data/makita_prices.xlsx', engine='xlrd')
    makita_df = pd.read_excel('~/Python_main/competitor_prices/data/makita_prices.xlsx', engine='xlrd')
    makita_df_with_our_code = makita_df[makita_df['Наш код'].notnull()]

    return instr_df_with_our_code, makita_df_with_our_code


# ------------------------------------------------------------------------------------------------
# push data to xlsx-file, decorate it
def push_data_to_xlsx(name, data):
    # today = datetime.today()
    file_path = './../xlsx/' + str(name) + '.xlsx'
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
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


# ------------------------------------------------------------------------------------------------
# push dataframe to csv
def push_data_to_csv(name, data):
    file_path = './../xlsx/' + str(name) + '.csv'
    data.to_csv(file_path, sep=';', header=False)

########     ###    ########   ######  #### ##    ##  ######
##     ##   ## ##   ##     ## ##    ##  ##  ###   ## ##    ##
##     ##  ##   ##  ##     ## ##        ##  ####  ## ##
########  ##     ## ########   ######   ##  ## ## ## ##   ####
##        ######### ##   ##         ##  ##  ##  #### ##    ##
##        ##     ## ##    ##  ##    ##  ##  ##   ### ##    ##
##        ##     ## ##     ##  ######  #### ##    ##  ######


# ------------------------------------------------------------------------------------------------
# parsing all items in data, take price-value from instrument site, add it to the dataframe
def get_df_with_prices_instr(data_instr):
    """
    data: pandas dataframe
    return: pandas dataframe with price for ich item
    """
    our_code_price_df = []  # meanwhile df is empty
    data_instr.reset_index(inplace=True)
    our_code_price_dict = {}
    session = requests.Session()
    for i in tqdm(range(len(data_instr['ссылка']))):
        try:
            response = session.get(data_instr['ссылка'][i])
            if response.status_code == 200:
                soup = bs(response.content, 'html.parser')
                price_value = price_cutter(soup.select('body > div.wrap > div.container.container_mobile.page__container.sticky-inside.content > div.product-view > div:nth-child(1) > div.col.l3.s12.sticky > div.product-view__wrap.product-view__buy-wrap.side-bar.hide-on-small-only > div:nth-child(1) > div > div.product-view__prices > div.product-view__price-value')[0].get_text().strip())
            else:
                price_value = 0  # todo прописать правильное назначение ноля, если не смог спарсить
            our_code_price_dict[int(data_instr['наш код'][i])] = [price_value]
            our_code_price_df = pd.DataFrame.from_dict(our_code_price_dict, orient='index')
        except Exception as e:
            with open('./../logs/log_1.txt', 'a') as f:
                f.write(f'error on parsing {data_instr["cсылка"][i]}, - {e}')

    return our_code_price_df


# ------------------------------------------------------------------------------------------------
# parsing all items in data, take price-value from makita-site, and push it to dataframe
def get_df_with_prices_makita(data_makita):
    """
    data-makita: pandas dataframe
    return: pandas dataframe with price for ich item
    """
    our_code_price_df = []  # empty output_list
    data_makita.reset_index(inplace=True)
    our_code_price_dict = {}
    session = requests.Session()
    for i in tqdm(range(len(data_makita['Cсылка']))):
        try:
            response = session.get(data_makita['Cсылка'][i])
            if response.status_code == 200:
                soup = bs(response.content, 'html.parser')
                price_value = price_cutter(soup.select('#content > div.product-info > div > div.extra-wrap > div.price > span')[0].get_text().strip())
            else:
                price_value = 0  # TODO прописать правильное назначение ноля, если не смог спарсить
            our_code_price_dict[int(data_makita['Наш код'][i])] = [price_value]
            our_code_price_df = pd.DataFrame.from_dict(our_code_price_dict, orient='index')
        except Exception as e:
            print(f'{e}')
            with open('./../logs/log_1.txt', 'a') as f:
                f.write(f'error on parsing {data_makita["Ссылка"][i]}, - {e}')

    return our_code_price_df



