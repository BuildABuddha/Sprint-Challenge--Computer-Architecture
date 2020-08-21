"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUS = 0b01000101
POP = 0b01000110
ADD = 0b10100000
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7  # Stack Pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0XF4

        self.L = 0 # Flag for "Less than", set to 0 or 1 boolean
        self.G = 0 # Flag for "Greater than" set to 0 or 1 boolean
        self.E = 0 # Flag for "Equal to" set to 0 or 1 boolean

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        if filename:
            with open(filename, 'r') as infile:
                lines = infile.readlines()

                for line in lines:
                    line = line.strip()
                    # Ignore blank lines and comments (lines that start with #):
                    if line and line[0] != '#':
                        line = line.split('#')[0].strip()  # Ignore text after # characters
                        line = int(line, 2)  # Cast to binary instruction
                        program.append(line)

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
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

    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, location, value):
        self.ram[location] = value

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            instruction = self.ram_read(self.pc)

            if instruction is HLT:
                running = False

            elif instruction is LDI:
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3

            elif instruction == ADD:
                pass

            elif instruction == PRN:
                register_num = self.ram_read(self.pc + 1)
                print(self.reg[register_num])
                self.pc += 2

            elif instruction == MUL:
                self.alu(MUL, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3

            elif instruction == PUS:
                reg_index = self.ram_read(self.pc + 1)
                val = self.reg[reg_index]
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], val)
                self.pc += 2

            elif instruction == POP:
                reg_index = self.ram_read(self.pc + 1)
                val = self.ram[self.reg[SP]]
                self.reg[SP] += 1
                self.reg[reg_index] = val
                self.pc += 2

            elif instruction == CALL:
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], self.pc +2)
                self.pc = self.reg[self.ram_read(self.pc + 1)]

            elif instruction == RET:
                self.pc = self.ramread(self.reg[SP])
                self.reg[SP] += 1

            elif instruction == CMP:
                self.alu(CMP, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3

            elif instruction == JMP:
                self.pc = self.reg[self.ram_read(self.pc + 1)]

            elif instruction == JEQ:
                if self.E == 1:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.E == 0:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2
            
