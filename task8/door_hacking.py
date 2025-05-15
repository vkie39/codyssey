#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZIP 파일 암호 해독 프로그램 (최적화 버전)

6자리 숫자와 소문자 알파벳으로 구성된 암호를 효율적으로 해독합니다.
"""

import zipfile
import time
import string
import itertools
import os
import zlib
import multiprocessing


def try_password(args):
    """
    주어진 패스워드로 ZIP 파일 암호 해제를 시도합니다.
    
    Args:
        args: (zip_path, password) 튜플
        
    Returns:
        성공 시 패스워드, 실패 시 None
    """
    zip_path, password = args
    
    try:
        with zipfile.ZipFile(zip_path) as zip_file:
            # 하나의 파일만 추출 시도
            for zip_info in zip_file.infolist():
                try:
                    zip_file.extract(zip_info, pwd=password.encode())
                    # 성공하면 암호 반환
                    return password
                except (zipfile.BadZipFile, RuntimeError, zlib.error):
                    break
    except Exception:
        pass
    
    return None


def unlock_zip(zip_path='emergency_storage_key.zip', output_file='password.txt', 
               num_processes=None, pattern=None, start_with=None, common_patterns=True):
    """
    ZIP 파일의 암호를 효율적인 방식으로 해독합니다.
    
    Args:
        zip_path (str): 해독할 ZIP 파일 경로
        output_file (str): 찾은 암호를 저장할 파일 경로
        num_processes (int): 사용할 프로세스 수 (기본값: CPU 코어 수)
        pattern (str): 암호에 적용할 패턴 (예: 'ddddaa' - 4개의 숫자 + 2개의 소문자)
        start_with (str): 이 문자열로 시작하는 암호만 시도
        common_patterns (bool): 일반적인 패턴을 먼저 시도할지 여부
        
    Returns:
        str or None: 성공 시 암호, 실패 시 None
    """
    # 파일 존재 확인
    if not os.path.exists(zip_path):
        print(f'오류: {zip_path} 파일을 찾을 수 없습니다.')
        return None
    
    try:
        # ZIP 파일 열기
        zip_file = zipfile.ZipFile(zip_path)
    except zipfile.BadZipFile:
        print(f'오류: {zip_path}는 올바른 ZIP 파일이 아닙니다.')
        return None
    
    # ZIP 파일에 파일이 있는지 확인
    if len(zip_file.namelist()) == 0:
        print(f'오류: {zip_path}에 파일이 없습니다.')
        zip_file.close()
        return None
    
    zip_file.close()
    
    # 사용할 문자 세트
    digits = string.digits
    lower_letters = string.ascii_lowercase
    
    # 암호 길이
    password_length = 6
    
    # 브루트포스 시작
    start_time = time.time()
    total_attempts = 0
    last_report_time = start_time
    
    print('암호 해독 시작...')
    
    # 멀티프로세싱 설정
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    print(f'CPU 코어 {num_processes}개를 사용하여 병렬 처리합니다.')
    
    # 가능한 패턴 목록
    if pattern:
        patterns = [pattern]
    elif common_patterns:
        # 일반적인 패턴 먼저 시도 (예: 모두 숫자, 모두 문자, 숫자+문자 조합)
        patterns = [
            'dddddd',       # 모두 숫자 (예: 123456)
            'aaaaaa',       # 모두 문자 (예: abcdef)
            'dddaaa',       # 숫자 3개 + 문자 3개 (예: 123abc)
            'aaaddd',       # 문자 3개 + 숫자 3개 (예: abc123)
            'ddddaa',       # 숫자 4개 + 문자 2개 (예: 1234ab)
            'aadddd',       # 문자 2개 + 숫자 4개 (예: ab1234)
            'adadad',       # 문자/숫자 교차 (예: a1b2c3)
            'dadada',       # 숫자/문자 교차 (예: 1a2b3c)
            'mixed'         # 나머지 모든 조합
        ]
    else:
        patterns = ['mixed']
    
    # 패턴별로 암호 시도
    for current_pattern in patterns:
        pattern_start_time = time.time()
        pattern_attempts = 0
        
        print(f'\n패턴 "{current_pattern}" 시도 중...')
        
        # 패턴에 따른 조합 생성 함수
        if current_pattern == 'dddddd':
            # 모두 숫자
            combinations = itertools.product(digits, repeat=password_length)
            max_combinations = len(digits) ** password_length
        elif current_pattern == 'aaaaaa':
            # 모두 문자
            combinations = itertools.product(lower_letters, repeat=password_length)
            max_combinations = len(lower_letters) ** password_length
        elif current_pattern == 'dddaaa':
            # 숫자 3개 + 문자 3개
            combinations = (d1+d2+d3+a1+a2+a3 for d1, d2, d3 in itertools.product(digits, repeat=3)
                          for a1, a2, a3 in itertools.product(lower_letters, repeat=3))
            max_combinations = len(digits)**3 * len(lower_letters)**3
        elif current_pattern == 'aaaddd':
            # 문자 3개 + 숫자 3개
            combinations = (a1+a2+a3+d1+d2+d3 for a1, a2, a3 in itertools.product(lower_letters, repeat=3)
                          for d1, d2, d3 in itertools.product(digits, repeat=3))
            max_combinations = len(digits)**3 * len(lower_letters)**3
        elif current_pattern == 'ddddaa':
            # 숫자 4개 + 문자 2개
            combinations = (d1+d2+d3+d4+a1+a2 for d1, d2, d3, d4 in itertools.product(digits, repeat=4)
                          for a1, a2 in itertools.product(lower_letters, repeat=2))
            max_combinations = len(digits)**4 * len(lower_letters)**2
        elif current_pattern == 'aadddd':
            # 문자 2개 + 숫자 4개
            combinations = (a1+a2+d1+d2+d3+d4 for a1, a2 in itertools.product(lower_letters, repeat=2)
                          for d1, d2, d3, d4 in itertools.product(digits, repeat=4))
            max_combinations = len(digits)**4 * len(lower_letters)**2
        elif current_pattern == 'adadad':
            # 문자/숫자 교차 (a1d1a2d2a3d3)
            combinations = (a1+d1+a2+d2+a3+d3 for a1, a2, a3 in itertools.product(lower_letters, repeat=3)
                          for d1, d2, d3 in itertools.product(digits, repeat=3))
            max_combinations = len(digits)**3 * len(lower_letters)**3
        elif current_pattern == 'dadada':
            # 숫자/문자 교차 (d1a1d2a2d3a3)
            combinations = (d1+a1+d2+a2+d3+a3 for d1, d2, d3 in itertools.product(digits, repeat=3)
                          for a1, a2, a3 in itertools.product(lower_letters, repeat=3))
            max_combinations = len(digits)**3 * len(lower_letters)**3
        else:  # 'mixed'
            # 모든 가능한 조합 (일반적인 패턴 이후에 남은 것들)
            chars = digits + lower_letters
            combinations = itertools.product(chars, repeat=password_length)
            max_combinations = len(chars) ** password_length
        
        # 시작 문자열 필터링
        if start_with:
            combinations = (''.join(c) for c in combinations if ''.join(c).startswith(start_with))
            print(f'"{start_with}"로 시작하는 암호만 시도합니다.')
        else:
            combinations = (''.join(c) for c in combinations)
        
        print(f'이 패턴의 최대 조합 수: {max_combinations:,}개')
        
        # 암호 목록 생성 및 분할
        password_batch_size = 1000  # 한 번에 처리할 암호 수
        with multiprocessing.Pool(processes=num_processes) as pool:
            password_batch = []
            
            for password in combinations:
                password_batch.append((zip_path, password))
                pattern_attempts += 1
                total_attempts += 1
                
                # 진행 상황 보고
                current_time = time.time()
                if current_time - last_report_time >= 1:
                    elapsed = current_time - start_time
                    attempts_per_second = total_attempts / elapsed if elapsed > 0 else 0
                    progress_percent = (pattern_attempts / max_combinations) * 100 if max_combinations > 0 else 0
                    
                    print(f'진행 중: 패턴 "{current_pattern}" | '
                          f'시도: {total_attempts:,} | '
                          f'진행률: {progress_percent:.2f}% | '
                          f'경과 시간: {elapsed:.2f}초 | '
                          f'초당 시도 횟수: {attempts_per_second:.2f}')
                    last_report_time = current_time
                
                # 배치 처리
                if len(password_batch) >= password_batch_size:
                    results = pool.map(try_password, password_batch)
                    for result in results:
                        if result:
                            # 암호 찾음
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            
                            print('\n암호 발견!')
                            print(f'암호: {result}')
                            print(f'시도 횟수: {total_attempts:,}')
                            print(f'소요 시간: {elapsed_time:.2f}초')
                            
                            # 암호를 파일에 저장
                            try:
                                with open(output_file, 'w') as f:
                                    f.write(result)
                                print(f'암호가 {output_file}에 저장되었습니다.')
                            except IOError as e:
                                print(f'경고: 암호를 파일에 저장하는 데 실패했습니다. {e}')
                            
                            return result
                    
                    # 배치 초기화
                    password_batch = []
            
            # 남은 암호 처리
            if password_batch:
                results = pool.map(try_password, password_batch)
                for result in results:
                    if result:
                        # 암호 찾음
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        
                        print('\n암호 발견!')
                        print(f'암호: {result}')
                        print(f'시도 횟수: {total_attempts:,}')
                        print(f'소요 시간: {elapsed_time:.2f}초')
                        
                        # 암호를 파일에 저장
                        try:
                            with open(output_file, 'w') as f:
                                f.write(result)
                            print(f'암호가 {output_file}에 저장되었습니다.')
                        except IOError as e:
                            print(f'경고: 암호를 파일에 저장하는 데 실패했습니다. {e}')
                        
                        return result
        
        # 이 패턴으로 암호를 찾지 못함
        pattern_end_time = time.time()
        pattern_elapsed_time = pattern_end_time - pattern_start_time
        print(f'패턴 "{current_pattern}" 완료 (찾지 못함): {pattern_attempts:,}개 시도, {pattern_elapsed_time:.2f}초 소요')
    
    # 모든 패턴을 시도했으나 암호를 찾지 못함
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print('\n암호를 찾지 못했습니다.')
    print(f'시도 횟수: {total_attempts:,}')
    print(f'소요 시간: {elapsed_time:.2f}초')
    
    return None


if __name__ == '__main__':
    try:
        print('ZIP 파일 암호 해독 최적화 버전을 시작합니다.')
        print('(종료하려면 Ctrl+C를 누르세요)')
        
        # 파일 경로 입력받기
        zip_path = input('해독할 ZIP 파일 경로 (기본값: emergency_storage_key.zip): ').strip()
        if not zip_path:
            zip_path = 'emergency_storage_key.zip'
        
        if not os.path.exists(zip_path):
            print(f'오류: {zip_path} 파일을 찾을 수 없습니다.')
            exit(1)
        
        # 최적화 옵션 입력받기
        use_optimization = input('최적화 옵션을 사용하시겠습니까? (Y/n): ').strip().lower() != 'n'
        
        if use_optimization:
            # 시작 문자열 힌트
            start_hint = input('암호의 시작 부분을 알고 있다면 입력하세요 (예: a1, 123 등): ').strip()
            start_with = start_hint if start_hint else None
            
            # 패턴 힌트
            print('\n사용할 패턴을 선택하세요:')
            print('1: 모두 숫자 (예: 123456)')
            print('2: 모두 문자 (예: abcdef)')
            print('3: 숫자 3개 + 문자 3개 (예: 123abc)')
            print('4: 문자 3개 + 숫자 3개 (예: abc123)')
            print('5: 숫자 4개 + 문자 2개 (예: 1234ab)')
            print('6: 문자 2개 + 숫자 4개 (예: ab1234)')
            print('7: 문자/숫자 교차 (예: a1b2c3)')
            print('8: 숫자/문자 교차 (예: 1a2b3c)')
            print('9: 일반적인 패턴을 순서대로 모두 시도')
            print('0: 모든 가능한 조합 시도')
            
            pattern_choice = input('선택 (기본값: 9): ').strip() or '9'
            
            pattern_map = {
                '1': 'dddddd',
                '2': 'aaaaaa',
                '3': 'dddaaa',
                '4': 'aaaddd',
                '5': 'ddddaa',
                '6': 'aadddd',
                '7': 'adadad',
                '8': 'dadada',
                '9': None,  # 일반적인 패턴 모두 시도
                '0': 'mixed'  # 모든 조합
            }
            
            selected_pattern = pattern_map.get(pattern_choice)
            use_common_patterns = pattern_choice == '9'
            
            # CPU 코어 설정
            cpu_cores = multiprocessing.cpu_count()
            core_input = input(f'사용할 CPU 코어 수 (기본값: {cpu_cores}): ').strip()
            num_processes = int(core_input) if core_input.isdigit() else cpu_cores
            
            # 암호 해독 시작
            unlock_zip(
                zip_path=zip_path,
                num_processes=num_processes,
                pattern=selected_pattern,
                start_with=start_with,
                common_patterns=use_common_patterns
            )
        else:
            # 기본 모드로 실행
            unlock_zip(zip_path=zip_path)
            
    except KeyboardInterrupt:
        print('\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')