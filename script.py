"""
idea: script that grabs popular cloud images, allows you to select one, and
guides you through a setup wizard that allows you to configure things like what's
installed on the image, timezone, password, ssh, etc.
"""
import urllib.request
import subprocess
import re
import os
from time import sleep

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
        os.system('clear')
        url = img_ext(images['Ubuntu 24.04'])
        filename = url.split('/')[-1]
        print('Downloading...')
        urllib.request.urlretrieve(url, filename)
        os.system('clear')
        print('Done!')
        sleep(1)
        configure(filename)
    elif img == '2':
        os.system('clear')
        url = img_ext(images["Ubuntu 22.04"])
        filename = url.split('/')[-1]
        print('Downloading...')
        urllib.request.urlretrieve(url, filename)
        os.system('clear')
        print('Done!')
        sleep(1)
        configure(filename)
    else:
        print('unrecognized input')

def configure(filename):
    os.system('clear')
    print(f'Configuring {filename}...')
    sleep(1)
    os.system('clear')
    print('libguestfs-tools must be installed for some parts of the configuration. Do u want to install it?')
    libguestfs = input('(Y/N): ')
    if libguestfs.lower() in ['y', 'yes']:
        try:
            subprocess.run(['sudo', 'apt', 'install', 'libguestfs-tools', '-y'], check=True)
        except subprocess.CalledProcessError as err:
            print(f'unable to install libguestfs-tools: {err}')
    else:
        print('libguestfs-tools is a requirement. exiting script...')
    vmid = input('Enter Virtual Machine ID: ')
    try:
        subprocess.run(['qm', 'set', f'{vmid}', '--serial0', 'socket', '--vga', 'serial0'], check=True)
    except subprocess.CalledProcessError as err:
        print(f'Invalid Virtual Machine ID: {err}')

if __name__ == '__main__':
    setup()