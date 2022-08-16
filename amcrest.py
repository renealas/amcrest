from bs4 import BeautifulSoup
from typing import Optional, List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
import requests
import re

from vdataclass import Firmware

MANIFEST_URL = "https://amcrest.com/firmware/"


@dataclass_json
@dataclass
class VendorMetadata:
    product_family: str
    model: str
    raritan_status: str
    os: str
    landing_urls: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    firmware_urls: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    bootloader_url: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    release_notes: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    user_manual: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    md5_url: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None))
    data: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


# vendor provided URL type alias for clarity
VendorUrl = str


def main():
    manifest = get_manifest(MANIFEST_URL)
    output_firmware(manifest)


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def output_firmware(manifest: List[VendorMetadata]):
    vendor_firmwares = []

    # join models based on URL (ie some models are the same firmware)
    firmwareInfoData = []
    for m in manifest:
        if m.data != None:
            firmwareInfoData.append(m.data)

    for firmware in firmwareInfoData:
        cells = firmware.find_all('td')

        #Here we get Model and Image 
        model = cells[0].find('img').get('alt')
        imageData = cells[0].find('img').get('src')
        if imageData == 'https://amcrest.com/static/frontend/Amcrest/amcrest/en_US/Magento_Catalog/images/product/placeholder/small_image.jpg':
            image = None
        else:
            image = [imageData]

        #Here we get the Version and Realease Date
        cell1 = cells[1]

        amountbr = cell1.find_all('br')

        textC1 = cells[1].text.strip()

        if len(amountbr) == 0:
            if '/' in textC1:
                slash = find_nth(textC1, '/', 1)
                lengthText = len(textC1)
                
                validation = textC1[slash - 2 : slash].strip()
                if validation[0].isdigit():
                    if int(validation[0]) > 1:
                        realese_date = textC1[slash - 1 : lengthText].strip()
                    else:
                        realese_date = textC1[slash - 2 : lengthText].strip()
                else:
                    realese_date = textC1[slash - 1 : lengthText].strip()
        else:
            try:
                versionInfo = cell1.find('br').previous_sibling.strip()
                if versionInfo[0] == 'V' or versionInfo[0] == 'v':
                    version = versionInfo[1:]
                else:
                    version = versionInfo
                
                realese_date = cell1.find('br').next_sibling.strip()
            except:
                pass
        
        #Here we get File Size 
        size = cells[2].text.strip()
        
        #Here we get the URL and File Name 
        try:
            url = cells[6].find('a').get('href')
            filenameSlash = url.rfind('/')
            lengUrl = len(url)
            filename = url[filenameSlash + 1 : lengUrl]
            
        except:
            pass

        a = Firmware(
            version = version, 
            models = [model], 
            filename = filename,
            url = url,
            size_bytes = size,
            release_date = realese_date,
            device_picture_urls = image
        )

        vendor_firmwares.append(a)
        
    return vendor_firmwares


def get_manifest(manifest_url: str) -> List[VendorMetadata]:
    """
    Gets list of firmware from the vendor and marshalls it into a list of VendorMetadata
        :param manifest_url: str
        :return manifest: List[VendorMetadata]
    """
    amcrest_models = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.request("GET", manifest_url, headers=headers)
    html = response.content
    response.close()
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', {'class': 'table table-hover'})

    for table in tables:
        body = table.find('tbody')
        lines = body.find_all('tr')

        for line in lines:
            cells = line.find_all('td')

            model = cells[0].find('span').text
            data = line

            a = VendorMetadata(
                product_family=None,
                model=model,
                raritan_status=None,
                os=None,
                data=data,
            )
            amcrest_models.append(a)

    return amcrest_models


if __name__ == "__main__":
    main()
