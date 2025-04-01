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

COLUMN_NAMES = ["x-coordinate", "Character", "y-coordinate"]
COLUMN_TYPES = {COLUMN_NAMES[0]: int, COLUMN_NAMES[1]: str, COLUMN_NAMES[2]: int}

X_COLUMN = 0
Y_COLUMN = 2
CHAR_COLUMN = 1


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

def df_row_to_grid(row: pd.Series, grid: np.ndarray) -> None:
    """Takes a row of x, y, and character and adds the char to the given coordinates in the specified grid"""

    # break info from row
    x, char, y = row

    # get size of the Y column
    y_size = grid.shape[1]

    # update grid
    grid[x, y_size - (y + 1)] = char


def html_to_array(html: str):
    """Converts an HTML string to an array"""

    soup = BeautifulSoup(html, "html.parser")

    # get first table
    table = soup.find("table")

    # there are obviously other ways to do this, but this feels the most readable

    # get each cell
    text_cells = [
                    # get cells from rows
                    [cell.get_text() for cell in row.find_all("td")]

                    # parse each row
                    for row in table.find_all("tr")[1:]
                 ]

    # convert to dataframe with correct types (infer objects means everything isn't strs)
    df = pd.DataFrame(text_cells, columns=COLUMN_NAMES)
    df = df.astype(COLUMN_TYPES)

    # find highest x & y values
    x_max = df.iloc[:, X_COLUMN].max()
    y_max = df.iloc[:, Y_COLUMN].max()

    # create 2D list of correct size
    chars = np.full((x_max + 1, y_max + 1), ' ', dtype="U1", order='F')

    print(type(chars))

    # fill list with correct values (add the values of each row to chars)
    df.apply(df_row_to_grid, args=(chars,), axis=1)

    # print list (transpose first, makes operations easier)
    for column in chars.T:
        for cell in column:
            print(cell, end="")
        print()



def url_to_grid(url: str = TEST_URL):
    """Prints a grid of characters based on a URL's contents"""

    html = url_to_string(url)
    html_to_array(html)


print(url_to_grid())