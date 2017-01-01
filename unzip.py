import zipfile
import sys
import argparse


def extractFile(openZip,password):
    try:
        openZip.extractall(path='./',pwd=password)
        return password
    except Exception as e:
        return

def main():
    with zipfile.ZipFile(sys.argv[1]) as openZip:
        passFile = open(sys.argv[2])
        for line in passFile.readlines():
            password = line.strip('\n')
            guess = extractFile(openZip,password)
            if guess:
                print("yes",password)
                exit(0)
            else:
                pass

if __name__ == '__main__':
    main()