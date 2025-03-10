import pandas as pd

try: #csv_file: csv파일
    csv_file = pd.read_csv('task2/Mars_Base_Inventory_List.csv')
    print(csv_file.head()) 

except FileNotFoundError:
    print("Error: The file 'mission_computer_main.log' was not found.")

except IOError: #Input/Output Error
    print("Error: An I/O error occurred while reading the file.")


#to_list: csv_file 리스트로 변환
to_list = csv_file.values.tolist()
print(to_list[:5])

to_list = sorted(to_list, key=lambda x: x[4]) #Flammability 오름차순 정열
print('\n\n\n', to_list[:5])
