import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        self.reg = [None] * 8 # R0-R7
        self.ram = [idx + 1 for idx, val in enumerate([None] * 255)]

    def ram_read(self, MAR): # Memory Address Register
        # get the value at ram location
        return self.ram[MAR]

    def reg_write(self, MAR, MDR): # Memory Data Register
        # write over a specified location in ram
        reg_ptr = self.reg[self.ram[MAR]]
        reg_ptr = self.ram[MDR]
        print(f"LS8 WRITE: ram[{self.ram[MAR]}] = {self.ram[MAR]}")

    def reg_read(self, MAR): # Memory Address Register
        # get the value at ram location
        return self.reg[self.ram[MAR]]

    def reg_write(self, MAR, MDR): # Memory Data Register
        # write over a specified location in ram
        self.reg[self.ram[MAR]] = self.ram[MDR]
        print(f"LS8 WRITE: reg[{self.ram[MAR]}] = {self.reg[self.ram[MAR]]}")

    def load(self, program):
        """Load a program into memory."""
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

    def run(self):
        """Run the CPU."""
        pc = 0  # Program Counter, address of the currently-executing instuction
        running = True
        while running:
            ir = self.ram[pc]  # Instruction Register, copy of the currently-executing instruction

            # LDI
            if ir == 130:
                self.reg_write(pc+1, pc+2)
                pc += 3
            # PRN
            elif ir == 71:
                print(f"LS8 PRN: {self.reg_read(pc + 1)}")
                pc += 2
            # HLT
            elif ir == 1: running = False
            # ???
            else: 
                print(f"Unknown instruction: \"{ir}\"")
                running = False
