#!/usr/bin/env python

import re 
import sys
from urllib import response 

from autopkglib import URLGetter

from html.parser import HTMLParser

BASE_URL = 'https://www.maplesoft.com/support/downloads/'
BASE_URL2 = 'https://www.maplesoft.com/downloads/'
REGEX1 = r"\/support\/downloads\/(m\d{4}[_\d]+update\.aspx)\"\ class=\"main-text-color\">Maple (2021\.2\.1) Update"
REGEX2 = r"https:\/\/www\.maplesoft\.com\/downloads\/(\?d=[\d\w]+&pr=Maple\d{4}[\.\d]+UpdateInstallers)"
__all__ = ['MaplesoftURLProvider']

class MapleUpdateURLProvider(URLGetter):
    """Provides a download URL for the latest update for Maple"""

    description = __doc__
    input_variables = {}
    output_variables = {'url': {'description': 'URL to latest version'}}

    def main(self):
        html_source = self.download(BASE_URL).decode("utf-8")
        response = re.search(REGEX1, html_source)
        escaped_url = response.group(1)
        version = response.group(2)
        url = HTMLParser().unescape(escaped_url)
        html_source2 = self.download(BASE_URL + url).decode("utf-8")
        final_url = re.search(REGEX2, html_source2).group(1)
        url2 = HTMLParser().unescape(final_url)
        if self.env["verbose"] > 0:
            print("F5transkriptURLProvider: Match found is: {}\n".format(final_url))
            print("F5transkriptURLProvider: Unescaped url is: {}\n".format(url2))
            print("F5transkriptURLProvider: Returning full url: {}{}".format(BASE_URL2, url2))

        self.env["url"] = BASE_URL2 + url2
        self.env["VERSION"] = version

if __name__ == "__main__":
    processor = MapleUpdateURLProvider()
    processor.execute_shell()

