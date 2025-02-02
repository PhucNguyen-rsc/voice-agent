import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

aii_key = os.getenv('AII_KEY')
openai_key = os.getenv('OPENAI_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_KEY')


class AI_Assistant:
    def __init__(self):
        aai.settings.api_key = aii_key
        self.openai_client = OpenAI(api_key=openai_key)
        self.elevenlabs_api_key = elevenlabs_key

        self.transcriber = None

        # prompt 
        self.full_transcript = [
            {"role":"system", 
             "content":"You are a compassionate, understanding, and non-judgmental therapist who listens deeply. \
                Your goal is to create a safe space where users feel heard, validated, and supported. \
                Always respond with warmth, empathy, and curiosity, encouraging them to share more. \
                Mirror their emotions, acknowledge their struggles, and avoid giving generic advice unless asked. \
                Instead of solving problems, focus on making them feel understood. \
                Keep a natural, conversational tone—like a friend who truly cares."}
        ]

    ## Real-time Transcription with Assembly AI

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate = 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close = self.on_close,
            end_utterance_silence_threshold = 1000  # time AI waits before making a new sentence
        )

        # Connect to your microphone
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        return

    def on_close(self):
        return
    
    def generate_ai_response(self, transcript):
        self.stop_transcription()

        self.full_transcript.append({"role":"user", "content":transcript.text})
        print(f"\n Client : {transcript.text} \r\n")

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)
        self.start_transcription()


    ## Generate audio with Eleven Labs
    def generate_audio(self, text):
        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = "Rachel",
            stream = True
        )

        stream(audio_stream)

# Starting the assistant
greeting = "Thank you for using our Num Num app. My name is Meow Meow. How is it going for you today?"
assistant = AI_Assistant()
print("Here")
assistant.generate_audio(greeting)
assistant.start_transcription()
