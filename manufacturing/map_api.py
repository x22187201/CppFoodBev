import requests

class MapAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_optimized_route(self, waypoints):
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        origin = waypoints[0]
        destination = waypoints[-1]
        waypoints_str = "|".join(waypoints[1:-1])

        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": f"optimize:true|{waypoints_str}",
            "key": self.api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data["status"] == "OK":
            optimized_route = data["routes"][0]["legs"]
            return optimized_route
        else:
            print("Error fetching route:", data)
            return None
    
    def get_route_distance_duration(self, origin, destination):
        base_url = "https://maps.googleapis.com/maps/api/directions/json"

        params = {
            "origin": origin,
            "destination": destination,
            "key": self.api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data["status"] == "OK":
            route_info = data["routes"][0]["legs"][0]
            distance = route_info["distance"]["text"]
            duration = route_info["duration"]["text"]
            return distance, duration
        else:
            print("Error fetching route information:", data)
            return None, None
        
    def geocode_address(self, address):
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"

        params = {
            "address": address,
            "key": self.api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            print("Error geocoding address:", data)
            return None, None