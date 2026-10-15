from io import BytesIO
from gtts import gTTS

def text_to_speech(text: str, lang: str = "en") -> BytesIO:
    if not text.strip():
        return None

    fp = BytesIO()
    tts = gTTS(text=text, lang=lang,tld = 'com.au', slow=False,)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp