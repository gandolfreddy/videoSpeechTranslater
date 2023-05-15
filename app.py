'''
    A speech translater for video with OpenAI Whisper api, edge-srt-to-speech, and ffmpeg.
'''
from dotenv import load_dotenv
import openai
import os


# get api key from environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_WHISPER_API_KEY')


def get_srt():
    file_path = 'C:\\Users\\loveh\\Desktop\\壓縮後\\_1_遊戲介紹.mp4'
    with open(file_path, "rb") as audio_file:
        transcription = openai.Audio.translate(
            model="whisper-1",
            file=audio_file,
            response_format="srt",
            language="en",
        )
        with open(f"en_out.srt", "w", encoding="utf-8") as f:
            f.write(transcription)


def get_audio():
    pass


def get_muted_video():
    pass


def combine_muted_video_and_audio():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
