import whisper
import os
import tempfile

print("Loading Whisper model (first time downloads ~150MB)...")
whisper_model = whisper.load_model("base")
print("Whisper ready.")

ALLOWED = {"mp3", "wav", "m4a", "webm", "ogg", "mp4"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def transcribe_audio(audio_file):
    try:
        ext = "." + audio_file.filename.rsplit(".", 1)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        result = whisper_model.transcribe(tmp_path, language="en")
        transcript = result["text"].strip()
        os.unlink(tmp_path)

        return {"success": True, "transcript": transcript}
    except Exception as e:
        return {"success": False, "error": str(e)}