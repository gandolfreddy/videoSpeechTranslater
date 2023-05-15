'''
    A speech translater for video with OpenAI Whisper api, edge-srt-to-speech, and ffmpeg.
'''
import argparse
from dotenv import load_dotenv
import openai
import os
import time


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


def combine_muted_video_and_audio(muted_video_path, audio_path, dst_path):
    '''
        Combine muted video and audio.
        CLI example:
            ffmpeg -i a_mute.mp4 -i a.mp3 -c:v copy -c:a aac a_en.mp4 -shortest
    '''
    cmd = f"ffmpeg -i {muted_video_path} -i {audio_path} -c:v copy -c:a aac {dst_path} -shortest"
    os.system(cmd)


def get_parser():
    '''
        Get parser for command line arguments.
    '''
    parser = argparse.ArgumentParser(
        prog='Video Speech Translater, VST',
        description='A speech translater for video with OpenAI Whisper api.',)
    parser.add_argument(
        "-s", "--src-path", 
        help="Path of source video, e.g. a.mp4")
    parser.add_argument(
        "-sp", "--srt-path", 
        help="Directory path of srt file, e.g. srt/. Default: $home/Desktop/material_dir_[yyyymmdd].")
    parser.add_argument(
        "-ap", "--audio-path", 
        help="Directory path of audio file, e.g. audio/. Default: $home/Desktop/material_dir_[yyyymmdd].")
    parser.add_argument(
        "-mvp", '--muted-video-path', 
        help="Directory path of muted video file, e.g. muted_video/. Default: $home/Desktop/material_dir_[yyyymmdd].")
    parser.add_argument(
        "-dp", "--dst-path", 
        help="Directory path of destination video file, e.g. dst/. Default: $home/Desktop/material_dir_[yyyymmdd].")
    return parser


def set_material_dir(args):
    '''
        Set directory for materials.
    '''
    # if any of the args isn't given, 
    # create a $home/Desktop/material_dir_[yyyymmdd] directory
    if not all([args.srt_path, args.audio_path, 
                args.muted_video_path, args.dst_path]):
        temp_dir = os.path.join(
            os.path.expanduser("~"), 
            f"Desktop\\material_dir_{time.strftime('%Y%m%d')}"
        )
        # check if the directory doesn't exists
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

    # if --srt-path isn't given, 
    # create srt directory and set --srt-path
    if not args.srt_path:
        args.srt_path = os.path.join(temp_dir, "srt")
        if not os.path.isdir(args.srt_path):
            os.mkdir(args.srt_path)
    # if --audio-path isn't given, 
    # create audio directory and set --audio-path
    if not args.audio_path:
        args.audio_path = os.path.join(temp_dir, "audio")
        if not os.path.isdir(args.audio_path):
            os.mkdir(args.audio_path)
    # if --muted-video-path isn't given,
    # create muted_video directory and set --muted-video-path
    if not args.muted_video_path:
        args.muted_video_path = os.path.join(temp_dir, "muted_video")
        if not os.path.isdir(args.muted_video_path):
            os.mkdir(args.muted_video_path)
    # if --dst-path isn't given,
    # create dst directory and set --dst-path
    if not args.dst_path:
        args.dst_path = os.path.join(temp_dir, "dst")
        if not os.path.isdir(args.dst_path):
            os.mkdir(args.dst_path)


def get_file_name(src_path):
    '''
        Get file name from src_path.
    '''
    return os.path.splitext(os.path.basename(src_path))[0]


def main():
    # get api key from environment variables
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_WHISPER_API_KEY")
    
    # get user input from command line
    args = get_parser().parse_args()

    # check if --src-path is given
    if not args.src_path:
        print("Please give a certain src_path (´▽`ʃ♡ƪ)")
        return
    
    # set directory for materials
    set_material_dir(args)

    # get file name from src_path
    file_name = get_file_name(args.src_path)

    # start main process
    print("Start to get srt file...")
    get_srt(
        src_path=args.src_path,
        dst_path=f"{args.srt_path}\\{file_name}.srt",
        response_format="srt", 
        language="en",
    )
    print("Start to get audio...")
    get_audio(
        srt_path=f"{args.srt_path}\\{file_name}.srt",
        audio_path=f"{args.audio_path}\\{file_name}.mp3",
        voice="en-US-JennyNeural", 
        default_speed="-25%",
    )
    print("Start to get muted video...")
    get_muted_video(
        src_path=args.src_path,
        dst_path=f"{args.muted_video_path}\\{file_name}_muted.mp4",
    )
    print("Start to combine muted video and audio...")
    combine_muted_video_and_audio(
        muted_video_path=f"{args.muted_video_path}\\{file_name}_muted.mp4",
        audio_path=f"{args.audio_path}\\{file_name}.mp3",
        dst_path=f"{args.dst_path}\\{file_name}_en.mp4",
    )
    print("Done !!")


if __name__ == '__main__':
    # execute main function
    main()
