from flask import Flask, request, jsonify, render_template
import spacy
import requests
import requests

app = Flask(__name__)

# Load the English language model in spaCy
nlp = spacy.load('en_core_web_sm')

# OpenWeatherMap API key (replace 'YOUR_API_KEY' with your actual API key)
API_KEY = '674df3e29521a6d9a90c4edd4a9540ff'
NEWS_API_KEY = 'dcfd4a35c0cc40ed9696e668bdb56e51'

# Define functions to handle different intents

def news_intent(message):
    if 'news' in message.lower():
        # Make a request to the NewsAPI for top headlines
        response = requests.get(f'http://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data['articles'][:5]  # Get the top 5 articles
            news_headlines = '\n'.join([article['title'] for article in articles])
            return f"Here are the latest headlines:\n{news_headlines}"
        else:
            return "Sorry, I couldn't retrieve the latest news. Please try again later."
    
    # Check for specific news categories
    if 'technology' in message.lower():
        # Make a request to the NewsAPI for technology news
        response = requests.get(f'http://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            tech_news_data = response.json()
            tech_articles = tech_news_data['articles'][:5]  # Get the top 5 technology articles
            tech_headlines = '\n'.join([article['title'] for article in tech_articles])
            return f"Here are the latest technology headlines:\n{tech_headlines}"
        else:
            return "Sorry, I couldn't retrieve the latest technology news. Please try again later."
    
    if 'sports' in message.lower():
        # Make a request to the NewsAPI for sports news
        response = requests.get(f'http://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            sports_news_data = response.json()
            sports_articles = sports_news_data['articles'][:5]  # Get the top 5 sports articles
            sports_headlines = '\n'.join([article['title'] for article in sports_articles])
            return f"Here are the latest sports headlines:\n{sports_headlines}"
        else:
            return "Sorry, I couldn't retrieve the latest sports news. Please try again later."
    
    if 'business' in message.lower():
        # Make a request to the NewsAPI for business news
        response = requests.get(f'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            business_news_data = response.json()
            business_articles = business_news_data['articles'][:5]  # Get the top 5 business articles
            business_headlines = '\n'.join([article['title'] for article in business_articles])
            return f"Here are the latest business headlines:\n{business_headlines}"
        else:
            return "Sorry, I couldn't retrieve the latest business news. Please try again later."
    
    if 'entertainment' in message.lower():
        # Make a request to the NewsAPI for entertainment news
        response = requests.get(f'http://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey={NEWS_API_KEY}')
        if response.status_code == 200:
            entertainment_news_data = response.json()
            entertainment_articles = entertainment_news_data['articles'][:5]  # Get the top 5 entertainment articles
            entertainment_headlines = '\n'.join([article['title'] for article in entertainment_articles])
            return f"Here are the latest entertainment headlines:\n{entertainment_headlines}"
        else:
            return "Sorry, I couldn't retrieve the latest entertainment news. Please try again later."
    
    return None  # Return None if no news-related intent is detected

def greet_intent(message):
    # Recognize greetings
    greetings = ['hello', 'hi', 'hey', 'howdy']
    if any(token.text.lower() in greetings for token in nlp(message)):
        return "Hello! How can I assist you today?"
    return None  # Return None if no greeting is detected

def farewell_intent(message):
    farewell_keywords = ['bye', 'goodbye', 'see you later', 'take care']
    if any(keyword in message.lower() for keyword in farewell_keywords):
        return "Goodbye! Have a great day!"
    return None

def weather_intent(message):
    # Normalize and tokenize the message using spaCy
    doc = nlp(message.lower())
    
    # Check for specific weather-related keywords and extract location if mentioned
    if any(token.text in ['weather', 'forecast', 'temperature'] for token in doc):
        # Initialize location variable
        location = None
        
        # Extract location using spaCy's named entity recognition (NER)
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # GPE (Geo-Political Entity) label in spaCy for locations
                location = ent.text
                break
        
        if location:
            # Call weather API to get current weather data for the extracted location
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}')
            if response.status_code == 200:
                weather_data = response.json()
                if 'weather' in weather_data and 'main' in weather_data:
                    weather_description = weather_data['weather'][0]['description']
                    temperature = weather_data['main']['temp']
                    # Convert temperature from Kelvin to Celsius
                    temperature_celsius = temperature - 273.15
                    return f"The weather in {location.title()} today: {weather_description}. Temperature: {temperature_celsius:.2f}°C"
                else:
                    return f"Sorry, I couldn't retrieve weather information for {location}."
            else:
                return f"Sorry, I couldn't retrieve weather information for {location}. Please try another location."
        else:
            return "Please specify a location for weather information (e.g., 'What's the weather in New York?')."
    
    return None  # Return None if no weather-related intent is detected

def calculator_intent(message):
    # Check if the message explicitly requests a calculation
    if 'calculate' in message.lower():
        # Extract the arithmetic expression to be evaluated
        expression = message.lower().replace('calculate', '').strip()
        
        try:
            result = eval(expression)  # Evaluate the arithmetic expression
            return f"The result of '{expression}' is: {result}"
        except Exception as e:
            return "Sorry, I couldn't perform that calculation."
    
    return None  # Return None if no calculation request is detected

def process_message(message):
    # Check for different intents including translation
    intents = [
        greet_intent, farewell_intent, weather_intent,
        calculator_intent, news_intent
    ]
    
    # Iterate over intents and execute corresponding function
    for intent_func in intents:
        response = intent_func(message)
        if response:
            return response  # Return the first non-None response
    
    return "I'm sorry, I didn't understand that."

# Define a route for the root URL to render the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle chatbot interactions
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    response = process_message(user_message)
    return jsonify({'message': response})

if __name__ == "__main__":
    app.run(debug=True)
