from decimal import Decimal

class Decline:
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        self.t = tipo
        self.cn = cuenta
        self.remaining = Decimal(cupor)
        self.m = Decimal(monto)
        self.date = date
        self.tnum = num
        self.s = Decimal(saldo)
        self.cliente = cliente
    def solve(self):
        print("Debe crearse un objeto del tipo de rechazo adecuado para poder utilizarse este método")

class DecAltaChequera(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.cheq():
            print("Transacción rechazada debido a que la cantidad de chequeras permitidas para esta cuenta ha sido alcanzada")

class DecAltaTarcred(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.tarcred():
            print("Transacción rechazada debido a que a cantidad de tarjetas de crédito permitidas para esta cuenta ha sido alcanzada")

class DecDolar(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.dolar():
            print("Transacción rechazada debido a que las cuentas classic no pueden comprar dólares")
        else:
            if self.m > self.s:
                print("Transacción rechazada por monto mayor a saldo en cuenta")

class DecRetEfec(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if (self.s + self.cliente.account.saldo_descubierto_disponible) < self.m:  
            print("Transacción rechazada por monto mayor a saldo en cuenta")
        elif self.m > self.remaining:
            print("Transacción rechazada por monto mayor a límite de extracción diario")    

class DecTranfRec(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if self.cliente.account.limite_transferencia_recibida:
            if self.cliente.account.limite_transferencia_recibida <= self.m:
                print("Transacción rechazada debido a que el monto es mayor al límite de transferencias recibidas para las cuentas de tipo", self.cliente.__class__.__name__)

class DecTranfEnv(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if (self.m + self.m * self.cliente.account.costo_transferencias) > (self.s + self.cliente.account.saldo_descubierto_disponible):
            print("Transacción rechazada debido a que el monto y la comisión (de aplicarse) son mayores al saldo en cuenta (incluyendo descubierto en caso de tenerse)")