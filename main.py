import speech_recognition as sr  # type: ignore
import webbrowser  # type: ignore
import pyttsx3  # type: ignore
import musiclibrary  # type: ignore
import requests  # type: ignore
import openai  # Correct import
from gtts import gTTS  # type: ignore
import pygame  # type: ignore
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d093053d72bc4024899804e0e67d"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def speak_new(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load and play the MP3 file
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    # Wait until the music is finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    os.remove("temp.mp3")  # Clean up


def openai_process(command):
    openai.api_key = "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"
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud, give short responses"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return "Sorry, there was a problem with OpenAI."


def process_command(command):
    print(f"Processing command: {command}")
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in command.lower() or "tell me the news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = openai_process(command)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis.......")

    while True:
        with sr.Microphone() as source:
            print("Listening for the wake word 'Jarvis'...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected within the time limit.")
                continue

        print("Recognizing wake word...")
        try:
            wake_word = recognizer.recognize_google(audio).lower()
            print(f"Wake word detected: {wake_word}")

            if wake_word == "jarvis":
                speak("Yes?")
                print("Jarvis is active...")

                with sr.Microphone() as source:
                    print("Listening for the command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    try:
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        process_command(command)
                    except sr.UnknownValueError:
                        print("Could not understand the command.")
                    except sr.RequestError as e:
                        print(f"Could not request results from the recognition service; {e}")

        except sr.UnknownValueError:
            print("Could not understand the wake word.")
        except sr.RequestError as e:
            print(f"Could not request results from the recognition service; {e}")
