from decimal import Decimal
import json

def salir(m):
    print(m)
    exit()

class Cuenta:
    def __init__(self, lime, limtr, mto, cost, sldd, **kwargs):
        super().__init__(**kwargs)
        self.limite_extraccion_diario = Decimal(lime)
        self.limite_transferencia_recibida = Decimal(limtr)
        self.monto = Decimal(mto)
        self.costo_transferencias = Decimal(cost)
        self.saldo_descubierto_disponible = Decimal(sldd)

class Direccion:
    def __init__(self, calle, num, ciudad, prov, pais, **kwargs):
        super().__init__(**kwargs)
        self.calle=calle
        self.numero=num
        self.ciudad=ciudad
        self.provincia=prov
        self.pais=pais
    def out_dir(self):
        print(f"Dirección: {self.pais}, {self.provincia}, {self.ciudad}, {self.calle}, {self.numero}")

class Cliente(Cuenta, Direccion):
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, **kwargs):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, **kwargs)
        self.nombre = nombre
        self.apellido = apellido
        self.numero_cliente= numc
        self.dni = dni

class Classic(Cliente):
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, curtarcred, curcheq):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        if curtarcred != 0:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else: self.curtarcred = curtarcred    
        if curcheq != 0:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self.curcheq = curcheq
    def cheq(self):
        return False
    def tarcred(self):
        return False
    def dolar(self):
        return False

class Gold(Cliente):
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, curtarcred, curcheq):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        if curtarcred < 0 or curtarcred > 1:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else: self.curtarcred = curtarcred    
        if curcheq < 0 or curcheq > 1:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self.curcheq = curcheq
    def cheq(self):
        if self.curcheq == 1:
            return False
        else:
            return True
    def tarcred(self):
        if self.curtarcred == 1:
            return False
        else:
            return True
    def dolar():
        return True

class Black(Cliente):
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, curtarcred, curcheq):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        if curtarcred < 0 or curtarcred > 5:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else: self.curtarcred = curtarcred    
        if curcheq < 0 or curcheq > 2:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self.curcheq = curcheq
    def cheq(self):
        if self.curcheq == 2:
            return False
        else:
            return True
    def tarcred(self):
        if self.curtarcred == 5:
            return False
        else:
            return True
    def dolar():
        return True

class Decline:
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        self.t = tipo
        self.cn = cuenta
        self.remaining = cupor
        self.m = monto
        self.date = date
        self.tnum = num
        self.s = saldo
        self.cliente = cliente
    def solve(self):
        print("Debe crearse un objeto del tipo de rechazo adecuado para poder utilizarse este método")

class DecAltaChequera(Decline):
    def __init__(self, tipo, cuenta, cupor, monto, date, num, saldo, cliente):
        super().__init__(tipo, cuenta, cupor, monto, date, num, saldo, cliente)
    def solve(self):
        if self.cliente.__class__.__name__ == "Classic":
            if not self.cliente.cheq():
                print("Transacción rechazada debido a que a cantidad de chequeras permitidas para esta cuenta ha sido alcanzada (las cuentas Classic no pueden tener chequeras)")
        elif self.cliente.__class__.__name__ == "Gold":
            if not self.cliente.cheq():
                print("Transacción rechazada debido a que la cantidad de chequeras permitidas para esta cuenta ha sido alcanzada (las cuentas Gold únicamente pueden tener una chequera)")
        elif self.cliente.__class__.__name__ == "Black":
            if not self.cliente.cheq():
                print("Transacción rechazada debido a que la cantidad de chequeras permitidas para esta cuenta ha sido alcanzada (las cuentas Black únicamente pueden tener hasta dos chequeras)")

a = Classic("12", "12.05", "100", "5", "2000", "Corrientes", "1270", "CABA", "Buenos Aires", "Argentina", "Pedro", "Rodriguez", "2235", "22065213", 0, 0)
a.out_dir()
print(a.limite_extraccion_diario, a.costo_transferencias, a.limite_transferencia_recibida, a.__class__.__name__, a.tarcred(), a.cheq())
print("")

arc = open("./test.json")
arcparse = json.load(arc)
trantype = []
for i in arcparse["transacciones"]:
    if i["estado"] == "RECHAZADA":
        trantype.append((i["numero"], i["tipo"]))
print(trantype)
arc.close()
print("")

rec = DecAltaChequera("ALTA_CHEQUERA", 190, 3000, 9000, "10/10/2022 16:00:55", 2, 100000, a)
rec.solve()