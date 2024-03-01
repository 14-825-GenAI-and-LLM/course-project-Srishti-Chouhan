import streamlit as st
import requests
import os
import vertexai
from langchain_google_vertexai import VertexAI
from langchain import PromptTemplate
from langchain.chains import LLMChain


# Set up OpenWeatherMap API key and other required information
OPENWEATHERMAP_API_KEY = "ENTER_YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ENTER_LOCATION_OF_KEY_JSON_FILE" # place the key JSON file in the same folder as your notebook
PROJECT_ID = "ENTER_PROJECT_ID" # use your project id
REGION = "ENTER_REGION"  # enter region
BUCKET_URI = f"ENTER_BUCKET_URI"  # create your own bucket

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)


# Models being used
# llm = VertexAI(model_name="text-bison@001")
llm = VertexAI(model_name="gemini-pro")


# Calling Weather API for current and forecasted weather
# Function to get current weather data from OpenWeatherMap API
def get_current_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "imperial",  # You can change this to "metric" for Celsius
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Function to get weather forecast data from OpenWeatherMap API
def get_weather_forecast(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "imperial",
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


# Function to get and cache current weather information
@st.cache_data(hash_funcs={requests.Response: lambda _: None}, ttl=600)  # Cache for 10 minutes
def get_cached_current_weather(city_name):
    return get_current_weather(city_name)

@st.cache_data(hash_funcs={requests.Response: lambda _: None}, ttl=600)  # Cache for 10 minutes
def get_cached_forecast_weather(city_name):
    return get_weather_forecast(city_name)

# Function to generate weather information using LangChain and cache the results
@st.cache(ttl=600, allow_output_mutation=True)  # Cache for 10 minutes
def generate_cached_weather_information(prompt_template, input_variables):
    llm_result = llm(prompt_template.template.format(**input_variables))
    return llm_result


# Sidebar input for the selected city
selected_city = st.sidebar.text_input("Enter City Name:")
get_weather_button = st.sidebar.button("Get Current Weather")
get_forecast_button = st.sidebar.button("Get Weather Forecast")


# Display weather information when the button is clicked
if get_weather_button:
    
    # Get current weather information from the API (cached)
    weather_data = get_cached_current_weather(selected_city) # weather data retrieved from cache, and if not present in cache fetched from the weather API

    # Create a prompt template for current weather information
    prompt_template_current_weather = PromptTemplate(
        input_variables=['city', 'temperature', 'description', 'humidity', 'wind_speed'],
        template="Provide current weather information for {city}. The temperature is {temperature}°F, the weather is {description}, the humidity is {humidity}%, and the wind speed is {wind_speed} m/s. Give your answer in bullets. Give some precautions of what to do in that weather as well."
    )

    # Error handling
    if weather_data['cod'] == '404':
        st.header(f"City does not exist. Please enter correct city.")
        pass
    
    else: 
        # Prepare input variables for the prompt
        input_variables = {
            'city': selected_city,
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }

        # Generate and cache current weather information using LangChain
        current_weather_result = generate_cached_weather_information(prompt_template_current_weather, input_variables)

        # Display the current weather information
        st.header(f"Current Weather Information for {selected_city}")
        st.write(current_weather_result)


# Display weather forecast information when the button is clicked
if get_forecast_button:
    # Get weather forecast information from the API(cached)
    forecast_data = get_cached_forecast_weather(selected_city)

    # Create a prompt template for weather forecast information
    prompt_template_forecast = PromptTemplate(
        input_variables=['city', 'forecast'],
        template="Provide weather forecast for {city}.{forecast}. Give your answer in bullets. Give some precautions of what to do in that weather as well."
    )

    # Error handling
    if forecast_data['cod'] == '404':
        st.header(f"City does not exist. Please enter correct city.")
        pass

    else:
        # Prepare input variables for the prompt
        input_variables = {
            'city': selected_city,
            'forecast': ', '.join([f"{item['dt_txt']}: {item['main']['temp']}°F" for item in forecast_data['list']])
        }

        # Generate and cache weather forecast information using LangChain
        forecast_result = generate_cached_weather_information(prompt_template_forecast, input_variables)

        # Display the weather forecast information
        st.header(f"Weather Forecast for {selected_city}")
        st.write(forecast_result)
