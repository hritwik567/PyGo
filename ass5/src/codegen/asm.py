from regs import Register

#Free eax before function call
#figure out how to use ecx and save it before function call
#There might be a problem if the return value is never being used it may cause some issue
# Verify the support for pointer and stuff dereferencing and stuff

def is_int(s):
    if s == True or s == False:
        return False
    try:
        int(s)
    except ValueError:
        return False
    return True

class ASM:
    def __init__(self, tac, st):
        self.tac = tac
        self.st = st
        self.asm = [".section .text", ".globl main", ""]
        self.constants = []
        self.temp_dict = dict()
        self.eax = Register("%eax")
        self.ebx = Register("%ebx")
        self.ecx = Register("%ecx")
        self.edx = Register("%edx")
        self.edi = Register("%edi")

        #used for func calls
        self.temp_asm = []
        self.return_temp = []

        self.op_map = {"int_+": "addl", "int_*": "imul", "int_-": "sub", "int_&": "and", "int_|": "or", "int_^": "xor", "int_>>": "shr"}
        self.rel_op = {"int_<": "jl", "int_<=": "jle", "int_==": "je", "int_!=": "jne", "int_>": "jg", "int_>=": "jge"}

    def generate(self):
        self.asm += ["main:", "call _func_main", "push $0", "call exit", ""]
        self.get_asm()
        self.asm += ["", ".section .data"] + self.constants #TODO change this
        return self.asm

    def save(self, val, temp, location = None, load = False):
        if self.eax.temp != None:
            if self.edx.temp != None and self.edx.location != None:
                self.asm += self.edx.wb()
            elif self.edx.temp != None and self.edx.location == None and load == True:
                if self.edi.temp == None and self.edi.location == None:
                    self.edi.saver(self.edx)
                    self.asm += ["movl %edx, %edi"]
                else:
                    assert (False), "Should not be here!"
            elif self.edx.temp != None and self.edx.location == None and self.edx.temp not in self.return_temp:
                assert (False), "Should not be here!"
            self.edx.saver(self.eax)
            self.asm += ["movl %eax, %edx"]
        self.eax.free()
        self.eax.save(temp, location)
        if load:
            self.asm += ["lea " + str(val) + ", %eax"]
        else:
            self.asm += ["movl " + str(val) + ", %eax"]

    def in_regs(self, temp):
        if self.eax.temp == temp:
            return self.eax
        elif self.edx.temp == temp:
            return self.edx
        elif self.edi.temp == temp:
            return self.edi
        else:
            return None

    def write_back(self):
        if self.eax.location != None:
            self.asm += self.eax.wb()
        if self.edx.location != None:
            self.asm += self.edx.wb()

    def free_regs(self):
        self.eax.free()
        self.ebx.free()
        self.ecx.free()
        self.edx.free()
        self.edi.free()

    def get_asm(self):
        i = -1
        while i < len(self.tac) - 1:
            i += 1
            attr = self.tac[i]
            # if "movl -112(%ebp), %ebx" in self.asm:
            #     print(attr)
            #     exit(1)
            if attr[0] == "label":
                #TODO: do we need to write back the registers before any label
                if "_end_if_" in attr[1] or "_end__for_" in attr[1]:
                    self.write_back()
                    self.free_regs()
                if "_for_" in attr[1]:
                    self.write_back()
                    self.free_regs()
                self.asm += [attr[1] + ":"]
            elif attr[0] == "func_begin":
                self.free_regs()
                self.asm += ["push %ebp", "movl %esp, %ebp"]
                self.asm += ["sub $" + str(abs(int(self.st[attr[1]][2]))) + ", %esp"]
            elif attr[0] == "func_end":
                self.write_back()
                self.asm += [attr[1] + ":", "movl %ebp, %esp", "pop %ebp", "ret", ""]
            elif attr[0] == "decl" or attr[0] == "argdecl":
                pass
            elif attr[0] == "(addr)":
                temp_loc = str(self.st[attr[1]][2]) + "(%ebp)" if attr[1] in self.st else None
                if attr[2] in self.st:
                    self.save(str(self.st[attr[2]][2]) + "(%ebp)", attr[1], temp_loc, True)
                else:
                    assert (False), "Should not be here"
            elif attr[0] == "(load)":
                if attr[2] == self.eax.temp:
                    temp_loc = str(self.st[attr[1]][2]) + "(%ebp)" if attr[1] in self.st else None
                    if attr[1] not in self.st:
                        self.asm += ["movl (%eax), %eax"]
                        self.eax.free()
                        self.eax.save(attr[1], temp_loc)
                    elif int(self.st[attr[1]][1]) == 4:
                        self.asm += ["movl (%eax), %eax"]
                        self.eax.free()
                        self.eax.save(attr[1], temp_loc)
                    elif int(self.st[attr[1]][1]) > 4:
                        temp_size = 0
                        while temp_size != int(self.st[attr[1]][1]):
                            self.asm += ["movl " + str(temp_size) + "(%eax), %ebx"]
                            self.asm += ["movl %ebx," + str(int(self.st[attr[1]][2]) + temp_size) + "(%ebp)"]
                            temp_size += 4
                        self.eax.free()
                    else:
                        assert (False), "Should not be here"

                elif attr[2] in self.st:
                    self.write_back()
                    if self.eax.temp != None and self.eax.location == None:
                        self.asm += ["movl %eax, %edx"]
                        self.edx.saver(self.eax)
                    temp_loc = str(self.st[attr[1]][2]) + "(%ebp)" if attr[1] in self.st else None
                    if temp_loc == None and int(self.st[attr[1][1]]) > 4:
                        assert (False), "Should not be here"
                    if int(self.st[attr[1]][1]) == 4:
                        self.asm += ["movl " + str(self.st[attr[2]][2]) + "(%ebp), %eax", "movl (%eax), %eax"]
                        self.eax.free()
                        self.eax.save(attr[1], temp_loc)
                    elif int(self.st[attr[1]][1]) > 4:
                        temp_size = 0
                        while temp_size != int(self.st[attr[1]][1]):
                            self.asm += ["movl " + str(self.st[attr[2]][2]) + "(%ebp), %eax"]
                            self.asm += ["movl " + str(temp_size) + "(%eax), %eax"]
                            self.asm += ["movl %eax," + str(int(self.st[attr[1]][2]) + temp_size) + "(%ebp)"]
                            temp_size += 4
                        self.eax.free()
                    else:
                        assert (False), "Should not be here"
                else:
                    assert (False), "Should not be here"
            elif attr[0] == "return": #all the returns will have an arg
                if attr[1] in self.temp_dict:
                    self.asm += ["movl " + self.temp_dict[attr[1]] + ", %eax"]
                elif attr[1] == self.eax.temp:
                    print("Return value already in eax!")
                    #TODO: do we need to free any regs here
                elif attr[1] in self.st:
                    self.asm += ["movl " + str(self.st[attr[1]][2]) + "(%ebp), %eax"]
            elif attr[0] == "goto":
                if "_end_if_" in attr[1] or "_for_" in attr[1]:
                    self.write_back()
                    self.free_regs()
                self.asm += ["jmp " + attr[1]]
            elif attr[0] == "push_begin":
                self.write_back()
                if self.edx.temp != None and self.edx.location == None and self.edx.temp not in self.return_temp:
                    assert (False), "Should not be here"
                if self.eax.temp != None and self.eax.location == None and self.eax.temp not in self.return_temp:
                    #should be freed after using them
                    self.asm += ["push %eax"]
                    self.temp_asm = [("pop %edx", self.eax.temp)]
                    self.eax.free()
                    self.edx.free()
                if self.edi.temp != None and self.edi.location == None:
                    #should be freed after using them
                    self.asm += ["push %edi"]
                    self.temp_asm = [("pop %edi", self.edi.temp)] + self.temp_asm
                    self.edi.free()
            elif attr[0] == "push":
                if attr[1] in self.temp_dict:
                    self.asm += ["push " + self.temp_dict[self.tac[i][1]]]
                elif attr[1] in self.st:
                    attr[2] = int(attr[2])
                    while attr[2] != 0:
                        attr[2] -= 4
                        self.asm += ["push " + str(int(self.st[self.tac[i][1]][2]) + attr[2]) + "(%ebp)"]
                elif self.in_regs(attr[1]):
                    self.asm += ["push " + self.in_regs(attr[1]).name]
                    self.in_regs(attr[1]).free()
                else:
                    assert (False), "Should not be here!"
            elif attr[0] == "call":
                self.asm += ["call " + attr[1]]
                i += 1
                self.eax.free()
                self.edx.free()
                self.edi.free()
                if self.tac[i][0] == "pop":
                    if self.tac[i][1] != "0":
                        self.asm += ["addl $" + self.tac[i][1] + ", %esp"]
                        for p in self.temp_asm:
                            self.asm += [p[0]]
                            if p[0] == "pop %edx":
                                self.edx.save(p[1])
                            elif p[0] == "pop %edi":
                                self.edi.save(p[1])
                            else:
                                assert (False), "Should not be here !"
                        self.temp_asm = []
                    i += 1
                else:
                    assert (False), "Should not be here!"

                if self.tac[i][0] == "=" and self.tac[i][2] == "return_value":
                    self.return_temp += [self.tac[i][1]]
                    if self.tac[i][1] in self.st:
                         self.eax.save(self.tac[i][1], str(self.st[self.tac[i][1]][2]) + "(%ebp)")
                    else:
                        self.eax.free()
                        self.eax.save(self.tac[i][1])
            elif attr[0] == "(store)":
                if attr[1] == self.eax.temp:
                    print("Address already in eax!")
                elif attr[1] in self.st:
                    self.save(str(self.st[attr[1]][2]) + "(%ebp)", "temp_var", None, True)
                else:
                    assert (False), "Should not be here!"

                if attr[2] == self.edi.temp:
                    self.asm += ["movl %edi, (%eax)"]
                    self.eax.free()
                    self.edi.free()
                elif attr[2] == self.edx.temp:
                    self.asm += ["movl %edx, (%eax)"]
                    self.eax.free()
                    self.edx.free()
                elif attr[2] in self.temp_dict:
                    self.asm += ["movl " + self.temp_dict[attr[2]] + ", (%eax)"]
                    self.eax.free()
                elif is_int(attr[2]):
                    self.asm += ["movl $" + attr[2] + ", (%eax)"]
                    self.eax.free()
                elif attr[2] in self.st:
                    self.asm += ["movl " + str(self.st[attr[2]][2]) + "(%ebp)" + ", %ebx", "movl %ebx, (%eax)"]
                    self.eax.free()
                else:
                    assert (False), "Should not be here!"
            elif attr[0] == "=":
                if attr[1] not in self.st:
                    if attr[2][:4] == "temp":
                        assert (False), "Should not be here!"
                    else:
                        if attr[2][0] == "'":
                            self.constants += [attr[1] + ': .string "' + attr[2][1:-1] + '"']
                            self.temp_dict[attr[1]] = "$" + attr[1]
                        elif attr[2] == "True" or attr[2] == "False":
                            print("Ignoring bool for now")
                        else:
                            self.temp_dict[attr[1]] = "$" + attr[2]
                else:
                    if attr[2][:4] == "temp":
                        if attr[2] in self.temp_dict:
                            self.save(self.temp_dict[attr[2]], attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                        elif self.in_regs(attr[2]) != None and attr[2] not in self.st:
                            self.in_regs(attr[2]).save(attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                        elif self.in_regs(attr[2]) != None and attr[2] in self.st:
                            self.asm += self.in_regs(attr[2]).wb()
                            self.in_regs(attr[2]).save(attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                        elif attr[2] in self.st:
                            self.save(str(self.st[attr[2]][2]) + "(%ebp)", attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                        else:
                            assert (False), "Should not be here!"
                    else:
                        if attr[2][0] == "'":
                            self.constants += [attr[1] + ': .string "' + attr[2][1:-1] + '"']
                            self.save("$" + attr[1], attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                        else:
                            self.save("$" + attr[2], attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
            elif attr[0] in self.op_map:
                self.write_back()
                # print(attr, "eax", self.eax.temp, self.eax.location, "edx", self.edx.temp, self.edx.location)
                if self.eax.temp != None and self.eax.location == None and self.eax.temp != attr[2] and self.eax.temp != attr[3]:
                    if self.edx.temp != None and self.edx.location == None and self.edx.temp == attr[2]:
                        self.asm += ["movl %eax, %ebx", "movl %edx, %eax", "movl %ebx, %edx"]
                        self.ebx.saver(self.eax)
                        self.eax.saver(self.edx)
                        self.edx.saver(self.ebx)
                    elif self.edx.temp != None and self.edx.location == None:
                        self.asm += ["movl %edx, %edi"]
                        self.edi.saver(self.edx)
                        self.asm += ["movl %eax, %edx"]
                        self.edx.saver(self.eax)
                    else:
                        self.asm += ["movl %eax, %edx"]
                        self.edx.saver(self.eax)

                # print(attr, "eax", self.eax.temp, self.eax.location, "edx", self.edx.temp, self.edx.location)


                if self.eax.temp == attr[3]:
                    self.ebx.save(attr[3]) #should add the location
                    self.asm += ["movl %eax, %ebx"]

                if attr[2] == self.edx.temp:
                    self.asm += ["movl %edx, %eax"]
                    self.eax.saver(self.edx)
                    self.edx.free()
                elif attr[2] == self.edi.temp:
                    self.asm += ["movl %edi, %eax"]
                    self.eax.saver(self.edi)
                    self.edi.free()
                elif attr[2] in self.temp_dict:
                    self.asm += ["movl " + self.temp_dict[attr[2]] + ", %eax"]
                    self.eax.free()
                    self.eax.save(attr[2])
                elif attr[2] in self.st:
                    self.asm += ["movl " + str(self.st[attr[2]][2]) + "(%ebp), %eax"]
                    self.eax.save(attr[2], str(self.st[attr[2]][2]) + "(%ebp)")
                elif is_int(attr[2]):
                    self.asm += ["movl $" + str(attr[2]) + ", %eax"]
                elif attr[2] == self.eax.temp:
                    print("Already in eax!")
                else:
                    assert (False), "Should not be here!"


                op = self.op_map[attr[0]]

                if self.eax.temp == attr[3]:
                    self.asm += [op + " %eax, %eax"]
                elif self.ebx.temp == attr[3]:
                    self.asm += [op + " %ebx, %eax"]
                    self.ebx.free()
                elif self.edx.temp == attr[3]:
                    self.asm += [op + " %edx, %eax"]
                    self.edx.free()
                elif attr[3] in self.temp_dict:
                    if op == "imul":
                        self.asm += ["movl " + self.temp_dict[attr[3]] + ", %ebx", "imul %ebx, %eax"]
                    else:
                        self.asm += [op + " " + self.temp_dict[attr[3]] + ", %eax"]
                elif attr[3] in self.st:
                    self.asm += [op + " " + str(self.st[attr[3]][2]) + "(%ebp)" + ", %eax"]
                elif is_int(attr[3]):
                    self.asm += [op + " $" + str(attr[3]) + ", %eax"]
                else:
                    assert (False), "Should not be here!"

                self.eax.free()
                if attr[1] in self.st:
                    self.eax.save(attr[1], str(self.st[attr[1]][2]) + "(%ebp)")
                else:
                    self.eax.free()
                    self.eax.save(attr[1])

            elif attr[0] == "if" and attr[1] in self.rel_op:
                self.write_back()
                if self.eax.temp != None and self.eax.location == None and self.eax.temp != attr[2] and self.eax.temp != attr[3]:
                    if self.edx.temp != None and self.edx.location == None and self.edx.temp == attr[2]:
                        self.asm += ["movl %eax, %ebx", "movl %edx, %eax", "movl %ebx, %edx"]
                        self.ebx.saver(self.eax)
                        self.eax.saver(self.edx)
                        self.edx.saver(self.ebx)
                    elif self.edx.temp != None and self.edx.location == None:
                        self.asm += ["movl %edx, %edi"]
                        self.edi.saver(self.edx)
                        self.asm += ["movl %eax, %edx"]
                        self.edx.saver(self.eax)
                    else:
                        self.asm += ["movl %eax, %edx"]
                        self.edx.saver(self.eax)

                if self.eax.temp == attr[3]:
                    self.ebx.save(attr[3]) #should add the location
                    self.asm += ["movl %eax, %ebx"]

                if attr[2] == self.edx.temp:
                    self.asm += ["movl %edx, %eax"]
                    self.eax.saver(self.edx)
                    self.edx.free()
                elif attr[2] == self.edi.temp:
                    self.asm += ["movl %edi, %eax"]
                    self.eax.saver(self.edi)
                    self.edi.free()
                elif attr[2] in self.temp_dict:
                    self.asm += ["movl " + self.temp_dict[attr[2]] + ", %eax"]
                    self.eax.free()
                    self.eax.save(attr[2])
                elif attr[2] in self.st:
                    self.asm += ["movl " + str(self.st[attr[2]][2]) + "(%ebp), %eax"]
                    self.eax.save(attr[2], str(self.st[attr[2]][2]) + "(%ebp)")
                elif is_int(attr[2]):
                    self.asm += ["movl $" + str(attr[2]) + ", %eax"]
                elif attr[2] == self.eax.temp:
                    print("Already in eax!")
                else:
                    assert (False), "Should not be here!"


                op = self.rel_op[attr[1]]

                if self.eax.temp == attr[3]:
                    self.asm += ["cmp %eax, %eax", op + " " + attr[5]]
                elif self.ebx.temp == attr[3]:
                    self.asm += ["cmp %ebx, %eax", op + " " + attr[5]]
                    self.ebx.free()
                elif self.edx.temp == attr[3]:
                    self.asm += ["cmp %edx, %eax", op + " " + attr[5]]
                    self.edx.free()
                elif attr[3] in self.temp_dict:
                    self.asm += ["cmp " + self.temp_dict[attr[3]] + ", %eax", op + " " + attr[5]]
                elif attr[3] in self.st:
                    self.asm += ["cmp " + str(self.st[attr[3]][2]) + "(%ebp)" + ", %eax", op + " " + attr[5]]
                elif is_int(attr[3]):
                    self.asm += ["cmp $" + str(attr[3]) + ", %eax", op + " " + attr[5]]
                else:
                    assert (False), "Should not be here!"

                self.free_regs()
            else:
                assert (False), "Instruction not supported yet"
            print(i+1, attr, "eax", self.eax.temp, self.eax.location, "edx", self.edx.temp, self.edx.location, "edi", self.edi.temp, self.edi.location)
