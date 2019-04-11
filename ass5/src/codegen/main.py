import sys
import asm
import csv

if len(sys.argv) != 3:
    print("Usage: python main.py <.ir> <.csymt>")
    exit(1)

#Load 3AC
f = open(sys.argv[1])
reader = csv.reader(f, delimiter=',', quotechar="'")
tac = [row for row in reader]
f.close()

#Load Symbol Table
f = open(sys.argv[2])
reader = csv.reader(f, delimiter=',', quotechar='"')
st = {}
for row in reader:
    st[row[0]] = row[1:]
f.close()

assembly = asm.ASM(tac, st)
f = open(sys.argv[1][:-3] + ".s", "w")
for i in assembly.generate():
    f.write(i + "\n")
f.close()
