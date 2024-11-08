# WebGroper

WebGroper is a Python class designed to recursively scrape and download media files (images, PDFs, etc.) from a specified website directory, such as the `/wp-content/uploads` directory of a WordPress site.

## Features

- Recursively traverses URLs to find and download media files.
- Ignores resized images generated by WordPress.
- Saves downloaded files in a structured directory.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:

    ```sh
    pip install requests beautifulsoup4
    ```

## Usage

1. Create an instance of the `WebGroper` class with the desired parameters.
2. Call the `traverse_url_recursive` method with the starting URL.

Example:

```python
from webgroper import WebGroper

# Initialize the WebGroper class
web_groper = WebGroper(
    output_directory="groped_data",
    time_between_download_requests=1,
    ignore_sizes_regex=r"-\d+x\d+\.[a-z]+"
)

# Start scraping from the specified URL
web_groper.traverse_url_recursive("https://example-wordpress-site.com/wp-content/uploads/")