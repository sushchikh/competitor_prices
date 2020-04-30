from time import sleep
from modules import get_data_from_file
from modules import get_df_with_prices_instr
from modules import push_data_to_xlsx
from modules import get_df_with_prices_makita
from modules import push_data_to_csv


if __name__ == '__main__':
    instr_df, makita_df = get_data_from_file()
    print('parsing Instrument:')
    sleep(0.2)
    code_prices_instr_df = get_df_with_prices_instr(instr_df)

    print('parsing Makita:')
    sleep(0.2)
    code_prices_makita_df = get_df_with_prices_makita(makita_df)
    name = 'instrument_prices'
    # push_data_to_xlsx(name, code_prices_instr_df)
    print('push Instrument to csv')
    push_data_to_csv(name, code_prices_instr_df)
    name = 'makita_prices'
    # push_data_to_xlsx(name, code_prices_makita_df)
    print('push Makita to csv')
    push_data_to_csv(name, code_prices_makita_df)
    # print(code_prices_df.head())
    # email_sender()
