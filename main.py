import os
import glob
import shutil
import argparse

class Args:
    def __init__(self):
        self.path = ""
        self.text = ""
        self.debug = False
        self.ext = ""

def main():
    args = Args()
    while True:
        print('\nEnter retrieval root directory:')
        args.path = input()
        path = os.path.abspath(args.path)
        if os.path.isdir(path):
            break
        else:
            print("invalid path: {}".format(path))

    print('Enter target text:')
    args.text = input()

    print('Enter target file extension (default: not specific extension):')
    args.ext = input()

    search(args.path, args)

def search(path, args):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print("invalid path: {}".format(path))
        return

    items = sorted(os.listdir(path))
    if args.ext == "":
        file_items = [os.path.join(path, item) for item in items if not os.path.isdir(os.path.join(path, item))]
    else:
        ext = str(args.ext).lstrip(".")
        file_items = glob.glob(os.path.join(path, "*.{}".format(ext)))

    for file_item in file_items:
        try:
            with open(file_item, "r") as file:
                content = file.read()
                if args.text.lower() in content.lower():
                    print("found in {}".format(file_item))
                    lines = content.split("\n")
                    for index, line in enumerate(lines):
                        if args.text in line:
                            print("\tline: {}".format(index))
                else:
                    pass
                    # print("not found in {}".format(file_item))
        except Exception as e:
            if args.debug:
                print("cannot read {}: {}".format(file_item, e))

    # recursively search folders
    folder_items = [os.path.join(path, item) for item in items if os.path.isdir(os.path.join(path, item))]
    for folder_item in folder_items:
        search(folder_item, args)


if __name__ == '__main__':
    main()
