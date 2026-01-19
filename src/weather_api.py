"""Weather API module for fetching weather data from MSN Weather API."""

from urllib.request import urlopen
import xmltodict


def get_weather(lat: float, lon: float) -> dict:
    """
    Fetch weather data from MSN Weather API.

    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate

    Returns:
        Dictionary containing weather data with keys:
        - Location: Location name
        - Weather: Weather description
        - Temperature: Temperature in Celsius
        - ImageURL: URL to weather icon
    """
    url = (
        f"http://api.msn.com/weather/LiveTile/front"
        f"?locale=zh-CN&lat={lat}&lon={lon}"
        f"&apiKey=OkWqHMuutahBXs3dBoygqCjgXRt6CV4i5V7SRQURrT"
    )

    response = urlopen(url)
    xml_data = response.read().decode()
    parsed = xmltodict.parse(xml_data)

    # Find TileWide binding (binding[2]) which has the most detailed information
    bindings = parsed["tile"]["visual"]["binding"]
    tilewide_binding = None

    for binding in bindings:
        if isinstance(binding, dict) and binding.get("@template") == "TileWide":
            tilewide_binding = binding
            break

    if tilewide_binding is None:
        # Fallback to first binding with DisplayName
        for binding in bindings:
            if isinstance(binding, dict) and "@DisplayName" in binding:
                tilewide_binding = binding
                break

    if tilewide_binding is None:
        # Last resort: use first binding
        tilewide_binding = bindings[0] if isinstance(bindings, list) else bindings

    location_name = tilewide_binding.get("@DisplayName", "未知位置")

    # Extract subgroups from TileWide binding
    temperature = "--℃"
    weather_desc = "--"
    image_url = ""

    # Get the group with subgroups (there might be multiple groups)
    groups = tilewide_binding.get("group", [])
    if isinstance(groups, dict):
        groups = [groups]

    # Find the group that has the weather data (usually the first one with multiple subgroups)
    target_group = None
    for group in groups:
        if isinstance(group, dict) and "subgroup" in group:
            subgroups = group["subgroup"]
            if isinstance(subgroups, list) and len(subgroups) >= 3:
                target_group = group
                break

    if target_group:
        subgroups = target_group["subgroup"]
        if isinstance(subgroups, dict):
            subgroups = [subgroups]

        # Extract temperature (from subgroups[1] and subgroups[2])
        if len(subgroups) > 1:
            temp_subgroup = subgroups[1]
            if isinstance(temp_subgroup, dict) and "text" in temp_subgroup:
                temp_text = temp_subgroup["text"]
                if isinstance(temp_text, dict) and "#text" in temp_text:
                    temperature = temp_text["#text"]

                    # Add unit from next subgroup if available
                    if len(subgroups) > 2:
                        unit_subgroup = subgroups[2]
                        if isinstance(unit_subgroup, dict) and "text" in unit_subgroup:
                            unit_text = unit_subgroup["text"]
                            if isinstance(unit_text, list):
                                for item in unit_text:
                                    if isinstance(item, str) and "°" in item:
                                        temperature += item
                                        break
                            elif isinstance(unit_text, str) and "°" in unit_text:
                                temperature += unit_text

        # Extract weather description (from last text subgroup)
        for subgroup in subgroups:
            if isinstance(subgroup, dict) and "text" in subgroup:
                text = subgroup["text"]
                if isinstance(text, dict) and "#text" in text:
                    text_value = text["#text"]
                    if text_value and len(text_value) > 1:
                        # Skip temperature values (contain numbers or degree symbol)
                        if (
                            not any(c.isdigit() for c in text_value)
                            and "°" not in text_value
                        ):
                            weather_desc = text_value

        # Extract weather icon (from first image subgroup that looks like a weather icon)
        for subgroup in subgroups:
            if isinstance(subgroup, dict) and "image" in subgroup:
                image = subgroup["image"]
                if isinstance(image, dict) and "@src" in image:
                    src = image["@src"]
                    if src and "weathermapdata/1/static/icons" in src:
                        image_url = src
                        break

        # If no weather icon found, use first image
        if not image_url:
            for subgroup in subgroups:
                if isinstance(subgroup, dict) and "image" in subgroup:
                    image = subgroup["image"]
                    if isinstance(image, dict) and "@src" in image:
                        src = image["@src"]
                        if src and src.startswith("http"):
                            image_url = src
                            break

    return {
        "Location": location_name,
        "Weather": weather_desc,
        "Temperature": temperature,
        "ImageURL": image_url,
    }