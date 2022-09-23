#!/usr/bin/env python

import re 
import sys
from urllib import response 

from autopkglib import URLGetter

import html

BASE_URL = 'https://www.maplesoft.com/support/downloads/'
BASE_URL2 = 'https://www.maplesoft.com/downloads/'
REGEX1 = fr'\/support\/downloads\/(m{{0}}[_\d]+update\.aspx)\"\ class=\"main-text-color\">Maple ({{0}}[\.\d]+) Update'
REGEX2 = fr"https:\/\/www\.maplesoft\.com\/downloads\/(\?d=[\d\w]+&pr=Maple{{}}[\.\d]+UpdateInstallers)"
__all__ = ['MaplesoftURLProvider']

class MapleUpdateURLProvider(URLGetter):
    """Provides a download URL for the latest update for Maple"""

    description = __doc__
    input_variables = {'MajorVersion': {
        "required": False,
        "description": (
            'Major version to download the right version of maple'
            ),}
        }
    output_variables = {'url': {'description': 'URL to latest version'}}

    def main(self):
        html_source = self.download(BASE_URL).decode("utf-8")
        response = re.search(REGEX1.format(self.env.get("MajorVersion","2021")), html_source)
        escaped_url = response.group(1)
        version = response.group(2)
        url = html.unescape(escaped_url)
        html_source2 = self.download(BASE_URL + url).decode("utf-8")
        final_url = re.search(REGEX2.format(self.env.get("MajorVersion",'2021')), html_source2).group(1)
        url2 = html.unescape(final_url)
        if self.env["verbose"] > 0:
            print("MapleUpdateURLProvider: Match found is: {}\n".format(final_url))
            print("MapleUpdateURLProvider: Unescaped url is: {}\n".format(url2))
            print("MapleUpdateURLProvider: Returning full url: {}{}".format(BASE_URL2, url2))

        self.env["url"] = BASE_URL2 + url2
        self.env["VERSION"] = version

if __name__ == "__main__":
    processor = MapleUpdateURLProvider()
    processor.execute_shell()

