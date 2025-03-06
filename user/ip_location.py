import requests

def get_ipaddress():
    return requests.get("https://ifconfig.me/ip").text


def get_location(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    location_data = {
        "ip": ip_address,
        "status": response.get("status"),
        "city": response.get("city"),
        "region": response.get("regionName"),
        "country": response.get("country"),
        "long": response.get("long"),
        "lat": response.get("lat"),
    }
    return location_data