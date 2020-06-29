#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import re

from autopkglib import URLGetter

import sys

try:
    # import for Python 3
    from html.parser import HTMLParser
except ImportError:
    # import for Python 2
    from HTMLParser import HTMLParser


BASE_URL = "https://www.audiotranskription.de"
REGEX = '(/audot/downloadfile\.php\?k=\d\&amp;d=\d{2}\&amp;l=de\&amp;c=.{5,15})\\"\>MAC OS \(F5\) \[v7\]'

__all__ = ["F5transkriptURLProvider"]


class F5transkriptURLProvider(URLGetter):
    """Provides a download URL for the latest version of F5transkript"""

    description = __doc__
    input_variables = {}
    output_variables = {"url": {"description": "URL to latest version"}}

    def main(self):
        if sys.version_info.major < 3:
            html_source = self.download(BASE_URL + "/downloads.html")
        else:
            html_source = self.download(BASE_URL + "/downloads.html").decode("utf-8")
        escaped_url = re.search(REGEX, html_source).group(1)
        url = HTMLParser().unescape(escaped_url)
        if self.env["verbose"] > 0:
            print(
                "F5transkriptURLProvider: Match found is: %s\n"
                "F5transkriptURLProvider: Unescaped url is: %s\n"
                "F5transkriptURLProvider: Returning full url: %s%s"
                % (escaped_url, url, BASE_URL, url)
            )

        self.env["url"] = BASE_URL + url


if __name__ == "__main__":
    processor = F5transkriptURLProvider()
    processor.execute_shell()
