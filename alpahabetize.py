'''
This module will take a text file and alphabetize it.

Example
-------
    $ python alphabetize.py items.csv
Alphabetizes items.csv by the first character on each line.
'''
import argparse

def get_file_to_alphabetize():
    '''
    Sets up command-line arguments and gets to file to be alphabeitzed.

    Attributs
    ---------
    parser : ArgumentParser
        Parses command-line arguments

    args : Parsed Arguments
    '''
    parser = argparse.ArgumentParser(description="Alphabetize a file")
    parser.add_argument('file', nargs='?', default='items.csv')
    args = parser.parse_args()
    parser.parse_args()
    return args.file


def alphabetize_file(filename):
    '''
    Alphabetizes filename

    Attributes
    ----------
    file_to_alphabetize : file
        The file to be alphabetized

    lines : list
        List of the lines from filename
    '''
    with open(filename, 'r+') as file_to_alphabetize:
        lines = file_to_alphabetize.readlines()
        lines.sort()
        file_to_alphabetize.seek(0)
        for line in lines:
            file_to_alphabetize.write(line)
    file_to_alphabetize.close()


if __name__ == '__main__':
    # Hard-code this line if running from an IDE
    FILE = get_file_to_alphabetize()
    alphabetize_file(FILE)
