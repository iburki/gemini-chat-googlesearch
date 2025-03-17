#works
import os


def get_crash_data():

    import looker_sdk
    from looker_sdk import models40 as models
    import os
    import json
    #sdk = looker_sdk.init40()
    sdk = looker_sdk.init40("looker.ini")

    
    look_id = "9"
    
    try:
        response = sdk.run_look(look_id=look_id, result_format="json")
        print('looker done')
        return json.loads(response)
        
    except Exception as e:
        print(f"Error fetching Looker data: {e}")
        return []


#works


def get_philly_weather_forecast():

   
    import requests
    from datetime import datetime, timedelta
    import json
    
    """
    Get 7-day weather forecast for Philadelphia using NOAA API
    Returns: JSON string of weather data
    """
    lat = "39.9526"
    lon = "-75.1652"
    url = f"https://api.weather.gov/points/{lat},{lon}"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'weatherapp/1.0'})
        response.raise_for_status()
        
        grid_data = response.json()
        forecast_url = grid_data['properties']['forecast']
        
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        weather_data = {
            "location": "Philadelphia, PA",
            "forecast_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "NOAA Weather API",
            "daily_forecasts": []
        }
        
        for period in forecast_data['properties']['periods'][:7]:  # Get 7 days
            daily = {
                "date": period['startTime'][:10],
                "forecast": {
                    "temperature": {
                        "value": period['temperature'],
                        "unit": period['temperatureUnit']
                    },
                    "conditions": period['shortForecast'],
                    "wind": {
                        "speed": period['windSpeed'],
                        "direction": period['windDirection']
                    },
                    "detailed_forecast": period['detailedForecast']
                }
            }
            weather_data["daily_forecasts"].append(daily)
        #print(weather_data)
    
        return json.dumps(weather_data, indent=2)
        
    except Exception as e:
        print(f"Error with NOAA API: {e}")
        return 'll'
        return json.dumps(weather_data, indent=2)

def get_philly_events():
    import requests
    from datetime import datetime, timedelta
    
    """
    Get Ticketmaster events in Philadelphia for next 7 days
    Args:
        api_key (str): enterkey
    Returns:
        list: List of events with basic details
    """
    base_url = "https://app.ticketmaster.com/discovery/v2/events"
    
    # Date range for next 7 days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    params = {
        "apikey": "enterkey",
        "city": "Philadelphia",
        "stateCode": "PA",
        "startDateTime": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "size": 50,
        "sort": "date,asc"
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return []
        
        data = response.json()
        events = []
        
        for event in data.get("_embedded", {}).get("events", []):
            venue = event["_embedded"]["venues"][0]
            event_info = {
                "name": event["name"],
                "date": event["dates"]["start"].get("dateTime", "TBA"),
                "venue": event["_embedded"]["venues"][0]["name"],
                "street": venue.get("address", {}).get("line1", ""),
                "type": event.get("type", ""),
                "genre": event.get("classifications", [{}])[0].get("genre", {}).get("name", "Unknown")
            }
            events.append(event_info)
        #print(events)
        return events
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []
