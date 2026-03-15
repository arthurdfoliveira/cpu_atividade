class MiniCPU:
    def __init__(self):
        self.mem = [0] * 256
        self.reg = [0, 0, 0, 0]
        self.pc = 0
        self.zf = 0
        self.running = True
        self.ciclo = 0

    def fetch(self):
        op = self.mem[self.pc]
        a = self.mem[self.pc + 1]
        b = self.mem[self.pc + 2]
        self.pc += 3
        return op, a, b

    def decode_execute(self, op, a, b):
        if op == 0x01:
            self.reg[a] = self.mem[b]
        elif op == 0x02:
            self.mem[b] = self.reg[a]
        elif op == 0x03:
            self.reg[a] = (self.reg[a] + self.reg[b]) & 0xFF
        elif op == 0x04:
            self.reg[a] = (self.reg[a] - self.reg[b]) & 0xFF
        elif op == 0x05:
            self.reg[a] = b
        elif op == 0x06:
            self.zf = 1 if self.reg[a] == self.reg[b] else 0
        elif op == 0x07:
            self.pc = a
        elif op == 0x08:
            if self.zf == 1: self.pc = a
        elif op == 0x09:
            if self.zf == 0: self.pc = a
        elif op == 0x0A:
            self.running = False

    def trace(self, op, a, b):
        nomes = {
            0x01: 'LOAD', 0x02: 'STORE', 0x03: 'ADD',
            0x04: 'SUB',  0x05: 'MOV',   0x06: 'CMP',
            0x07: 'JMP',  0x08: 'JZ',    0x09: 'JNZ',
            0x0A: 'HALT'
        }
        nome = nomes.get(op, '???')
        print(f"Ciclo {self.ciclo}: {nome:5s} {a},{b} | "
              f"R0={self.reg[0]:3d} R1={self.reg[1]:3d} "
              f"R2={self.reg[2]:3d} R3={self.reg[3]:3d} | "
              f"PC={self.pc:3d} ZF={self.zf}")