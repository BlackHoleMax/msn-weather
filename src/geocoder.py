"""Geocoding module for converting location names to coordinates using Bing Maps crawler."""

import requests
import time
import random
import re
from typing import Optional, Tuple


class BingMapsCrawler:
    """Bing Maps crawler for converting location names to coordinates."""

    def __init__(self):
        """Initialize the Bing Maps crawler."""
        self.base_url = "https://cn.bing.com/api/v6/Places/AutoSuggest"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://cn.bing.com/maps",
            "Origin": "https://cn.bing.com",
        }

    def geocode(self, location_name: str) -> Optional[Tuple[float, float]]:
        """
        Convert a location name to latitude and longitude coordinates using Bing Maps search.

        Args:
            location_name: Name of the location (e.g., "北京", "上海市", "广州天河区")

        Returns:
            Tuple of (latitude, longitude) if found, None otherwise
        """
        try:
            # Prepare request parameters based on the example
            params = {
                "q": location_name,
                "appid": "D41D8CD98F00B204E9800998ECF8427E1FBE79C2",
                "mv8cid": "bfdcea26-4b1b-561b-138a-8cf7d4792a39",
                "mv8ig": "ED44C2E34DD148ED8C9F73E0EBF487C3",
                "localMapView": "39.91497830161123,116.39130592346055,39.900641901315225,116.40388011932174",
                "localcircularview": "31.96147918701172,119.5755844116211,100",
                "count": "5",
                "structuredaddress": "true",
                "types": "",
                "histcnt": "",
                "favcnt": "",
                "ensearch": "0",
                "ptypes": "favorite",
                "clientid": "1FF27D562EDC64B025F96BB32F64654C",
                "abbrtext": "1",
            }

            # Make the request
            response = requests.get(
                self.base_url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()

            # Parse the response
            data = response.json()

            # Check if we have results
            if data.get("value") and len(data["value"]) > 0:
                # Get the first result
                first_result = data["value"][0]
                if "geo" in first_result:
                    geo = first_result["geo"]
                    if "latitude" in geo and "longitude" in geo:
                        lat = geo["latitude"]
                        lon = geo["longitude"]
                        return lat, lon

            # If no results in the first API, try alternative approach
            return self._try_alternative_search(location_name)

        except Exception as e:
            print(f"Bing Maps爬虫错误 '{location_name}': {e}")
            return None

    def _try_alternative_search(
        self, location_name: str
    ) -> Optional[Tuple[float, float]]:
        """Try alternative search method if the first one fails."""
        try:
            # Try a simpler search approach
            search_url = "https://cn.bing.com/maps"
            params = {"q": location_name, "FORM": "HDRSC4"}

            response = requests.get(
                search_url, params=params, headers=self.headers, timeout=10
            )

            # Try to extract coordinates from the page
            content = response.text

            # Look for latitude/longitude patterns in the HTML
            # Pattern 1: Look for centerLatitude in localStorage patterns
            lat_pattern = r'centerLatitude["\']?\s*[:=]\s*["\']?([-+]?\d*\.?\d+)'
            lon_pattern = r'centerLongitude["\']?\s*[:=]\s*["\']?([-+]?\d*\.?\d+)'

            lat_match = re.search(lat_pattern, content)
            lon_match = re.search(lon_pattern, content)

            if lat_match and lon_match:
                lat = float(lat_match.group(1))
                lon = float(lon_match.group(1))
                return lat, lon

            # Pattern 2: Look for coordinates in URL parameters
            coord_pattern = r"([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+)"
            coord_matches = re.findall(coord_pattern, content)

            if coord_matches:
                # Take the first coordinate pair that looks like lat/lon
                for lat_str, lon_str in coord_matches:
                    try:
                        lat = float(lat_str)
                        lon = float(lon_str)
                        # Validate reasonable latitude/longitude ranges
                        if -90 <= lat <= 90 and -180 <= lon <= 180:
                            return lat, lon
                    except ValueError:
                        continue

            return None

        except Exception as e:
            print(f"备用搜索方法错误 '{location_name}': {e}")
            return None


class Geocoder:
    """Main geocoder class that uses Bing Maps crawler."""

    def __init__(self):
        """Initialize the geocoder with Bing Maps crawler."""
        self.crawler = BingMapsCrawler()

    def get_coordinates(self, location_name: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a location name.

        Args:
            location_name: Name of the location

        Returns:
            Tuple of (latitude, longitude) if found, None otherwise
        """
        # Add a small delay to be polite to the server
        time.sleep(random.uniform(0.5, 1.5))

        # Try Bing Maps crawler
        coordinates = self.crawler.geocode(location_name)

        if coordinates is None:
            print(f"无法找到地区 '{location_name}' 的坐标")

        return coordinates


# Global geocoder instance
_geocoder = None


def get_geocoder() -> Geocoder:
    """Get or create the global geocoder instance."""
    global _geocoder
    if _geocoder is None:
        _geocoder = Geocoder()
    return _geocoder


def geocode_location(location_name: str) -> Optional[Tuple[float, float]]:
    """
    Convenience function to geocode a location name.

    Args:
        location_name: Name of the location

    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    geocoder = get_geocoder()
    return geocoder.get_coordinates(location_name)


if __name__ == "__main__":
    # Test the geocoder
    test_locations = ["北京", "上海", "广州", "深圳市", "杭州西湖"]

    for location in test_locations:
        print(f"搜索: {location}")
        result = geocode_location(location)
        if result:
            print(f"  结果: 纬度={result[0]:.6f}, 经度={result[1]:.6f}")
        else:
            print("  未找到")
        print()
