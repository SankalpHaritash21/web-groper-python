class WebsiteNotFoundError(Exception):
    """
    An exception raised when a website is not found.
    """

    pass


class FileDownloadError(Exception):
    """
    An exception raised when a file download fails.
    """

    pass


# CONSTANTS
WEBSITE_IS_REQURIED = WebsiteNotFoundError("Website URL is required.")
FILE_DOWNLOAD_ERROR = FileDownloadError("Failed to download file.")
