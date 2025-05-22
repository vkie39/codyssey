def caesar_cipher_decode(target_text):
    # 영어 사전 단어들 (보너스 과제용)
    common_words = [
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
        'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
        'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'mars', 'base',
        'door', 'open', 'password', 'key', 'emergency', 'storage', 'access',
        'system', 'code', 'security', 'enter', 'unlock', 'station', 'facility'
    ]
    
    results = []
    
    print('=== 카이사르 암호 해독 결과 ===\n')
    
    # 26가지 shift 값에 대해 모두 시도
    for shift in range(26):
        decoded_text = ''
        
        for char in target_text:
            if char.isalpha():
                # 대문자와 소문자 구분
                if char.isupper():
                    # A-Z (65-90)
                    decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    # a-z (97-122)
                    decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decoded_text += decoded_char
            else:
                # 알파벳이 아닌 문자는 그대로 유지
                decoded_text += char
        
        results.append((shift, decoded_text))
        
        # 결과 출력
        print(f'Shift {shift:2d}: {decoded_text}')
        
        # 보너스 과제: 사전 단어 확인
        decoded_lower = decoded_text.lower()
        found_words = []
        for word in common_words:
            if word in decoded_lower:
                found_words.append(word)
        
        if found_words:
            print(f'         → 발견된 단어: {", ".join(found_words)}')
            print(f'         → *** 이 결과가 정답일 가능성이 높습니다! ***')
        
        print()
    
    return results


def save_result_to_file(decoded_text, shift_value):
    """
    해독된 결과를 result.txt 파일에 저장하는 함수
    """
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(f'카이사르 암호 해독 결과\n')
            file.write(f'사용된 Shift 값: {shift_value}\n')
            file.write(f'해독된 텍스트: {decoded_text}\n')
        print(f'결과가 result.txt 파일에 저장되었습니다.')
        return True
    except Exception as e:
        print(f'파일 저장 중 오류가 발생했습니다: {e}')
        return False


def read_password_file():
    """
    password.txt 파일을 읽어오는 함수
    """
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            content = file.read().strip()
        print(f'password.txt 파일을 성공적으로 읽었습니다.')
        print(f'암호화된 텍스트: {content}\n')
        return content
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')

    except Exception as e:
        print(f'파일 읽기 중 오류가 발생했습니다: {e}')
        return None


def main():
    """
    메인 함수
    """
    print('=== 화성 기지 비상 저장소 암호 해독 시스템 ===\n')
    
    # password.txt 파일 읽기
    encrypted_text = read_password_file()
    
    if encrypted_text is None:
        print('프로그램을 종료합니다.')
        return
    
    # 카이사르 암호 해독
    results = caesar_cipher_decode(encrypted_text)
    
    # 사용자가 올바른 결과 선택
    while True:
        try:
            print('어떤 결과가 올바른 암호인 것 같습니까?')
            print('Shift 값을 입력하세요 (0-25, 종료하려면 -1): ', end='')
            
            choice = input().strip()
            
            if choice == '-1':
                print('프로그램을 종료합니다.')
                break
            
            shift_num = int(choice)
            
            if 0 <= shift_num <= 25:
                selected_result = results[shift_num][1]
                print(f'\n선택된 결과 (Shift {shift_num}): {selected_result}')
                
                # 결과 저장 확인
                save_confirm = input('이 결과를 result.txt에 저장하시겠습니까? (y/n): ').strip().lower()
                
                if save_confirm == 'y' or save_confirm == 'yes':
                    if save_result_to_file(selected_result, shift_num):
                        print('암호 해독 완료')
                    break
                else:
                    print('다른 결과를 선택해보세요.\n')
            else:
                print('0-25 범위의 숫자를 입력하세요.')
                
        except ValueError:
            print('올바른 숫자를 입력하세요.')
        except KeyboardInterrupt:
            print('\n\n프로그램이 중단되었습니다.')
            break
        except Exception as e:
            print(f'오류가 발생했습니다: {e}')


if __name__ == '__main__':
    main()