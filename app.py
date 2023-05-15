'''
    A speech translater for video with OpenAI Whisper api, edge-srt-to-speech, and ffmpeg.
'''
from dotenv import load_dotenv
import openai
import os


# get api key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_WHISPER_API_KEY")


def get_srt(src_path, dst_path, response_format="srt", language="en"):
    '''
        Get srt file from video.
    '''
    with open(src_path, "rb") as audio_file:
        transcription = openai.Audio.translate(
            model="whisper-1",
            file=audio_file,
            response_format=response_format,
            language=language,
        )
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(transcription)
    return transcription


def get_audio():
    '''
        Get audio from srt file.
    '''
    pass


def get_muted_video():
    '''
        Get muted video from original video.
    '''
    pass


def combine_muted_video_and_audio():
    '''
        Combine muted video and audio.
    '''
    pass


def main():
    transcription = get_srt(
        src_path='C:\\Users\\loveh\\Desktop\\test_project\\src_videos\\_1_遊戲介紹.mp4', 
        dst_path='C:\\Users\\loveh\\Desktop\\test_project\\srts\\_1_遊戲介紹.srt',
        response_format='srt', language='en'
    )


if __name__ == '__main__':
    main()
