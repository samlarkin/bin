#!/usr/bin/python3
import pyqrcode
url = pyqrcode.create('https://samlarkin.xyz')
url.svg('samlarkin_url.svg', scale=8)
