import requests
import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# OpenWeather API key, city, and state
API_KEY = "58cef9659cdf58d5e41f169d59e058dd"
CITY = "New York"
STATE = "NY"  # Add the state code here

def get_weather_data():
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{CITY},{STATE},US",  # Include state and country code
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    return json.loads(response.text)

def create_pdf(data):
    doc = SimpleDocTemplate("weather_forecast.pdf", pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph(f"5-Day Weather Forecast for {CITY}, {STATE}", styles['Title'])  # Include state in title
    elements.append(title)
    
    table_data = [['Date', 'Time', 'Temperature (°C)', 'Description']]
    for item in data['list'][:40:8]:  # Get data for every 24 hours (3-hour steps)
        date = datetime.fromtimestamp(item['dt'])
        table_data.append([
            date.strftime("%Y-%m-%d"),
            date.strftime("%H:%M"),
            f"{item['main']['temp']:.1f}",
            item['weather'][0]['description']
        ])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    doc.build(elements)

def main():
    weather_data = get_weather_data()
    create_pdf(weather_data)
    print(f"Weather forecast PDF for {CITY}, {STATE} has been generated.")

if __name__ == "__main__":
    main()