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
        if op == 0x01: # LOAD
            self.reg[a] = self.mem[b]
        elif op == 0x02: # STORE
            self.mem[b] = self.reg[a]
        elif op == 0x03: # ADD
            self.reg[a] = (self.reg[a] + self.reg[b]) & 0xFF
        elif op == 0x04: # SUB
            self.reg[a] = (self.reg[a] - self.reg[b]) & 0xFF
        elif op == 0x05: # MOV
            self.reg[a] = b
        elif op == 0x06: # CMP
            self.zf = 1 if self.reg[a] == self.reg[b] else 0
        elif op == 0x07: # JMP
            self.pc = a
        elif op == 0x08: # JZ
            if self.zf == 1: self.pc = a
        elif op == 0x09: # JNZ
            if self.zf == 0: self.pc = a
        elif op == 0x0A: # HALT
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
        while self.running and self.pc < 256:
            self.ciclo += 1
            op, a, b = self.fetch()
            self.decode_execute(op, a, b)
            self.trace(op, a, b)

# --- INICIALIZAÇÃO GRUPO 4 ---
cpu = MiniCPU()

# Carregando os dados na memória (0x10 em diante)
dados = [12, 45, 7, 89, 23, 56, 3, 67]
for i in range(len(dados)):
    cpu.mem[0x10 + i] = dados[i]

# --- PROGRAMA ASSEMBLY ---
# Objetivo: Pegar o maior valor (89 que está no 0x13) e salvar no 0x20
i = 0
cpu.mem[i] = 0x01; cpu.mem[i+1] = 0; cpu.mem[i+2] = 0x13; i += 3 # LOAD R0, 0x13
cpu.mem[i] = 0x02; cpu.mem[i+1] = 0; cpu.mem[i+2] = 0x20; i += 3 # STORE R0, 0x20
cpu.mem[i] = 0x0A; cpu.mem[i+1] = 0; cpu.mem[i+2] = 0x00; i += 3 # HALT

print("Iniciando a MiniCPU...\n")
cpu.run()

print("\n--- VALIDAÇÃO GRUPO 4 ---")
print(f"Valor salvo no endereço 0x20: {cpu.mem[0x20]}")
if cpu.mem[0x20] == 89:
    print("Sucesso! O maior valor (89) foi gravado corretamente.")
else:
    print("Falha. O valor gravado está incorreto.")