# -------------------------------
# BUILT-IN MODULES
import os
import re
import time

# THIRD_PARTY MODULES
import requests
import urllib.parse
from bs4 import BeautifulSoup

# LOCAL MODULES
from .exception import WEBSITE_IS_REQURIED, FILE_DOWNLOAD_ERROR
# -------------------------------


class WebGroper:
    """
    A class to scrape media files from a website using a recursive traversal algorithm.
    """

    def __init__(
        self,
        # website_url=None,
        output_directory="groped_data",
        time_between_download_requests=1,
        ignore_sizes_regex=r"-\d+x\d+\.[a-z]+",
    ):
        """
        Initialize the WebGroper class with the following parameters:
        - website_url: The URL of the website to scrape.
        - output_directory: The directory where the scraped files will be saved.
        - time_between_download_requests: The time to wait between downloading files.
        - ignore_sizes_regex: A regular expression pattern to ignore URLs that match.
        """
        # self.website_url = website_url
        self.output_directory = output_directory
        self.time_between_download_requests = time_between_download_requests
        self.ignore_sizes_regex = ignore_sizes_regex

    def download_file(self, url, save_path):
        """Downloads a file from a URL and saves it to the specified path."""
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"File downloaded: {save_path}")
            else:
                # print(
                #     f"Failed to download: {url} (Status Code: {response.status_code})"
                # )
                raise FILE_DOWNLOAD_ERROR
        except Exception as e:
            # print(f"Error downloading {url}: {e}")
            raise FILE_DOWNLOAD_ERROR

    def traverse_url_recursive(self, url=None):
        """Recursively traverses a URL and downloads media files."""

        # Ignore URLs that match the ignore pattern
        if re.search(self.ignore_sizes_regex, url):
            return

        try:
            # Check if the URL is an HTML page
            if url is not None:
                response = requests.head(url, allow_redirects=True)
            else:
                raise WEBSITE_IS_REQURIED
        except Exception as e:
            # print(f"Failed to reach URL {url}: {e}")
            return

        content_type = response.headers.get("Content-Type", "")

        if "html" in content_type:
            # Process HTML page and look for links
            try:
                response = requests.get(url)
                html_parsed = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                print(f"Error parsing HTML at {url}: {e}")
                return

            # Traverse links within the HTML
            for link in html_parsed.find_all("a", href=True):
                link_text = link.get_text(strip=True)
                if link_text not in {
                    "Name",
                    "Last modified",
                    "Size",
                    "Description",
                    "Parent Directory",
                }:
                    next_url = urllib.parse.urljoin(url, link["href"])
                    self.traverse_url_recursive(next_url)

        else:
            # Download non-HTML content (e.g., images, videos, PDFs)
            time.sleep(self.time_between_download_requests)

            # Derive file path within the data directory
            file_path = os.path.join(
                self.output_directory, urllib.parse.urlparse(url).path.lstrip("/")
            )

            # Create necessary directories if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Download file
            self.download_file(url, file_path)
