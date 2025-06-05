import os #표준
import csv #표준
import wave #표준
import contextlib #표준
import speech_recognition as sr #외부 라이브러리, 음성 인식용 (구글 api)

""" .wav 파일 리스트 반환"""
def list_audio_files(directory): 
    return [f for f in os.listdir(directory) if f.endswith('.wav')]
    #여기서는 _ for _ 를 안 쓰는 게 좋음, 파일 이름을 불러올 때 헷갈리니까

"""파일 경로 인자로 받고, 오디오 파일 길이 초 단위로 반환하기"""
def get_audio_duration(file_path):
    #wave.open() 을 써야 .wav 파일 읽을 수 있음, file.read() 는 안 됨
    with contextlib.closing(wave.open(file_path, 'r')) as audio:
        frames = audio.getnframes() #프레임 수 (총 프레임)
        rate = audio.getframerate() #프레임 속도 (헤르츠)
        duration = frames / float(rate) #음성녹음 파일의 길이(초) 계산
        return duration
    
"""파일 경로 인자로 받고, 오디오 파일 텍스트로 변환하기""" 
def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer() #stt 인식기 객체 생성
    result = [] #[시간, 텍스트]

    with sr.AudioFile(file_path) as source: #source로 오디오 파일 열기
        audio = recognizer.record(source)
        #record(source, duration=n)하면 n초 동안 stt 처리(세분화)
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')  #텍스트 추출
            result.append(('0.0', text))  #0.0로 시작 시간 임의로 설정(단순화하려고)
        except sr.UnknownValueError: #UnknownValueError: 음성 인식 실패
            result.append(('0.0', '음성 인식 실패'))
        except sr.RequestError: #RequestError: API 요청 오류
            result.append(('0.0', 'API 요청 오류'))

    return result

"""파일 이름과 인식된 텍스트를 CSV 파일로 저장하기"""
def save_transcription_to_csv(audio_filename, transcription):
    csv_filename = audio_filename.replace('.wav', '.csv') #.wav만 .csv로 바꿔서 파일 이름 생성
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        #newline=''은 줄바꿈 방지용 (줄이 두 번씩 띄어지는 거 방지)

        writer = csv.writer(file)
        writer.writerow(['시간', '인식된 텍스트']) #각 열의 제목(첫 열)
        for timestamp, text in transcription:
            writer.writerow([timestamp, text])

#보너스- 디렉토리의 모든 CSV 파일에서 키워드 검색하기
def search_keyword_in_csv(directory, keyword):
    matched_files = []

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            with open(os.path.join(directory, filename), encoding='utf-8') as file:
                reader = csv.reader(file)
                      
                for row in reader: #row는 각 행, 리스트 형태 ['시간', '텍스트']
                    row_text = ''.join(row).replace(' ', '').strip()#공백 제거, 문자열로 변환
                    if keyword.replace(' ', '') in row_text:
                        print(f'[{filename}]', ', '.join(row))
                        matched_files.append(filename)
                        break  # 해당 파일에서 하나라도 찾으면 추가 후 다음 파일로 넘어감

    return matched_files             

def main():
    directory = 'D:/projectMoeumZip/grade4/Codyssey/codyssey/records'  # 현재 디렉토리
    audio_files = list_audio_files(directory)

    for audio_file in audio_files:
        full_path = os.path.join(directory, audio_file)
        print(f'{audio_file} 처리 중...')
        #transcription = convert_audio_to_text(audio_file)
        #save_transcription_to_csv(audio_file, transcription)
        transcription = convert_audio_to_text(full_path)  # 전체 경로로 변경
        save_transcription_to_csv(audio_file, transcription)
        print(f'{audio_file} -> CSV 저장 완료')

    # 보너스: 키워드 검색 예시
    keyword = input('검색할 키워드를 입력하세요: ')
    #search_keyword_in_csv(directory, keyword)

    matched_files = search_keyword_in_csv(directory, keyword)
    if matched_files:
            print('\n 키워드를 포함한 파일 목록:')
            for filename in matched_files:
                print(f' - {filename}')
    else:
        print('\n 해당 키워드를 포함한 파일이 없습니다.')

if __name__ == '__main__':
    main()