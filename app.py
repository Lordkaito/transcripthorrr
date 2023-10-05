from flask import Flask, request, jsonify
from flask_cors import CORS
import audio_transcriber
import librosa
import audio_transcriber_pro
from werkzeug.exceptions import RequestEntityTooLarge
from decouple import config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app, origins=[config('FRONTEND_URL')])

@app.route('/')

def index():
    return jsonify({'message': 'Hello, World!'})

@app.route("/transcribe", methods=["POST"])
def transcribe():
  audio_file = request.files.get("audio_file")
  audio_data, sr = librosa.load(audio_file)
  result = audio_transcriber.transcribe_audio(audio_data)
  # print(type(audio_data))
  print(result)
  return jsonify({'message': result})

@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(error):
    print(error)
    return jsonify({'error': 'El archivo es demasiado grande. El tamaño máximo permitido es de 16 MB.'}), 400


@app.route("/transcribe_pro", methods=["POST"])
def transcribe_pro():
  print(request)
  audio_file = request.files.get("audio_file")
  audio_data, sr = librosa.load(audio_file)

  audio_thing = audio_file.read()
  print(len(audio_thing))
  result = audio_transcriber_pro.transcribe_audio(audio_data)
  print(result)
  return jsonify({'message': result})


def allowed_file(file):
  return "." in file and file.rsplit(".", 1)[1].lower() in {"wav", "mp3"}


if __name__ == '__main__':
    app.run()