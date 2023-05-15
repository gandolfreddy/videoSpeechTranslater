from dotenv import load_dotenv
import openai
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_WHISPER_API_KEY')

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