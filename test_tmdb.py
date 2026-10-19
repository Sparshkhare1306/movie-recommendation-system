
import requests

url = "https://api.themoviedb.org/3/movie/550"

try:
    response = requests.get(
        url,
        params={"api_key": "436aa9502f2ba8c2208ee5548f2a2ba6"},
        timeout=15
    )
    print("Status:", response.status_code)
    print(response.text[:500])

except requests.RequestException as e:
    print("Request failed:", repr(e))
