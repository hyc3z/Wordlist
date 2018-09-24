import re


def read(filename):
    f = open(filename, "r")
    strn = f.read()
    fpt = {}
    res = re.split('\n', strn)
    for i in range(1, len(res), 2):
        fpt[res[i-1]] = [res[i]]
    f.close()
    return fpt


def write(filename, a):
    f = open(filename, "w+")
    for i in a:
        f.write(i+"\n")
        a[i].append('0')
        a[i].append('0')
        for k in a[i]:
            f.write(k + "\n")
    f.close()


def main():
    filename = "wordlist.txt"
    a = read(filename)
    write(filename, a)


if __name__ == '__main__':
    main()
