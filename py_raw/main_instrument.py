from modules import get_data_from_file
from modules import get_df_with_prices
from modules import push_data_to_xlsx

if __name__ == '__main__':
    instr_df = get_data_from_file()
    code_prices_df = get_df_with_prices(instr_df)
    push_data_to_xlsx(code_prices_df)
    # print(code_prices_df.head())

