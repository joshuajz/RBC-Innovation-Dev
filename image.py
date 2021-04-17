import requests


def download_image(url, name):
    """Downloads an image from a url, places it in static/images/database"""

    # Database ID starts @ 1 instead of 0
    if name == 0:
        name = 1
    try:
        # Request to the url
        response = requests.get(url)

        # Create a file and write the image to the file
        f = open(f"static/images/database/{name}.png", "wb")
        f.write(response.content)

        # Close the file
        f.close()

        # Return the location of the file
        return f"static/images/database/{name}.png"
    except:
        return None

    return None