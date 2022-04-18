import re
import glob

search_str = input("Укажите строку : ")
files = glob.glob('*.txt')
for v_file in files:
    print(v_file)
    idx = 1
    textfile = open(v_file, 'r')
    line = textfile.readline()
    feof = True
    while feof:
        index = line.find(search_str)
        if (index != -1) :
            print("[", idx, ",", index, "] ", line, sep="")
        line = textfile.readline()
        idx += 1
        if not line:
            feof=False
    textfile.close()
