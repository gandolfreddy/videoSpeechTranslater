# videoSpeechTranslater
A speech translater for video with OpenAI Whisper api.

## 基本需求
- [x] 1. 取得原影片語音轉文字內容之字幕。
    > 可由 Whisper api 取得語音辨識結果並翻譯。 
- [x] 2. 取得字幕的翻譯（中翻英）。
    > 可由 Whisper api 取得語音辨識結果並翻譯。 
- [x] 3. 取得英文版字幕的配音語音。
    > 透過 `edge-srt-to-speech` 取得可接受配音。
- [x] 4. 結合原影片與英文版配音。
    > 透過 ffmpeg 取得靜音影片。 
    > 透過 ffmpeg 結合靜音影片與音訊。 

## 實驗記錄
### 取得原影片語音轉文字內容之字幕，並取得字幕的翻譯（中翻英）。
* 安裝 `openai` 與 `dotenv` 模組。
```bash
# execute in PowerShell
> pip install openai
> pip install python-dotenv
```
* 設定 OpenAI API Key。
```python
openai.api_key = os.getenv('設定 API KEY 的環境變數')
```
* 取得 `file_path` 影像檔案的字幕（`.srt`）並翻譯成英文，最後輸出至 `srts/en_out.srt`。
```python
file_path = '存放影像檔案的目錄路徑'
with open(file_path, "rb") as audio_file:
    transcription = openai.Audio.translate(
        model="whisper-1",
        file=audio_file,
        response_format="srt",
        language="en",
    )
    with open(f"srts/en_out.srt", "w", encoding="utf-8") as f:
        f.write(transcription)
```
### 取得英文版字幕的配音語音。
* 安裝 `edge-srt-to-speech` 模組。
```bash
# execute in PowerShell
> pip install edge-srt-to-speech
```
* 透過 `edge-srt-to-speech` 取得可接受配音。
```bash
# execute in PowerShell
> edge-srt-to-speech <srt file> <output_audio file> [--voice <voice name>] [--default-speed<=[+-][0-100]%>]
```
### 結合原影片與英文版配音。
* 取得去除聲音版本的影像檔（CLI）
```bash
# execute in PowerShell
> ffmpeg -i <video file> -vcodec copy -an <muted video file>
```
* 結合靜音影像檔與英文版配音（CLI）
```bash
# execute in PowerShell
> ffmpeg -i <muted video file> -i <audio file> -c:v copy -c:a aac <output_video file> -shortest
```

## 實驗結果
- 此流程基本可動作，但結果影片中，有部份音訊因受到字幕檔時間限制，讀文字的速度較快，需要靠後期精修處理。

## 相關工具
- [Clipchamp](https://app.clipchamp.com/)
- [Download FFmpeg](https://ffmpeg.org/download.html#build-windows)

## 參考資源
1. [Speech to text - OpenAI document](https://platform.openai.com/docs/guides/speech-to-text)
2. [[ChatGPT] 如何使用Whisper API 與 ChatGPT API 快速摘要YouTube 影片?](https://youtu.be/uD5_pKbBhgo)
3. [Getting Started With OpenAI Whisper API In Python | Beginner Tutorial](https://youtu.be/BkcSJol59Rg)
4. [AI上廣東話字幕免費（接近） | Cantonese subtitle generator | Python 教學 廣東話 | Whisper API](https://youtu.be/04bgLwKjCmY)
5. [appfromape/open_ai_whisper_1_transcribe](https://github.com/appfromape/open_ai_whisper_1_transcribe)
6. [openai/openai-cookbook](https://github.com/openai/openai-cookbook)
7. [( Day 18 ) 取出影片聲音、影片加入聲音](https://ithelp.ithome.com.tw/articles/10292945?sc=rss.qu)
