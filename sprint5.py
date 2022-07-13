from cmath import inf
from decimal import Decimal
import json
from msilib.schema import Property


def salir(m):
    print(m)
    exit()

class Cuenta:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limite_extraccion_diario = None
        self.limite_transferencia_recibida = None
        self.monto = None
        self.costo_transferencias = None
        self.saldo_descubierto_disponible = None

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
    def __init__(self, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, **kwargs):
        super().__init__(calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, **kwargs)
        self.nombre = nombre
        self.apellido = apellido
        self.numero_cliente= numc
        self.dni = dni

class Classic(Cliente):
    def __init__(self, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni):
        super().__init__(calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        self.limite_extraccion_diario = Decimal("10000")
        self.limite_transferencia_recibida = Decimal("150000")
        self.costo_transferencias = Decimal("0.01")
        self.saldo_descubierto_disponible = Decimal("0")
    
    @property
    def curtarcred(self):
        return self._curtarcred
    @curtarcred.setter
    def curtarcred(self, ctc):
        if ctc != 0:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else:
            self._curtarcred = ctc 

    @property
    def curcheq(self):
            return self._curcheq
    @curcheq.setter
    def curcheq(self, crc):
        if crc != 0:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self._curcheq = crc

    def cheq(self):
        return False

    def tarcred(self):
        return False

    def dolar(self):
        return False

class Gold(Cliente):
    def __init__(self, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni):
        super().__init__(calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        self.limite_extraccion_diario = Decimal("20000")
        self.limite_transferencia_recibida = Decimal("500000")
        self.costo_transferencias = Decimal("0.005")
        self.saldo_descubierto_disponible = Decimal("10000")

    @property
    def curtarcred(self):
        return self._curtarcred
    @curtarcred.setter
    def curtarcred(self, ctc):
        if ctc < 0 or ctc > 1:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else:
            self._curtarcred = ctc 

    @property
    def curcheq(self):
            return self._curcheq
    @curcheq.setter
    def curcheq(self, crc):
        if crc < 0 or crc > 1:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self._curcheq = crc

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
    def __init__(self, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni):
        super().__init__(calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais, nombre = nombre, apellido = apellido, numc = numc, dni = dni)
        self.limite_extraccion_diario = Decimal("100000")
        self.costo_transferencias = Decimal("0")
        self.saldo_descubierto_disponible = Decimal("10000")

    @property
    def curtarcred(self):
        return self._curtarcred
    @curtarcred.setter
    def curtarcred(self, ctc):
        if ctc < 0 or ctc > 5:
            salir("Error de cuenta: cantidad de tarjetas de crédito imposible")
        else:
            self._curtarcred = ctc 

    @property
    def curcheq(self):
            return self._curcheq
    @curcheq.setter
    def curcheq(self, crc):
        if crc < 0 or crc > 2:
            salir("Error de cuenta: cantidad de chequeras imposible")
        else:
            self._curcheq = crc

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

print("")

arc = open("./test.json")

arcparse = json.load(arc)

rejectedt = {}

if arcparse["tipo"] == "CLASSIC":
    c = Classic(None, None, None, None, None, arcparse["nombre"], arcparse["apellido"], arcparse["numero"], arcparse["DNI"])
elif arcparse["tipo"] == "GOLD":
    c = Gold(None, None, None, None, None, arcparse["nombre"], arcparse["apellido"], arcparse["numero"], arcparse["DNI"])
elif arcparse["tipo"] == "BLACK":
    c = Black(None, None, None, None, None, arcparse["nombre"], arcparse["apellido"], arcparse["numero"], arcparse["DNI"])

for i in arcparse["transacciones"]:
    if i["estado"] == "RECHAZADA":
        c.monto = i["saldoEnCuenta"]

        c.curtarcred = i["totalTarjetasDeCreditoActualmente"]
        print(c.curtarcred, "tarjetas de crédito")

        c.curcheq = i["totalChequerasActualmente"]
        print(c.curcheq, "chequeras")
        
        trnum = i["numero"]

        if i["tipo"] == "ALTA_CHEQUERA":
            rejectedt[f"tr {trnum}"] = DecAltaChequera(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            print("transacción", rejectedt[f"tr {trnum}"].tnum)
            rejectedt[f"tr {trnum}"].solve()
    else:
        print("La transacción", i["numero"], "se encuentra aceptada")

arc.close()

print("")