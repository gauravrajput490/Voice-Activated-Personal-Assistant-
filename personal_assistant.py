import speech_recognition as sr
import pyttsx3
import requests
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speaking rate

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I am listening.")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("There seems to be a problem with the speech recognition service.")
        return ""

def check_weather():
    """Fetch and report weather information."""
    API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    speak("Which city's weather do you want to know?")
    city = listen()
    if city:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()
            if response["cod"] == 200:
                weather = response["weather"][0]["description"]
                temp = response["main"]["temp"]
                speak(f"The current weather in {city} is {weather} with a temperature of {temp}°C.")
            else:
                speak(f"Sorry, I could not find weather information for {city}.")
        except Exception as e:
            speak("There was an error fetching the weather information.")
    else:
        speak("You did not specify a city.")

def set_reminder():
    """Set a reminder."""
    speak("What should I remind you about?")
    reminder = listen()
    if reminder:
        speak("When should I remind you? Please say the time in hours and minutes.")
        time = listen()
        if time:
            speak(f"Reminder set for {time}. I will remind you to {reminder}.")
        else:
            speak("I could not understand the time.")
    else:
        speak("I could not understand the reminder.")

def read_news():
    """Fetch and read the latest news headlines."""
    API_KEY = "your_newsapi_org_api_key"  # Replace with your NewsAPI.org API key
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        response = requests.get(url).json()
        if response["status"] == "ok":
            headlines = [article["title"] for article in response["articles"][:5]]
            speak("Here are the top news headlines:")
            for i, headline in enumerate(headlines, start=1):
                speak(f"Headline {i}: {headline}")
        else:
            speak("Sorry, I could not fetch the news at the moment.")
    except Exception as e:
        speak("There was an error fetching the news.")

def main():
    """Main function for the personal assistant."""
    speak("Hello! I am your personal assistant. How can I help you?")
    while True:
        command = listen()
        if "weather" in command:
            check_weather()
        elif "reminder" in command:
            set_reminder()
        elif "news" in command:
            read_news()
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break
        else:
            speak("Sorry, I can't do that yet. Please try another command.")

if __name__ == "__main__":
    main()
