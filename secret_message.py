"""Code to decode a "Secret Message" for SE320
Author: Taylor Hancock
Date:   03/30/2025
Class:  SE320 - Software Construction
Assignment: Decode a Secret Message - Extra Credit
"""

from bs4 import BeautifulSoup
from requests import get, RequestException
import pandas as pd
import numpy as np


TEST_URL = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"


def url_to_string(url: str) -> str | None:
    """Gets a string from a URL or None if failed"""

    text_out = None

    try:
        response = get(url, timeout=20)
        # if call fails, raise status as exception
        response.raise_for_status()
        text_out = response.text

    except RequestException as e:
        print(f"Document failed to load: {e}")

    return text_out

def html_to_array(html: str):
    """Converts an HTML string to an array"""

    X_COLUMN = 0
    Y_COLUMN = 2
    CHAR_COLUMN = 1

    soup = BeautifulSoup(html, "html.parser")

    # get first table
    table = soup.find("table")

    # there are obviously other ways to do this, but this feels the most readable

    # get column names
    column_row = table.find("tr")
    column_names = [cell.get_text() for cell in column_row.find_all("td")]

    # get each cell
    text_cells = [
                    # get cells from rows
                    [cell.get_text() for cell in row.find_all("td")]

                    # parse each row
                    for row in table.find_all("tr")[1:]
                 ]
    
    # convert to dataframe with correct types (infer objects means everything isn't strs)
    df = pd.DataFrame(text_cells, columns=column_names)
    df = df.astype({"x-coordinate": int, "Character": str, "y-coordinate": int})
    print(df.dtypes)

    print(df)

    # find highest x & y values
    x_max = df.iloc[:, X_COLUMN].max()
    y_max = df.iloc[:, Y_COLUMN].max()

    # create 2D list of correct size
    chars = np.full((x_max, y_max), ' ', dtype="U1")

    # fill list with correct values
    for x, char, y in df.T.iteritems:
        chars[row, y] = char

    # print list
    for row in chars:
        for cell in row:
            print(cell)



def url_to_grid(url: str = TEST_URL):
    """Prints a grid of characters based on a URL's contents"""

    html = url_to_string(url)
    html_to_array(html)


print(url_to_grid())