import httpx
from lxml import html

def fetch_url(url):
    """
    Fetches the content of the given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The content of the page if successful, None otherwise.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.content
    except httpx.RequestError as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def extract_from_url(url, xpath_filter : str | list = "//a/@href"):
    """
    Fetches all `a href` links from the given URL.

    Args:
        url (str): The URL to fetch links from.

    Returns:
        list: A list of href links found on the page.
    """

    content = fetch_url(url)
    if content is None:
        return []
    tree = html.fromstring(content)
    if isinstance(xpath_filter, str):
        xpath_filter = [xpath_filter]
    l_links = []
    for xf in xpath_filter:
        l_links.append(tree.xpath(xf))
    return l_links



month_to_num = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}