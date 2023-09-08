"""A collection of useful functions.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

from pathlib import Path

# import xml.etree.ElementTree as ET
import defusedxml.ElementTree


def read_ocad_file(filename: Path):
    """Reads an OCAD file and prints information about controls."""
    print(f"Parsing file {filename}")
    root = defusedxml.ElementTree.parse(filename).getroot()
    # root = tree.getroot()
    print(len(root))

    tag_name = "{http://www.orienteering.org/datastandard/3.0}Control"
    for control in root.iter(tag_name):
        id = ""
        x_pos = 0
        y_pos = 0
        for sub in list(control):
            if sub.tag[-2:] == "Id":
                id = sub.text
            if sub.tag[-11:] == "MapPosition":
                x_pos = sub.attrib.get("x")
                y_pos = sub.attrib.get("y")
                # print(f"{id}: {sub.attrib}")
                print(f"{id}: {x_pos=} {y_pos=}")
