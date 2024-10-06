from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import matplotlib.pyplot as plt
import datetime

app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = '57956d6785c0a3e93ac81b7ba38b7723'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    error_message = None

    if request.method == 'POST':
        num_cities = int(request.form.get('num_cities'))
        cities = [request.form.get(f'city_{i+1}') for i in range(num_cities)]

        for city in cities:
            if city:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
                response = requests.get(url).json()

                if response.get("cod") != 200:
                    error_message = response.get("message", f"Error with {city}")
                    break
                else:
                    # Record the timestamp
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    weather_data[city] = {
                        'timestamp': timestamp,
                        'temperature': response["main"]["temp"],
                        'humidity': response["main"]["humidity"],
                        'pressure': response["main"]["pressure"],
                        'wind_speed': response["wind"]["speed"],
                        'description': response["weather"][0]["description"],
                        'icon': response["weather"][0]["icon"]
                    }
            else:
                error_message = "Please enter a city name."
                break

        # Generate graph if weather data exists
        if weather_data and not error_message:
            generate_advanced_graph(weather_data)

    return render_template('weather.html', weather_data=weather_data, error_message=error_message)

def generate_advanced_graph(weather_data):
    cities = list(weather_data.keys())
    temperatures = [data['temperature'] for data in weather_data.values()]
    humidities = [data['humidity'] for data in weather_data.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    bar_width = 0.3

    # Temperature bar chart
    ax1.bar(cities, temperatures, color='tab:red', width=bar_width)
    ax1.set_title('Temperature (°C)')
    ax1.set_ylabel('Temperature (°C)')

    # Humidity bar chart
    ax2.bar(cities, humidities, color='tab:blue', width=bar_width)
    ax2.set_title('Humidity (%)')
    ax2.set_ylabel('Humidity (%)')

    plt.tight_layout()

    # Ensure 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Save the plot as an image
    plt.savefig('static/chart.png')
    plt.close()

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Process the form data if necessary, or just redirect
        return redirect(url_for('about'))  # Redirect to 'aboutus' page
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
