location = 'task2/'
csvF = "Mars_Base_Inventory_List.csv"
binF = "Mars_Base_Inventory_List.bin"
filtered_csvF = "Mars_Base_Inventory_danger.csv"

def read_csv(file_path):
    inventory_list = []
    header = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            header = lines[0].strip().split(',')  # 첫 줄은 헤더
            inventory_list = [line.strip().split(',') for line in lines[1:]]  # 데이터 읽기
        print("CSV 파일 읽기 성공:", inventory_list[:5])
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError:
        print("Error: An I/O error occurred while reading the file.")
    return header, inventory_list

def write_binary(file_path, inventory_list):
    try:
        with open(file_path, 'wb') as file:
            for item in inventory_list:
                file.write(",".join(item).encode() + b'\n')
        print("바이너리 파일 쓰기 성공:", file_path)
    except IOError:
        print("Error: An I/O error occurred while writing the file.")

def read_binary(file_path):
    loaded_list = []
    try:
        with open(file_path, 'rb') as file:
            loaded_list = [line.decode().strip().split(',') for line in file]
        print("바이너리 파일 읽기 성공:", loaded_list[:5])
    except FileNotFoundError:
        print(f"Error: The binary file '{file_path}' was not found.")
    except IOError:
        print("Error: An I/O error occurred while reading the file.")
    return loaded_list

def write_csv(file_path, header, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(",".join(header) + '\n')  # 헤더 추가
            for item in data:
                file.write(",".join(item) + '\n')  # 데이터 추가
        print("CSV 파일 쓰기 성공:", file_path)
    except IOError:
        print("Error: An I/O error occurred while writing the file.")
    except PermissionError:
        print("Error: 파일 접근 권한이 없습니다.")

# CSV 파일 읽기
header, inventory_list = read_csv(location + csvF)

# Flammability 값을 기준으로 정렬 (내림차순)
try:
    inventory_list = sorted(inventory_list, key=lambda x: float(x[4]), reverse=True)
    print("\n\n\nFlammability 내림차순 정렬된 데이터:", inventory_list[:5])
except IndexError:
    print("Error: 데이터 구조가 예상과 다릅니다.")
except ValueError:
    print("Error: Flammability 값이 숫자가 아닙니다.")

# 바이너리 파일 쓰기
write_binary(location + binF, inventory_list)

# 바이너리 파일 읽기
loaded_list = read_binary(location + binF)

# Flammability > 0.7 항목 필터링
F7 = [item for item in inventory_list if float(item[4]) > 0.7]
print("Flammability > 0.7 필터링된 데이터:", F7[:5])

# 필터링된 데이터 CSV로 저장
write_csv(location + filtered_csvF, header, F7)