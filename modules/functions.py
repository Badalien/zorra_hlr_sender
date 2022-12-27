from modules import reader as rd
from modules import zorra_hlr
import time
import csv
import numpy as np
from modules.logger import logger


# read numbers from console
def read_numbers_console() -> list:
    numbers = []
    user_input = ''

    while True:
        user_input = input()
        if user_input == "OK":
            break
        numbers.append(user_input)
    return numbers


# read numbers from file to list
def read_numbers_file(file_path: str) -> list:
    reader = rd.FileReader(file_path)
    reader.read_file()
    reader.read_columns()
    columns = reader.get_columns()
    print('Choose column to read numbers: ')
    for i in range(len(columns)):
        print(f'{i + 1}. {columns[i]}')
    column_number = input('Enter column number: ')
    numbers = reader.df_to_list(columns[int(column_number) - 1])
    return numbers


# login to Zorra and get token
def zorra_login(email: str, password: str) -> zorra_hlr.ZorraHLR:
    zorra = zorra_hlr.ZorraHLR(email, password)
    zorra.get_token()
    zorra.get_user_id()
    return zorra


# format hlr_stats to output data structure
def beutify_hlr_stat_row(hlr_stat_row: dict) -> dict:
    stat_row_nice = {}
    stat_row_nice['request_id'] = hlr_stat_row['request_id']
    stat_row_nice['number'] = hlr_stat_row['number']
    stat_row_nice['state'] = hlr_stat_row['state']
    stat_row_nice['mcc'] = hlr_stat_row['mcc_default']
    stat_row_nice['mnc'] = hlr_stat_row['mnc_default']
    stat_row_nice['available'] = hlr_stat_row['available']
    stat_row_nice['ported'] = hlr_stat_row['ported']
    stat_row_nice['info'] = hlr_stat_row['info']
    return stat_row_nice


# get hlr_stats from Zorra
def get_hlr_stats(zorra: zorra_hlr.ZorraHLR, request_ids_list: list) -> list:  # noqa: E501
    hlr_stats = []
    start_time = time.time()
    ids_count = len(request_ids_list)
    time_to_wait = np.log(ids_count)**3 + 60  # we set time to sleep before requesting results as ln() of requests count
    print(f'You sent {ids_count} requests.\n')
    logger(f'You sent {ids_count} requests.\n')
    print(f'Start getting HLR stats... (waiting {time_to_wait} seconds)')
    logger(f'Start getting HLR stats... (waiting {time_to_wait} seconds)')
    while True:  # noqa: E501
        for request_id in request_ids_list:
            hlr_stat = zorra.get_stat_by_id(request_id)
            if hlr_stat['state'] in ['finished', 'invalid', 'rejected']:
                hlr_stat_row = beutify_hlr_stat_row(hlr_stat)
                hlr_stats.append(hlr_stat_row)
                request_ids_list.remove(request_id)
        print(f'{ids_count - len(request_ids_list)} results ready.')
        logger(f'{ids_count - len(request_ids_list)} results ready.')
        if len(request_ids_list) == 0:
            break
        if time.time() - start_time > time_to_wait:
            break
        iteration_sleep = time_to_wait / ids_count
        print(f'Sleeping for {iteration_sleep} seconds...')
        time.sleep(iteration_sleep)

    return hlr_stats


# postprocess hlr_stat and prepare for writing to csv
def postprocess_hlr_stat(hlr_stat: dict) -> dict:
    for key in hlr_stat:
        if hlr_stat[key] is None:
            hlr_stat[key] = 'False'
    return hlr_stat


# write results to csv file
def list_of_dicts_to_csv(list_of_dicts: list, file_path: str) -> None:
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = list_of_dicts[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for d in list_of_dicts:
            writer.writerow(d)
