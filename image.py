import requests


def download_image(url, name):
    # Database ID starts @ 1 instead of 0
    if name == 0:
        name = 1
    try:
        response = requests.get(url)
        f = open(f"static/images/database/{name}.png", "wb")
        f.write(response.content)
        f.close()
        return f"static/images/database/{name}.png"
    except:
        return False

    return False