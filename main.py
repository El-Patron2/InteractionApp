import os
from flask import Flask, render_template, request, jsonify, send_file
from google.cloud import speech, texttospeech
from google.oauth2 import service_account
import io
import logging
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up credentials
credentials = service_account.Credentials.from_service_account_file(
    "voiceinteractionapp-436602-64413c96f909.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    app.logger.info("Transcribe endpoint hit")
    if 'audio' not in request.files:
        app.logger.error("No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        app.logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    audio_content = audio_file.read()

    client = speech.SpeechClient(credentials=credentials)
    audio = speech.RecognitionAudio(content=audio_content)
    
    file_extension = os.path.splitext(audio_file.filename)[1].lower()
    encoding = speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    if file_extension == '.wav':
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    elif file_extension in ['.mp3', '.mpeg']:
        encoding = speech.RecognitionConfig.AudioEncoding.MP3
    elif file_extension == '.ogg':
        encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    try:
        app.logger.info("Sending request to Google Speech-to-Text API")
        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            app.logger.warning("No speech detected in the audio")
            return jsonify({'error': 'No speech detected'}), 400
        
        transcription = ' '.join([result.alternatives[0].transcript for result in response.results])
        app.logger.info(f"Transcription successful: {transcription}")
        return jsonify({'transcription': transcription})
    except Exception as e:
        app.logger.error(f"Transcription error: {str(e)}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/generate-speech', methods=['POST'])
def generate_speech():
    app.logger.info("Generate speech endpoint hit")
    text = request.json.get('text')
    
    if not text:
        app.logger.error("No text provided for speech generation")
        return jsonify({'error': 'No text provided'}), 400

    client = texttospeech.TextToSpeechClient(credentials=credentials)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        app.logger.info("Sending request to Google Text-to-Speech API")
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        app.logger.info("Speech generated successfully")
        return send_file(
            io.BytesIO(response.audio_content),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="speech.mp3"
        )
    except Exception as e:
        app.logger.error(f"Speech generation error: {str(e)}")
        return jsonify({'error': f'Speech generation failed: {str(e)}'}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)