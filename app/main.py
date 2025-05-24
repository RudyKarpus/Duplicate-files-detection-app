from detection_module import hash, find_duplicates
import sys


def scan_folder(folder):
    # return list of files paths in folder
    pass

def delete_files(path_list):
    # deletes files
    pass

def main():
    if len(sys.argv) != 2:
        print("Help: python main.py <path>")
        sys.exit(1)
    folder = sys.argv[1]
    files = scan_folder(folder)
    hash_list = []
    for path in files:
        h = hash(path)
        if h is not None:
            hash_list.append((h, path))

    duplicates = find_duplicates(hash_list)
    if len(duplicates) != 0:
        print("Found 0 duplicates")
        sys.exit(0)
    for duplicate in duplicates:
        print("Found duplicates:")
        for file in duplicate:
            print(f"{file}")
        print("")

    print("Delete them? (YES/NO)")
    answer = input()

    if(answer == "YES"):
        delete_files(duplicates)
        
if __name__ == "__main__":
    main()
