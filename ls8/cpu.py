"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.instructions = {
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b10100000: "ADD",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01010000: "CALL",
            0b00010001: "RET",
            0b10100111: "CMP",
            0b01010100: "JMP",
            0b01010101: "JEQ",
            0b01010110: "JNE",
        }
        try:
            self.file = sys.argv[1]
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file not found")

    def load(self):
        """Load a program into memory."""

        address = 0
        with open(self.file) as file:
            for line in file:
                command = line.split("#")[0]
                if command == "":
                    continue
                instruction = int(command, 2)
                self.ram[address] = instruction
                address += 1

    def ram_read(self, mar):
        self.mar = mar
        return self.ram[self.mar]

    def ram_write(self, mar, mdr):
        self.mar = mar
        self.mdr = mdr
        self.ram[self.mar] = self.mdr

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def jump(self):
        self.pc = self.reg[self.operand_a]

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.ram[self.pc]
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2)
            self.pc += 1 + (command >> 6)
            if self.instructions[command] == "HLT":
                running = False
            if self.instructions[command] == "LDI":
                self.reg[self.operand_a] = self.operand_b
            if self.instructions[command] == "PRN":
                print(self.reg[self.operand_a])
            if self.instructions[command] == "MUL":
                self.alu("MUL", self.operand_a, self.operand_b)
            if self.instructions[command] == "ADD":
                self.alu("ADD", self.operand_a, self.operand_b)
            if self.instructions[command] == "PUSH":
                self.reg[7] -= 1
                self.ram_write(self.reg[7], self.reg[self.operand_a])
            if self.instructions[command] == "POP":
                self.reg[self.operand_a] = self.ram_read(self.reg[7])
                self.reg[7] += 1
            if self.instructions[command] == "CALL":
                self.reg[7] -= 1
                self.ram_write(self.reg[7], self.pc)
                self.pc = self.reg[self.operand_a]
            if self.instructions[command] == "RET":
                ret_address = self.ram_read(self.reg[7])
                self.reg[7] += 1
                self.pc = ret_address
            if self.instructions[command] == "CMP":
                self.alu("CMP", self.operand_a, self.operand_b)
            if self.instructions[command] == "JMP":
                self.jump()
            if self.instructions[command] == "JEQ":
                if self.fl == 0b00000001:
                    self.jump()
            if self.instructions[command] == "JNE":
                if self.fl & 0b00000001 == 0:
                    self.jump()
