import requests
import sys
import os

TYPECAST_API_KEY = "__pltNDmWzdnPzEbPZcjZWNaA9PTHLLBMUzokWWzUjqXg"
VOICE_ID = "tc_69fc0cff784968297fb45daa"
API_URL = "https://api.typecast.ai/v1/text-to-speech"


def text_to_speech(text: str, output_path: str = "output.wav") -> str:
    response = requests.post(
        API_URL,
        headers={
            "X-API-KEY": TYPECAST_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "voice_id": VOICE_ID,
            "text": text,
            "model": "ssfm-v30",
            "language": "kor",
            "output": {"audio_format": "wav"},
        },
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "안녕하세요 저는 유준하입니다"
    out = sys.argv[2] if len(sys.argv) > 2 else "output.wav"
    result = text_to_speech(text, out)
    print(f"saved: {os.path.abspath(result)}")
