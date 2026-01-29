import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import pyaudio

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "f174daf8c4fda536bc6bc53476d229b2"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        parts = c.split(" ", 1)
        if len(parts) < 2:
            speak("Please say the song name")
            return

        song = parts[1]
        link = musicLibrary.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in c:
        speak("Fetching latest Google news")

        url = f"https://gnews.io/api/v4/search?q=Google&lang=en&max=5&apikey={newsapi}"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            if not articles:
                speak("No news found")
                return

            for i, article in enumerate(articles[:3], start=1):
                speak(f"News {i}")
                speak(article["title"])
        else:
            speak("Failed to fetch news")
    elif "quit" in c or "stop" in c:
        speak("Goodbye")
        exit()
        
    else:
        speak("Sorry, I did not understand that")

if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Hello, how can I help you?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Jarvis listening...")
                    audio = recognizer.listen(source, phrase_time_limit=6)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("Could not understand")
        except Exception as e:
            print("Error:", e)
