import argparse

def get_file_to_alphabetize():
    parser = argparse.ArgumentParser(description="Alphabetize a file")
    parser.add_argument('file', nargs='?', default='items.csv')
    args = parser.parse_args()
    parser.parse_args()
    return args.file


def alphabetize_file(filename):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        lines.sort()
        f.seek(0)
        for line in lines:
            f.write(line)
    f.close()
    


if __name__ == '__main__':
    FILE = get_file_to_alphabetize()
    alphabetize_file(FILE)
