"""
idea: script that grabs popular cloud images, allows you to select one, and
guides you through a setup wizard that allows you to configure things like what's
installed on the image, timezone, password, ssh, etc.
"""
import urllib.request
import re

images = {
    'Ubuntu 24.04': 'https://cloud-images.ubuntu.com/minimal/releases/noble/release/',
    'Ubuntu 22.04': 'https://cloud-images.ubuntu.com/minimal/releases/jammy/release/'
}

def img_ext(base_url):
    with urllib.request.urlopen(base_url) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'href="([^"]*amd64\.img)"', html)
        if match:
            return base_url + match.group(1)
        else:
            return None

def setup():
    print('''What image would you like to select?
[1] Ubuntu 24.04
[2] Ubuntu 22.04''')
    img = input('Enter Number: ')
    if img == '1':
        url = img_ext(images["Ubuntu 24.04"])
        urllib.request.urlretrieve(url, 'ubuntu-24.04-cloudimg.img')
    elif img == '2':
        url = img_ext(images["Ubuntu 22.04"])
        urllib.request.urlretrieve(url, 'ubuntu-22.04-cloudimg.img')
    else:
        print('unrecognized input')

setup()