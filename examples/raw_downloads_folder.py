"""Set a custom browser downloads folder per driver instance.

Run with:  python examples/raw_downloads_folder.py

The "downloads_folder" option lets each driver save downloaded files to
its own folder, instead of all drivers sharing the default location
(the "downloaded_files/" folder in the current working directory).
This makes it possible to run multiple isolated instances in parallel,
each one downloading into a separate folder.

(The "downloads_folder" option is also available via the "SB()" manager,
 "self.get_new_driver()", the "--downloads-folder" pytest command-line
 option, and "behave -D downloads-folder=DIR".)
"""
import os
import time
from seleniumbase import Driver

# A simple page with a link that downloads a text file when clicked.
DOWNLOAD_PAGE = (
    "data:text/html,"
    "<a id='dl' download='hello.txt' "
    "href='data:text/plain,Hello from SeleniumBase'>Download</a>"
)


def wait_for_file(file_path, timeout=10):
    stop_time = time.time() + timeout
    while time.time() < stop_time:
        if os.path.exists(file_path):
            return True
        time.sleep(0.2)
    return False


def run_instance(downloads_folder, file_name):
    driver = Driver(
        browser="chrome",
        headless=True,
        downloads_folder=downloads_folder,
    )
    try:
        driver.get(DOWNLOAD_PAGE)
        driver.click("#dl")  # Click the link to download the file
        expected_file = os.path.join(
            os.path.abspath(downloads_folder), file_name
        )
        assert wait_for_file(expected_file), (
            "Expected downloaded file not found: %s" % expected_file
        )
        print("Downloaded file saved to: %s" % expected_file)
    finally:
        driver.quit()


if __name__ == "__main__":
    # Two separate instances, each with its own downloads folder.
    run_instance("downloads_instance_1", "hello.txt")
    run_instance("downloads_instance_2", "hello.txt")
