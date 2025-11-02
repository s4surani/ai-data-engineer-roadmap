# api_client.py - REST API Client

import requests
import json
from datetime import datetime
import time


class APIClient:
    """Generic REST API client with error handling and retry logic"""
    
    def __init__(self, base_url, timeout=30, max_retries=3):
        """
        Initialize API client
        
        Args:
            base_url (str): Base URL for API
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
    
    def _make_request(self, method, endpoint, **kwargs):
        """
        Make HTTP request with retry logic
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            dict: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"🌐 {method} {url}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Raise exception for bad status codes
                response.raise_for_status()
                
                print(f"✅ Success (Status: {response.status_code})")
                
                # Try to parse JSON
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {'text': response.text}
                
            except requests.exceptions.Timeout:
                print(f"⚠️  Timeout on attempt {attempt}/{self.max_retries}")
                if attempt == self.max_retries:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.HTTPError as e:
                print(f"❌ HTTP Error: {e}")
                raise
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Request Error: {e}")
                if attempt == self.max_retries:
                    raise
                time.sleep(2 ** attempt)
    
    def get(self, endpoint, params=None, headers=None):
        """Make GET request"""
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def post(self, endpoint, data=None, json_data=None, headers=None):
        """Make POST request"""
        return self._make_request('POST', endpoint, data=data, json=json_data, headers=headers)
    
    def put(self, endpoint, data=None, json_data=None, headers=None):
        """Make PUT request"""
        return self._make_request('PUT', endpoint, data=data, json=json_data, headers=headers)
    
    def delete(self, endpoint, headers=None):
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint, headers=headers)


def fetch_crypto_prices():
    """
    Fetch cryptocurrency prices from CoinGecko API
    (Free, no API key required)
    """
    print("\n" + "="*70)
    print("💰 FETCHING CRYPTOCURRENCY PRICES")
    print("="*70 + "\n")
    
    client = APIClient('https://api.coingecko.com/api/v3')
    
    try:
        # Get Bitcoin, Ethereum, and Cardano prices
        response = client.get(
            'simple/price',
            params={
                'ids': 'bitcoin,ethereum,cardano',
                'vs_currencies': 'usd,inr',
                'include_24hr_change': 'true'
            }
        )
        
        print("\n📊 Current Prices:\n")
        
        for crypto, data in response.items():
            print(f"{crypto.upper()}:")
            print(f"  USD: ${data['usd']:,.2f}")
            print(f"  INR: ₹{data['inr']:,.2f}")
            
            change = data.get('usd_24h_change', 0)
            change_symbol = "📈" if change > 0 else "📉"
            print(f"  24h Change: {change_symbol} {change:.2f}%")
            print()
        
        return response
        
    except Exception as e:
        print(f"❌ Error fetching crypto prices: {e}")
        return None


def fetch_random_users(count=5):
    """
    Fetch random user data from RandomUser API
    (Free, no API key required)
    """
    print("\n" + "="*70)
    print("👥 FETCHING RANDOM USER DATA")
    print("="*70 + "\n")
    
    client = APIClient('https://randomuser.me/api')
    
    try:
        response = client.get('', params={'results': count})
        
        users = response.get('results', [])
        
        print(f"📋 Generated {len(users)} users:\n")
        
        for i, user in enumerate(users, 1):
            name = f"{user['name']['first']} {user['name']['last']}"
            email = user['email']
            city = user['location']['city']
            country = user['location']['country']
            
            print(f"{i}. {name}")
            print(f"   Email: {email}")
            print(f"   Location: {city}, {country}")
            print()
        
        return users
        
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return None


def fetch_weather_data(city='Pune'):
    """
    Fetch weather data from Open-Meteo API
    (Free, no API key required)
    """
    print("\n" + "="*70)
    print(f"🌤️  FETCHING WEATHER DATA FOR {city.upper()}")
    print("="*70 + "\n")
    
    # Coordinates for Pune
    coords = {
        'Pune': {'lat': 18.5204, 'lon': 73.8567},
        'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946}
    }
    
    if city not in coords:
        print(f"❌ City '{city}' not found")
        return None
    
    client = APIClient('https://api.open-meteo.com/v1')
    
    try:
        response = client.get(
            'forecast',
            params={
                'latitude': coords[city]['lat'],
                'longitude': coords[city]['lon'],
                'current_weather': 'true',
                'timezone': 'Asia/Kolkata'
            }
        )
        
        current = response.get('current_weather', {})
        
        print(f"Current Weather in {city}:")
        print(f"  Temperature: {current.get('temperature')}°C")
        print(f"  Wind Speed: {current.get('windspeed')} km/h")
        print(f"  Time: {current.get('time')}")
        print()
        
        return response
        
    except Exception as e:
        print(f"❌ Error fetching weather: {e}")
        return None


def save_api_response(data, filename):
    """Save API response to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved response to: {filename}\n")
    except Exception as e:
        print(f"❌ Error saving response: {e}")


if __name__ == "__main__":
    print("="*70)
    print("🌐 REST API CLIENT DEMONSTRATION")
    print("="*70)
    
    # Fetch crypto prices
    crypto_data = fetch_crypto_prices()
    if crypto_data:
        save_api_response(crypto_data, 'output/crypto_prices.json')
    
    # Fetch random users
    users_data = fetch_random_users(count=3)
    if users_data:
        save_api_response(users_data, 'output/random_users.json')
    
    # Fetch weather
    weather_data = fetch_weather_data('Pune')
    if weather_data:
        save_api_response(weather_data, 'output/weather_pune.json')
    
    print("="*70)
    print("✅ API CLIENT DEMONSTRATION COMPLETE")
    print("="*70)