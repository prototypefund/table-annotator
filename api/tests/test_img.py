from typing import Text
import pytest
import numpy as np

import table_annotator.img
import table_annotator.io
from table_annotator.types import Point, Rectangle


@pytest.mark.parametrize("img_path, width, height",
                         [("test_images/ducks_1.jpeg", 620, 465),
                          ("test_images/ducks_2.jpg", 640, 427)])
def test_get_dimensions(img_path: Text, width: int, height: int) -> None:
    image = table_annotator.io.read_image(img_path)
    assert (width, height) == table_annotator.img.get_dimensions(image)


def test_crop() -> None:
    img_path = "test_images/bluegreen.png"
    image = table_annotator.io.read_image(img_path)

    blue_part = table_annotator.img.crop(image,
                                         Rectangle(topLeft=Point(x=0, y=0),
                                                   bottomRight=Point(x=100, y=100)))
    green_part = table_annotator.img.crop(image,
                                          Rectangle(topLeft=Point(x=100, y=0),
                                                    bottomRight=Point(x=200, y=100)))
    assert blue_part.shape == (100, 100, 3)
    assert green_part.shape == (100, 100, 3)
    assert np.all(blue_part == [255, 0, 0])
    assert np.all(green_part == [0, 255, 0])


def test_get_image_rectangle_borders() -> None:
    img_path = "test_images/bluegreen.png"
    image = table_annotator.io.read_image(img_path)

    oversized_part = table_annotator.img.crop(image,
                                              Rectangle(topLeft=Point(x=-10, y=-10),
                                                        bottomRight=Point(x=210, y=110)))
    assert oversized_part.shape == (100, 200, 3)


def test_extract_table() -> None:
    img_path = "test_images/0100_5312606_1.jpg"
    table_json_path = "test_images/0100_5312606_1.json"

    image = table_annotator.io.read_image(img_path)
    table = table_annotator.io.read_tables(table_json_path)[0]

    table_image_part = table_annotator.img.extract_table(image, table)

    assert table_image_part.shape == (table.outline.height(), table.outline.width(), 3)

    # table_annotator.io.write_image("cell_test/table.jpg", table_image_part)


def test_get_cell_grid() -> None:
    table_json_path = "test_images/0100_5312606_1.json"
    table = table_annotator.io.read_tables(table_json_path)[0]

    expected_rows = len(table.rows) + 1
    expected_columns = len(table.columns) + 1
    cell_grid = table_annotator.img.get_cell_grid(table)
    assert len(cell_grid) == expected_rows
    for row in cell_grid:
        assert len(row) == expected_columns


def test_get_cell_image_grid() -> None:
    img_path = "test_images/0100_5312606_1.jpg"
    table_json_path = "test_images/0100_5312606_1.json"

    image = table_annotator.io.read_image(img_path)
    table = table_annotator.io.read_tables(table_json_path)[0]

    cell_image_grid = table_annotator.img.get_cell_image_grid(image, table)
    for i, row in enumerate(cell_image_grid):
        for j, img in enumerate(row):
            continue
            # table_annotator.io.write_image(f"cell_test/{i}_{j}.jpg", img)