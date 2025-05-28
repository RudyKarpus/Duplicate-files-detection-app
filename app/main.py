import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import scan_folder
from workers import delete_file_worker, hash_worker

from detection_module import find_duplicates


def main():
    if len(sys.argv) != 2:
        print(
            "Help:\n "
            "python main.py <path>\n"
            "<path>: path to catalog to check for duplicates"
            ""
        )
        sys.exit(1)
    folder = sys.argv[1]
    files = scan_folder(folder)
    hash_list = []
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        future_to_path = {executor.submit(hash_worker, path): path for path in files}
        for future in as_completed(future_to_path):
            result = future.result()
            if result:
                hash_list.append(result)

    duplicates = find_duplicates(hash_list)
    if len(duplicates) == 0:
        print("Found 0 duplicates")
        sys.exit(0)
    for duplicate in duplicates:
        print("Found duplicates:")
        for file in duplicate:
            print(f"{file}")
        print("")

    print("Delete duplicates them? (YES/NO)")

    while True:
        answer = input()

        if answer == "YES":
            files_to_delete = []
            for group in duplicates:
                files_to_delete.extend(group[1:])

            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(delete_file_worker, path)
                    for path in files_to_delete
                ]
                for future in as_completed(futures):
                    future.result()
            sys.exit(0)

        if answer == "NO":
            sys.exit(0)


if __name__ == "__main__":
    main()
