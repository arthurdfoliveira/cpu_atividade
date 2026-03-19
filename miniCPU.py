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
        
    def run(self):
        while self.running:
            op, a, b = self.fetch()
            self.trace(op, a, b)
            self.decode_execute(op, a, b)
            self.ciclo += 1



if __name__ == "__main__":
    cpu = MiniCPU()
    # Programa de exemplo: R0 = 5, R1 = 10, R2 = R0 + R1, HALT
    programa = [
        0x05, 0x00, 0x05,  # MOV R0, 5
        0x05, 0x01, 0x0A,  # MOV R1, 10
        0x03, 0x02, 0x00,  # ADD R2, R0
        0x03, 0x02, 0x01,  # ADD R2, R1
        0x0A, 0x00, 0x00   # HALT
    ]
    cpu.mem[:len(programa)] = programa
    cpu.run()


# class MiniCPU:
#     def __init__(self):
#         self.mem = [0] * 256
#         self.reg = [0, 0, 0, 0]
#         self.pc = 0
#         self.zf = 0
#         self.running = True
#         self.ciclo = 0

#     def fetch(self):

#         op = self.mem[self.pc]
#         a = self.mem[self.pc + 1]
#         b = self.mem[self.pc + 2]
#         self.pc += 3
#         return op, a, b

#     def decode_execute(self, op, a, b):
        
#         if op == 0x01: # LOAD: Pega da memória e põe no registrador [cite: 35]
#             self.reg[a] = self.mem[b]
#         elif op == 0x02: # STORE: Pega do registrador e guarda na memória [cite: 35]
#             self.mem[b] = self.reg[a]
#         elif op == 0x05: # MOV: Coloca um número direto na mão [cite: 35]
#             self.reg[a] = b
#         elif op == 0x06: # CMP: Compara as duas mãos (levanta bandeira se igual) [cite: 35]
#             self.zf = 1 if self.reg[a] == self.reg[b] else 0
#         elif op == 0x07: # JMP: Pula para outro lugar do mapa [cite: 35]
#             self.pc = a
#         elif op == 0x0A: # HALT: Para tudo e vai dormir [cite: 35]
#             self.running = False

#     def trace(self, op, a, b):
        
#         nomes = {1:'LOAD', 2:'STORE', 5:'MOV', 6:'CMP', 7:'JMP', 10:'HALT'}
#         nome_op = nomes.get(op, '???')
#         print(f"Ciclo {self.ciclo}: {nome_op} ({a}, {b}) | R0={self.reg[0]} R1={self.reg[1]} | PC={self.pc} ZF={self.zf}")

#     def run(self):
        
#         while self.running and self.pc < 256:
#             self.ciclo += 1
#             op, a, b = self.fetch()
#             self.decode_execute(op, a, b)
#             self.trace(op, a, b)

# cpu = MiniCPU()

 

# valores_teste = [12, 45, 7, 89, 23, 56, 3, 67]
# for i, valor in enumerate(valores_teste):
#     cpu.mem[0x10 + i] = valor

# cpu.mem[0] = 0x01; cpu.mem[1] = 0; cpu.mem[2] = 0x10 # LOAD R0, [0x10]

# cpu.mem[3] = 0x01; cpu.mem[4] = 1; cpu.mem[5] = 0x11 # LOAD R1, [0x11]

# cpu.mem[6] = 0x02; cpu.mem[7] = 0; cpu.mem[8] = 0x20 # STORE R0, [0x20]
# cpu.mem[9] = 0x0A; cpu.mem[10] = 0; cpu.mem[11] = 0 # HALT

# print("Iniciando Simulação do Grupo 4 (Máximo do Array):")
# cpu.run()
# print(f"\nResultado no pote 0x20 (Memória[32]): {cpu.mem[0x20]}")