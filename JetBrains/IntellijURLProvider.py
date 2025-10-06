#!/usr/local/autopkg/python
"""Intellij URL Provider."""
# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import

import sys
from xml.dom import minidom

from autopkglib import ProcessorError, URLGetter

__all__ = ["IntellijURLProvider"]

intellij_version_url = "https://www.jetbrains.com/updates/updates.xml"


class IntellijURLProvider(URLGetter):
    """Provide URL for latest Intellij IDEA build."""

    description = "Provides URL and version for the latest release of Intellij."
    input_variables = {
        "base_url": {
            "required": False,
            "description": (
                "Default is " "https://www.jetbrains.com/updates/updates.xml"
            ),
        },
        "edition": {
            "required": False,
            "description": (
                'Either "C" for "Community" or "U" for "Ultimate" '
                'edition. Defaults to "C".'
            ),
        },
        "arch": {
            "required": False,
            "description": (
                'Target architecture: "intel" (default) or "aarch64" '
                '(Apple Silicon).'
            ),
        },
    }
    output_variables = {"url": {"description": "URL to the latest release of Intellij"}}

    __doc__ = description

    def get_intellij_version(self, intellij_version_url):
        """Retrieve version number from XML."""
        # Read XML
        try:
            # Check Major Python version (2 or 3)
            if sys.version_info.major < 3:
                html = self.download(intellij_version_url)
            else:
                html = self.download(intellij_version_url).decode("utf-8")
        except Exception as e:
            raise ProcessorError("Can not download %s: %s" % (intellij_version_url, e))

        root = minidom.parseString(html)
        # Get all products in the XML
        products = root.childNodes[0].getElementsByTagName("product")

        intellij_product = None
        for product in products:
            if (
                product.hasAttribute("name")
                and product.getAttribute("name") == "IntelliJ IDEA"
            ):
                intellij_product = product

        if intellij_product is not None:
            channels = intellij_product.getElementsByTagName("channel")
            for channel in channels:
                if (
                    channel.hasAttribute("licensing")
                    and channel.getAttribute("licensing") == "release"
                ):
                    if channel.hasAttribute(
                        "name"
                    ) and "EAP" not in channel.getAttribute("name"):
                        builds = channel.getElementsByTagName("build")
                        available_versions = list()
                        for build in builds:
                            if build.hasAttribute("version"):
                                available_versions.append(build.getAttribute("version"))
                        available_versions.sort(reverse=True)
                        # We can return here because we found the release channel.
                        return str(available_versions[0])
        else:
            raise ProcessorError("Did not find Intellij in version XML.")

    def main(self):
        """Main function."""
        # Determine values.
        version_url = self.env.get("version_url", intellij_version_url)
        version = self.get_intellij_version(version_url)
        edition = self.env.get("edition", "C")
        arch = self.env.get("arch", "intel")
        if arch == "aarch64":
            download_url = "https://download.jetbrains.com/idea/" "ideaI%s-%s-aarch64.dmg" % (
                edition,
                version,
            )
        else:
            download_url = "https://download.jetbrains.com/idea/" "ideaI%s-%s.dmg" % (
                edition,
                version,
            )

        self.env["url"] = download_url
        self.output("URL: %s" % self.env["url"])


if __name__ == "__main__":
    processor = IntellijURLProvider()
    processor.execute_shell()
