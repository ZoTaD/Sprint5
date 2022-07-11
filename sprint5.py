from decimal import Decimal

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
    def __init__(self, lime, limtr, mto, cost, sldd, calle, num, ciudad, prov, pais, nombre, apellido, numc, dni):
        super().__init__(lime = lime, limtr = limtr, mto = mto, cost = cost, sldd = sldd, calle = calle, num = num, ciudad = ciudad, prov = prov, pais = pais)
        self.nombre = nombre
        self.apellido = apellido
        self.numero_cliente= numc
        self.dni = dni

a = Cliente("12", "12.05", "100", "5", "2000", "Corrientes", "1270", "CABA", "Buenos Aires", "Argentina", "Pedro", "Rodriguez", "2235", "22065213")
a.out_dir()
print(a.limite_extraccion_diario, a.costo_transferencias, a.limite_transferencia_recibida)