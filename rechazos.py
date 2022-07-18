from decimal import Decimal

class Decline:
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        self.state = estado
        self.t = tipo
        self.cn = cuenta
        self.remaining = Decimal(cupor)
        self.m = Decimal(monto)
        self.date = date
        self.tnum = num
        self.s = Decimal(saldo)
        self.cliente = cliente
    def solve(self):
        return "Debe crearse un objeto del tipo de rechazo adecuado para poder utilizarse este método"

class DecAltaChequera(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.cheq():
            return "Cantidad máxima de chequeras permitidas alcanzada"
        else:
                return "Transacción aceptada"

class DecAltaTarcred(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.tarcred():
            return "Cantidad máxima de tarjetas de crédito permitidas alcanzada"
        else:
                return "Transacción aceptada"

class DecDolar(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if not self.cliente.dolar():
            return "Las cuentas classic no pueden comprar dólares"
        else:
            if self.m > self.s:
                return "Monto mayor a saldo en cuenta"
            else:
                return "Transacción aceptada"
                    

class DecRetEfec(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if (self.s + self.cliente.account.saldo_descubierto_disponible) < self.m:  
            return "Monto mayor a saldo en cuenta"
        elif self.m > self.remaining:
            return "Monto mayor a límite de extracción diario restante"
        else:
            return "Transacción aceptada"

class DecTranfRec(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if self.cliente.account.limite_transferencia_recibida:
            if self.cliente.account.limite_transferencia_recibida <= self.m:
                return f"Monto mayor al límite de transferencias recibidas para las cuentas de tipo {self.cliente.__class__.__name__}"
            else:
                return "Transacción aceptada"
        else:
            return "Transacción aceptada"

class DecTranfEnv(Decline):
    def __init__(self, estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(estado, tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if (self.m + self.m * self.cliente.account.costo_transferencias) > (self.s + self.cliente.account.saldo_descubierto_disponible):
            if self.cliente.__class__.__name__ == "BLACK":
                return "Monto mayor a saldo en cuenta más descubierto disponible"
            elif self.cliente.__class__.__name__ == "GOLD":
                "Monto y comisión mayores a saldo en cuenta más descubierto disponible"
            else:
                return "Monto y comisión mayores a saldo en cuenta"
        else:
            return "Transacción aceptada"