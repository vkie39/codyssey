import os
import wave
import datetime
import glob
from typing import List, Tuple
import pyaudio
1
class VoiceRecorder:
    """음성 녹음을 담당하는 클래스"""
    
    def __init__(self, sample_rate: int = 44100, chunk_size: int = 1024, 
                 audio_format=pyaudio.paInt16, channels: int = 1):
        """        
        Args:
            sample_rate: 샘플링 주파수 (기본값: 44100 Hz)
            chunk_size: 버퍼 크기 (기본값: 1024)
            audio_format: 오디오 포맷 (기본값: 16bit PCM)
            channels: 채널 수 (기본값: 1 - 모노)
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_format = audio_format
        self.channels = channels
        self.audio = pyaudio.PyAudio()
        self.records_dir = 'records'
        
        # records 폴더 생성
        self._create_records_directory()
    
    def _create_records_directory(self) -> None:
        """records 폴더가 없으면 생성"""
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)
            print(f'{self.records_dir} 폴더가 생성되었습니다.')
    
    def _get_filename(self) -> str:
        """현재 날짜와 시간을 기반으로 파일명 생성"""
        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S.wav')
        return os.path.join(self.records_dir, filename)
    
    def _get_microphone_info(self) -> None:
        """사용 가능한 마이크 정보 출력"""
        print('\n=== 사용 가능한 오디오 디바이스 ===')
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        for i in range(0, num_devices):
            device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                print(f'디바이스 {i}: {device_info.get("name")}')
        print('================================\n')
    
    def record_voice(self, duration: int = None) -> str:
        """
        음성 녹음 수행
        
        Args:
            duration: 녹음 시간 (초). None이면 사용자 입력까지 녹음
            
        Returns:
            저장된 파일의 경로
        """
        filename = self._get_filename()
        
        try:
            # 마이크 정보 출력
            self._get_microphone_info()
            
            # 녹음 스트림 열기
            stream = self.audio.open(format=self.audio_format,
                                   channels=self.channels,
                                   rate=self.sample_rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)
            
            print('녹음을 시작합니다...')
            if duration:
                print(f'{duration}초 동안 녹음합니다.')
            else:
                print('Ctrl + C 키를 누르면 녹음이 종료됩니다.')
            
            frames = []
            
            if duration:
                # 지정된 시간만큼 녹음
                total_frames = int(self.sample_rate / self.chunk_size * duration)
                for _ in range(total_frames):
                    data = stream.read(self.chunk_size)
                    frames.append(data)
            else:
                # 사용자 입력까지 녹음 (별도 스레드 필요하지만 제약사항에 따라 간단히 구현)
                print('녹음 중... (Ctrl+C로 중지)')
                try:
                    while True:
                        data = stream.read(self.chunk_size)
                        frames.append(data)
                except KeyboardInterrupt:
                    print('\n녹음을 중지합니다.')
            
            # 스트림 종료
            stream.stop_stream()
            stream.close()
            
            # WAV 파일로 저장
            self._save_wav_file(filename, frames)
            
            print(f'녹음이 완료되었습니다: {filename}')
            return filename
            
        except Exception as e:
            print(f'녹음 중 오류가 발생했습니다: {e}')
            return ''
    
    def _save_wav_file(self, filename: str, frames: List[bytes]) -> None:
        """녹음된 데이터를 WAV 파일로 저장"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
    
    def list_recordings(self, start_date: str = None, end_date: str = None) -> List[Tuple[str, str]]:
        """
        특정 범위의 날짜에 해당하는 녹음 파일 목록 반환
        
        Args:
            start_date: 시작 날짜 (YYYYMMDD 형식)
            end_date: 종료 날짜 (YYYYMMDD 형식)
            
        Returns:
            (파일명, 파일경로) 튜플의 리스트
        """
        pattern = os.path.join(self.records_dir, '*.wav')
        files = glob.glob(pattern) # 알아보는걸로
        
        if not start_date and not end_date:
            # 모든 파일 반환
            return [(os.path.basename(f), f) for f in sorted(files)]
        
        filtered_files = []
        
        for file_path in files:
            filename = os.path.basename(file_path)
            # 파일명에서 날짜 추출 (YYYYMMDD-HHMMSS.wav 형식)
            try:
                file_date = filename.split('-')[0]
                
                # 날짜 범위 확인
                if start_date and file_date < start_date:
                    continue
                if end_date and file_date > end_date:
                    continue
                    
                filtered_files.append((filename, file_path))
                
            except (IndexError, ValueError):
                # 파일명 형식이 맞지 않으면 무시
                continue
        
        return sorted(filtered_files)
    
    def show_recordings(self, start_date: str = None, end_date: str = None) -> None:
        """녹음 파일 목록을 화면에 출력"""
        recordings = self.list_recordings(start_date, end_date)
        
        if not recordings:
            print('해당 조건에 맞는 녹음 파일이 없습니다.')
            return
        
        print('\n=== 녹음 파일 목록 ===')
        if start_date or end_date:
            print(f'기간: {start_date or "시작"} ~ {end_date or "종료"}')
        
        for filename, file_path in recordings:
            # 파일 크기 정보 추가
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)
            
            # 파일명에서 날짜/시간 파싱하여 읽기 쉽게 표시
            try:
                date_part, time_part = filename.replace('.wav', '').split('-')
                formatted_date = f'{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}'
                formatted_time = f'{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}'
                print(f'{formatted_date} {formatted_time} | {size_mb:.2f}MB | {filename}')
            except (ValueError, IndexError):
                print(f'{filename} | {size_mb:.2f}MB')
        
        print('=====================\n')
    
    def cleanup(self) -> None:
        """리소스 정리"""
        self.audio.terminate()


def main():
    """메인 함수"""
    recorder = VoiceRecorder()
    
    try:
        print('화성 생활 기록 시스템 - JAVIS')
        print('한송희 박사의 음성 기록을 위한 프로그램입니다.\n')
        
        while True:
            print('메뉴를 선택하세요:')
            print('1. 음성 녹음 (시간 지정)')
            print('2. 음성 녹음 (수동 중지)')
            print('3. 모든 녹음 파일 보기')
            print('4. 날짜별 녹음 파일 보기')
            print('5. 종료')
            
            choice = input('\n선택 (1-5): ').strip()
            
            if choice == '1':
                try:
                    duration = int(input('녹음 시간을 초 단위로 입력하세요: '))
                    recorder.record_voice(duration)
                except ValueError:
                    print('올바른 숫자를 입력해주세요.')
                    
            elif choice == '2':
                recorder.record_voice()
                
            elif choice == '3':
                recorder.show_recordings()
                
            elif choice == '4':
                print('날짜 형식: YYYYMMDD (예: 20240315)')
                start_date = input('시작 날짜 (비워두면 처음부터): ').strip()
                end_date = input('종료 날짜 (비워두면 끝까지): ').strip()
                
                # 빈 문자열을 None으로 변환
                start_date = start_date if start_date else None
                end_date = end_date if end_date else None
                
                recorder.show_recordings(start_date, end_date)
                
            elif choice == '5':
                print('프로그램을 종료합니다.')
                break
                
            else:
                print('올바른 번호를 선택해주세요.')
            
            print('-' * 50)
    
    except KeyboardInterrupt:
        print('\n\n프로그램이 중단되었습니다.')
    
    finally:
        recorder.cleanup()


if __name__ == '__main__':
    main()