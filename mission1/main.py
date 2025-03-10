try:
    with open('mission1\mission_computer_main.log', 'r', encoding='utf-8') as file:
        print_log = file.readlines()  ##.read: 파일 전체, .readlines: 라인 별
        for line in reversed(print_log):  #reversed: 거꾸로
            print(line, end = '')

        print('\n\n\n오류 발생: ')
        for line in print_log[-3:]:
            print(line, end = '')
    
    with open('mission1\Error.log', 'w', encoding='utf-8') as file:
        for line in print_log[-3:]:
            file.write(line)

except FileNotFoundError:
    print("Error: The file 'mission_computer_main.log' was not found.")

except IOError: #Input/Output Error
    print("Error: An I/O error occurred while reading the file.")

