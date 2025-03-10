import pandas as pd
import pickle

try: #csv_file: csv파일
    csv_file = pd.read_csv('task2/Mars_Base_Inventory_List.csv')
    print(csv_file.head()) 

except FileNotFoundError:
    print("Error: The file 'Mars_Base_Inventory_List.csv' was not found.")

except IOError: #Input/Output Error
    print("Error: An I/O error occurred while reading the file.")


#to_list: csv_file 리스트로 변환
to_list = csv_file.values.tolist()
print(to_list[:5])

to_list = sorted(to_list, key=lambda x: x[4], reverse=True) #Flammability 내림차순 정열
print('\n\n\n', to_list[:5])

# 바이너리 파일 쓰기
try:
    with open('task2/Mars_Base_Inventory_List.bin', 'wb') as write_bin:
        pickle.dump(to_list, write_bin) 

    # 바이너리 파일 읽기
    with open('task2/Mars_Base_Inventory_List.bin', 'rb') as read_bin:
        loaded_list = pickle.load(read_bin)

except FileNotFoundError:
    print("Error: 바이너리 파일이 존재하지 않습니다.")

except EOFError:
    print("Error: 파일의 데이터가 손상되었거나 비어있습니다.")

except pickle.PickleError:
    print("Error: pickle 데이터의 형식이 올바르지 않습니다.")

except PermissionError:
    print("Error: 파일 접근 권한이 없습니다.")

except IOError:
    print("Error: 파일 입출력 중 오류가 발생했습니다.")

print(loaded_list)


#Flammability > 0.7 항목 필터링
#F7: 필터링한 항목
F7 = list(filter(lambda x: x[4] >=0.7, to_list))
print(F7)

try:
    F7 = pd.DataFrame(F7, columns=csv_file.columns)
    F7.to_csv('task2/Mars_Base_Inventory_danger.csv', index=False)

except FileNotFoundError:
    print("Error: The file 'Mars_Base_Inventory_danger.csv' was not found.")

except IOError:
    print("Error: An I/O error occurred while reading the file.")

except PermissionError:
    print("Error: 파일 접근 권한이 없습니다.")