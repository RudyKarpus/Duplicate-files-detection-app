import os


def scan_folder(folder):
    """Return: list of files paths in folder"""
    paths = []
    for root, _, files in os.walk(folder):
        for name in files:
            paths.append(os.path.join(root, name))

    return paths
