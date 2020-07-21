"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.instructions = {
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b10100010: "MUL",
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
                command = line[:8]
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
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        ir = self.pc

        running = True
        while running:
            command = self.ram[ir]
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)
            if self.instructions[command] == "HLT":
                running = False
            if self.instructions[command] == "LDI":
                self.reg[operand_a] = operand_b
                ir += 1 + (command >> 6)
            if self.instructions[command] == "PRN":
                print(self.reg[operand_a])
                ir += 1 + (command >> 6)
            if self.instructions[command] == "MUL":
                self.alu("MUL", operand_a, operand_b)
                ir += 1 + (command >> 6)
