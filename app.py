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


def get_audio(srt_path, audio_path, **kwargs):
    '''
        Get audio from srt file.
        CLI example:
            edge-srt-to-speech a.srt a.mp3 --voice=en-US-JennyNeural --default-speed=-25%
    '''
    cmd = f"edge-srt-to-speech {srt_path} {audio_path}"
    for key, value in kwargs.items():
        cmd += f" --{key.replace('_', '-')}={value}"
    os.system(cmd)


def get_muted_video(src_path, dst_path):
    '''
        Get muted video from original video.
        CLI example:
            ffmpeg -i a.mp4 -vcodec copy -an a_muted.mp4
    '''
    cmd = f"ffmpeg -i {src_path} -vcodec copy -an {dst_path}"
    os.system(cmd)


def combine_muted_video_and_audio():
    '''
        Combine muted video and audio.
    '''
    pass


def main():
    # get_srt(
    #     src_path="C:\\Users\\loveh\\Desktop\\test_project\\src_videos\\_1_遊戲介紹.mp4", 
    #     dst_path="C:\\Users\\loveh\\Desktop\\test_project\\srts\\_1_遊戲介紹.srt",
    #     response_format="srt", 
    #     language="en",
    # )
    # get_audio(
    #     srt_path="C:\\Users\\loveh\\Desktop\\test_project\\srts\\_1_遊戲介紹.srt", 
    #     audio_path="C:\\Users\\loveh\\Desktop\\test_project\\audios\\_1_遊戲介紹.mp3", 
    #     voice="en-US-JennyNeural", 
    #     default_speed="-25%",
    # )
    get_muted_video(
        src_path="C:\\Users\\loveh\\Desktop\\test_project\\src_videos\\_1_遊戲介紹.mp4", 
        dst_path="C:\\Users\\loveh\\Desktop\\test_project\\muted_videos\\_1_遊戲介紹_muted.mp4",
    )


if __name__ == '__main__':
    main()
