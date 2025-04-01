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
FINAL_URL = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"


COLUMN_NAMES = ["x-coordinate", "Character", "y-coordinate"]
COLUMN_TYPES = {COLUMN_NAMES[0]: int, COLUMN_NAMES[1]: str, COLUMN_NAMES[2]: int}

X_COLUMN = 0
Y_COLUMN = 2
CHAR_COLUMN = 1


def url_to_string(url: str) -> str | None:
    """Gets a string from a URL or None if failed"""
    text_out = None

    # try to get response
    try:
        response = get(url, timeout=20)
        # if call fails, raise status as exception
        response.raise_for_status()
        text_out = response.text

    except RequestException as e:
        print(f"Document failed to load: {e}")

    return text_out


def df_row_to_grid(row: pd.Series, grid: np.ndarray) -> None:
    """Adds a character to the given coordinates in the specified grid from a row"""
    # break info from row
    x, char, y = row

    # get size of the Y column
    y_size = grid.shape[1]

    # update grid
    grid[x, y_size - (y + 1)] = char


def html_to_2d_list(html: str):
    """Converts an HTML string to a 2D list"""
    soup = BeautifulSoup(html, "html.parser")

    # get first table
    table = soup.find("table")

    # there are obviously other ways to do this, but this feels the most readable & speedy
    # get each cell
    text_cells = [
                    # get cells from rows
                    [cell.get_text() for cell in row.find_all("td")]

                    # parse each row
                    for row in table.find_all("tr")[1:]
                 ]

    return text_cells


def list_to_char_grid(array: list[list]) -> np.ndarray:
    """Converts a 2D list into a character grid"""
    # convert to dataframe with correct types (infer objects means everything isn't strs)
    df = pd.DataFrame(array, columns=COLUMN_NAMES)
    df = df.astype(COLUMN_TYPES)

    # find highest x & y values
    x_size = df.iloc[:, X_COLUMN].max() + 1
    y_size = df.iloc[:, Y_COLUMN].max() + 1

    # create 2D list of correct size
    chars = np.full((x_size, y_size), ' ', dtype="U1")

    # fill list with correct values (add the values of each row to chars)
    df.apply(df_row_to_grid, args=(chars,), axis=1)

    return chars


def print_char_grid(char_grid: np.ndarray) -> None:
    """Prints a given character grid"""
    # print list (transpose first, makes operations easier)
    for column in char_grid.T:
        for cell in column:
            print(cell, end="")
        print()


def url_to_grid(url: str = TEST_URL):
    """Prints a grid of characters based on a URL's contents"""
    html  = url_to_string(url)
    array = html_to_2d_list(html)
    chars = list_to_char_grid(array)

    print_char_grid(chars)


if __name__ == "__main__":
    # try example
    url_to_grid()
    print()

    # try real url
    url_to_grid(FINAL_URL)
