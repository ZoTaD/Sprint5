from decimal import Decimal

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
        cadena=self.calle+ ", "+self.numero+ ", "+self.ciudad+ ", "+self.provincia+ ", "+self.pais
        print(cadena)

class Cliente(Cuenta, Direccion):
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni, **kwargs):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais)
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
    def cheq():
        return False
    def tarcred():
        return False
    def dolar():
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


a = Gold("12", "12.05", "100", "5", "2000", "Corrientes", "1270", "CABA", "Buenos Aires", "Argentina", "Pedro", "Rodriguez", "2235", "22065213", 1, 1)
a.out_dir()
print(a.limite_extraccion_diario, a.costo_transferencias, a.limite_transferencia_recibida, a.__class__.__name__, a.cheq(), a.tarcred())
