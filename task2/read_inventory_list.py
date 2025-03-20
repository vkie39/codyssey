# CSV 파일 읽기
file_name = 'task2/Mars_Base_Inventory_List.csv'
inventory_list = []
header = []  # header 변수를 try 블록 밖에서 정의

try:
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')  # 첫 줄은 헤더
        print(header)
        inventory_list = [line.strip().split(',') for line in lines[1:]]  # 데이터 읽기

    print("CSV 파일 읽기 성공:", inventory_list[:])

except FileNotFoundError:
    print("Error: The file 'Mars_Base_Inventory_List.csv' was not found.")
    inventory_list = []  # 파일이 없을 경우 빈 리스트 유지

except IOError:
    print("Error: An I/O error occurred while reading the file.")

# Flammability 값을 기준으로 정렬 (내림차순)
try:
    inventory_list = sorted(inventory_list, key=lambda x: float(x[4]), reverse=True)
    print("\n\n\nFlammability 내림차순 정렬된 데이터:", inventory_list[:])

except IndexError:
    print("Error: 데이터 구조가 예상과 다릅니다.")

except ValueError:
    print("Error: Flammability 값이 숫자가 아닙니다.")

# 바이너리 파일 쓰기
bin_file = 'task2/Mars_Base_Inventory_List.bin'

try:
    with open(bin_file, 'wb') as file:
        for item in inventory_list:
            file.write(",".join(item).encode() + b'\n')

    # 바이너리 파일 읽기
    loaded_list = []
    with open(bin_file, 'rb') as file:
        loaded_list = [line.decode().strip().split(',') for line in file]

except FileNotFoundError:
    print("Error: 바이너리 파일이 존재하지 않습니다.")

except IOError:
    print("Error: 파일 입출력 중 오류가 발생했습니다.")

print("바이너리 파일 로드된 데이터:", loaded_list[:5])

# Flammability > 0.7 항목 필터링
F7 = [item for item in inventory_list if float(item[4]) > 0.7]

print("Flammability > 0.7 필터링된 데이터:", F7[:])

# 필터링된 데이터 CSV로 저장 (csv 모듈 없이)
filtered_csv = 'task2/Mars_Base_Inventory_danger.csv'

try:
    with open(filtered_csv, 'w', encoding='utf-8') as file:
        file.write(",".join(header) + '\n')  # 헤더 추가
        for item in F7:
            file.write(",".join(item) + '\n')  # 데이터 추가

except FileNotFoundError:
    print("Error: The file 'Mars_Base_Inventory_danger.csv' was not found.")

except IOError:
    print("Error: An I/O error occurred while writing the file.")

except PermissionError:
    print("Error: 파일 접근 권한이 없습니다.")