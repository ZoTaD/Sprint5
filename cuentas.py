from decimal import Decimal

def salir(m):
    print(m)
    exit()

class Cuenta:
    def __init__(self):
        self.limite_extraccion_diario = None
        self.limite_transferencia_recibida = None
        self.monto = None
        self.costo_transferencias = None
        self.saldo_descubierto_disponible = None

class Direccion:
    def __init__(self, calle, num, ciudad, prov, pais):
        self.calle=calle
        self.numero=num
        self.ciudad=ciudad
        self.provincia=prov
        self.pais=pais
    def out_dir(self):
        print(f"Dirección: {self.pais}, {self.provincia}, {self.ciudad}, {self.calle}, {self.numero}")

class Cliente:
    def __init__(self, nombre, apellido, numc, dni, cuenta, direccion):
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.numero_cliente= numc
        self.dni = dni
        self.cuenta=cuenta
        self.direccion=direccion

class Classic(Cliente):
    def __init__(self, nombre, apellido, numc, dni, cuenta, dir):
        super().__init__(nombre = nombre, apellido = apellido, numc = numc, dni = dni, cuenta = cuenta, direccion = dir)
        self.account = cuenta
        self.direc = dir
        self.account.limite_extraccion_diario = Decimal("10000")
        self.account.limite_transferencia_recibida = Decimal("150000")
        self.account.costo_transferencias = Decimal("0.01")
        self.account.saldo_descubierto_disponible = Decimal("0")
    
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
    def __init__(self, nombre, apellido, numc, dni, cuenta, dir):
        super().__init__(nombre = nombre, apellido = apellido, numc = numc, dni = dni, cuenta = cuenta, direccion = dir)
        self.account = cuenta
        self.direc = dir
        self.account.limite_extraccion_diario = Decimal("20000")
        self.account.limite_transferencia_recibida = Decimal("500000")
        self.account.costo_transferencias = Decimal("0.005")
        self.account.saldo_descubierto_disponible = Decimal("10000")
        

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

    def dolar(self):
        return True

class Black(Cliente):
    def __init__(self, nombre, apellido, numc, dni, cuenta, dir):
        super().__init__(nombre = nombre, apellido = apellido, numc = numc, dni = dni, cuenta = cuenta, direccion = dir)
        self.account = cuenta
        self.direc = dir
        self.account.limite_extraccion_diario = Decimal("100000")
        self.account.limite_transferencia_recibida = None
        self.account.costo_transferencias = Decimal("0")
        self.account.saldo_descubierto_disponible = Decimal("10000")
        

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
    def dolar(self):
        return True