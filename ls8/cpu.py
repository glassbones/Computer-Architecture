import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        self.pc = 0 # Program Counter, address of the currently-executing instuction
        self.reg = [0, 0, 0, 0, 0, 0, 0, 244] # R0-R7
        self.sp = self.reg[7]
        self.ram = [idx + 1 for idx, val in enumerate([None] * 255)]
        self.running = True 
        self.branchtable = {
            0b10100000: self.ADD,       # 160
            0b10101000: self.AND,       # 168
            0b01010000: self.CALL_REG,  # 80
            0b10100111: self.CMP,       # 167
            0b01100110: self.DEC,       # 102
            0b10100011: self.DIV,       # 163
            0b00000001: self.HLT,       # 1
            0b01100101: self.INC,       # 101
            0b01010010: self.INT,       # 82
            0b00010011: self.IRET,      # 19
            0b01010101: self.JEQ,       # 85
            0b01011010: self.JGE,       # 90
            0b01010111: self.JGT,       # 87
            0b01011001: self.JLE,       # 89
            0b01011000: self.JLT,       # 88
            0b01010100: self.JMP,       # 84
            0b01010110: self.JNE,       # 86
            0b10000010: self.LDI,       # 130
            0b10100100: self.MOD,       # 164
            0b10100010: self.MUL,       # 162
            0b00000000: self.NOP,       # 0
            0b01101001: self.NOT,       # 105
            0b10101010: self.OR,        # 170
            0b01000110: self.POP,       # 70
            0b01001000: self.PRA,       # 72
            0b01000111: self.PRN,       # 71
            0b01000101: self.PUSH,      # 69
            0b00010001: self.RET,       # 17
            0b10101100: self.SHL,       # 172
            0b10101101: self.SHR,       # 173
            0b10000100: self.ST,        # 132
            0b10100001: self.SUB,       # 161
            0b10101011: self.XOR        # 171
        }

    def ram_read(self, MAR): # Memory Address Register
        # get the value at ram location
        return self.ram[MAR]

    def ram_write(self, arg): # Memory Data Register
        # write over a specified location in ram

        ram_loc = self.ram[arg[0]] # ram location
        val = self.ram[arg[1]] # value

        ram_loc = val
        print(f"[WRITE] Address: ram[{arg[0]}] Value: {ram_loc}")

    # Get a reg value from reg location
    def reg_read(self, idx):
        return self.reg[self.ram[idx]]
        
    # Load a program into memory.
    def load(self, program):
        for idx, value in enumerate(program): self.ram[idx] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def get_arg(self, ir):
        if ir >> 6 == 2: return [self.pc + 1, self.pc + 2]
        elif ir >> 6 == 1: return self.pc + 1
        else: return 0


    def ADD(self):
        pass
    def AND(self):
        pass
    def CALL_REG(self):
        pass
    def CMP(self):
        pass
    def DEC(self):
        pass
    def DIV(self):
        pass

    def HLT(self, arg): self.running = False

    def INC(self):
        pass
    def INT(self):
        pass
    def IRET(self):
        pass
    def JEQ(self):
        pass
    def JGE(self):
        pass
    def JGT(self):
        pass
    def JLE(self):
        pass
    def JLT(self):
        pass
    def JMP(self):
        pass
    def JNE(self):
        pass

    # Set a reg value
    def LDI(self, arg):
        reg_idx = self.ram[arg[0]] # address in reg
        val = self.ram[arg[1]] # value

        self.reg[reg_idx] = val
        print(f"[WRITE] Address: reg[{reg_idx}] Value: {self.reg[reg_idx]}")

    def MOD(self):
        pass
    def MUL(self):
        pass
    def NOP(self):
        pass
    def NOT(self):
        pass
    def OR(self):
        pass
    def POP(self, arg):
        # sp is the value you want to put into the register
        value = self.ram[self.sp]
        # opA is the register you want to store into
        self.reg[arg] = value
        self.sp += 1
        self.pc += 1
    def PRA(self):
        pass

    def PRN(self, arg): print(f"[PRN] Address: reg[{self.ram[arg]}] Value: {self.reg_read(arg)}")

    def PUSH(self, arg):
        # decrement stack pointer
        self.sp -= 1
        # copy the value to the SP address
        self.ram[self.sp] = self.reg[arg]
        # increment program counter
        self.pc += 1
        
    def RET(self):
        pass
    def SHL(self):
        pass
    def SHR(self):
        pass
    def ST(self):
        pass
    def SUB(self):
        pass
    def XOR(self):
        pass

    

    

    def run(self):
        """Run the CPU."""
        
        while self.running:

            ir = self.ram[self.pc]  # Instruction Register, copy of the currently-executing instruction
            arg = self.get_arg(ir)

            if ir in self.branchtable: self.branchtable[ir](arg)
            else:
                print(f"Unknown instruction: \"{ir}\"")
                running = False

            # skip arguments and go to next instruction
            self.pc += ( ir >> 6 ) + 1
    
    