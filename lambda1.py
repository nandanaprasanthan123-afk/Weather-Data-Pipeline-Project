import json
import urllib.request
import boto3
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Weather_table')

def lambda_handler(event, context):
    
    cities = ["Kannur", "Delhi","Varanasi","Kochi"]
    api_key = "API KEY" 
    
    results = []
    
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

                city = data['name']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                
                table.put_item(
                    Item={
                        'city': city,
                        'timestamp': timestamp,
                        'temperature': str(temp),
                        'humidity': str(humidity),
                        'condition': description
                    }
                )
                results.append(f"Success: {city}")
                
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
            results.append(f"Failed: {city}")

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }