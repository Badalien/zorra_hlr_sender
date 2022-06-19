from modules import functions as fs
from getpass import getpass
from pprint import pp
import datetime
import pytz

# read user credentials from console
print('This app helps you to send HLR requests to Zorra.')
email = input('Enter your email: ')
password = getpass('Enter your password: ')

zorra = fs.zorra_login(email, password)

if zorra.token:
    print('Successful login to Zorra.')


print("\n\n")
print("Choose mode:")
print("1 - Read numbers from file")
print("2 - Read numbers from console")
mode = input("Enter mode: ")


# define numbers read mode
def read_mode(mode: str) -> list:
    if mode == "1":
        file_path = input("Enter file path: ")
        return fs.read_numbers_file(file_path)
    elif mode == "2":
        print("Enter numbers one by one (enter \"OK\" to finish):")
        return fs.read_numbers_console()
    else:
        read_mode(input("Wrong input! Enter mode: "))


numbers_list = read_mode(mode)
request_ids_list = []

print('\nStart sending HLR requests...')
for number in numbers_list:
    print(f'Sending HLR request for number: {number}')
    response = zorra.send_hlr_background(number)
    request_ids_list.append(response)
print('Sending finished.\n')


stat_to_file = fs.get_hlr_stats(zorra, request_ids_list)

for s in range(len(stat_to_file)):
    stat_to_file[s] = fs.postprocess_hlr_stat(stat_to_file[s])

pp(stat_to_file, indent=4)

output_file_path = input('\nEnter directory for output file: ')

output_file_name = f'{output_file_path}/hlr_results_{datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d_%H-%M-%S")}.csv'  # noqa: E501

print(f'Writing results to file: {output_file_name}')
fs.list_of_dicts_to_csv(stat_to_file, output_file_name)
input('\nPress any key to exit...')
