import os  # 표준
import csv  # 표준
import wave  # 표준
import contextlib  # 표준
import speech_recognition as sr  # 외부 라이브러리, 음성 인식용 (구글 API)

directory = 'C:/Users/109-2/Desktop/s/codyssey/records'

""" .wav 파일 리스트 반환 """
def list_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.wav')]

""" 오디오 파일 길이(초)를 반환 """
def get_audio_duration(file_path):
    with contextlib.closing(wave.open(file_path, 'r')) as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        duration = frames / float(rate)
        return duration

""" 오디오 파일을 텍스트로 변환 (시간 포함) """
def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer()
    result = []

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
            duration = get_audio_duration(file_path)
            result.append((f'0.0 ~ {duration:.2f}', text))
        except sr.UnknownValueError:
            result.append(('0.0', '음성 인식 실패'))
        except sr.RequestError:
            result.append(('0.0', 'API 요청 오류'))

    return result

""" 텍스트 결과를 CSV로 저장 """
def save_transcription_to_csv(audio_filename, transcription):
    csv_filename = audio_filename.replace('.wav', '.csv')
    csv_filepath = os.path.join(directory, csv_filename)
    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['시간', '인식된 텍스트'])
        for timestamp, text in transcription:
            writer.writerow([timestamp, text])

""" CSV 파일에서 키워드 검색 """
def search_keyword_in_csv(directory, keyword):
    matched_files = []
    keyword_cleaned = keyword.replace(' ', '').lower()

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            with open(os.path.join(directory, filename), encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # 헤더 건너뛰기

                for row in reader:
                    if not row:
                        continue
                    row_text = ''.join(row).replace(' ', '').strip().lower()
                    if keyword_cleaned in row_text:
                        print(f'[{filename}]', ', '.join(row))
                        matched_files.append(filename)
                        break

    return matched_files

""" 메인 실행 함수 """
def main():
    audio_files = list_audio_files(directory)

    for audio_file in audio_files:
        full_path = os.path.join(directory, audio_file)
        print(f'{audio_file} 처리 중...')
        transcription = convert_audio_to_text(full_path)
        save_transcription_to_csv(audio_file, transcription)
        print(f'{audio_file} -> CSV 저장 완료')

    keyword = input('검색할 키워드를 입력하세요: ')
    matched_files = search_keyword_in_csv(directory, keyword)
    if matched_files:
        print('\n 키워드를 포함한 파일 목록:')
        for filename in matched_files:
            print(f' - {filename}')
    else:
        print('\n 해당 키워드를 포함한 파일이 없습니다.')

if __name__ == '__main__':
    main()
