from dotenv import load_dotenv
import json
import openai
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_WHISPER_API_KEY')

file_path = 'C:\\Users\\loveh\\Desktop\\壓縮後\\_1_遊戲介紹.mp4'
with open(file_path, "rb") as audio_file:
    try:
        # transcription = openai.Audio.transcribe(
        #     model="whisper-1",
        #     file=audio_file,
        #     response_format="srt",
        #     language="zh",
        # )
        # print(transcription)
        # with open("zh_out.srt", "w", encoding="utf-8") as f:
        #     f.write(transcription)
        transcription = openai.Audio.translate(
            model="whisper-1",
            file=audio_file,
            response_format="srt",
            language="en",
        )
        print(transcription)
        with open("en_out.srt", "w", encoding="utf-8") as f:
            f.write(transcription)
        # try:
        #     text = json.loads(transcription)
        #     lines = text.split('\n')
        #     new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
        #     new_text = "1" + "\n" + '\n'.join(new_lines).strip() + '\n'
        #     with open("out.srt", "w") as f:
        #         f.write(new_text)
        # except json.decoder.JSONDecodeError as e:
        #     print(f"JSON 解碼出錯：{e}")
        #     text = transcription
        #     lines = text.split('\n')
        #     new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
        #     new_text = '\n'.join(new_lines).strip() + '\n'
        #     with open("out.srt", "w") as f:
        #         f.write(new_text)
    except openai.error.APIError as e:
        print(f"API 出錯：{e}")
        text = str(e)
        lines = text.split('\n')
        new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
        new_text = "1" + "\n" + '\n'.join(new_lines).strip() + '\n'
        with open('out.srt', 'w') as f:
            f.write(new_text)