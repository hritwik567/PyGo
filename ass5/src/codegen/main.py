import sys
import asm

if len(sys.argv) != 3:
    print("Usage: python main.py <.ir> <.csymt>")
    exit(1)

#Load 3AC
f = open(sys.argv[1])
tac = f.read()
f.close()
tac = [ i.split(',') for i in tac.split()]

#Load Symbol Table
f = open(sys.argv[2])
_st = f.read()
f.close()
st = {}
for i in _st.split():
    st[i.split(',')[0]] = i.split(',')[1:]

assembly = asm.ASM(tac, st)
f = open(sys.argv[1][:-3] + ".s", "w")
for i in assembly.generate():
    f.write(i + "\n")
f.close()
