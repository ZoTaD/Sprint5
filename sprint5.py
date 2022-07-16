import json, cuentas, rechazos, sys

print("")

filename = str(sys.argv[1])

try:
    arc = open("./files/" + filename)
except:
    cuentas.salir("Error al abrir el archivo")   

try:
    arcparse = json.load(arc)
except:
    cuentas.salir("Error de procesado del archivo JSON")

rejectedt = {}

try:
    nombre = arcparse["nombre"]
    apellido = arcparse["apellido"]
    numeroc = arcparse["numero"]
    dni = arcparse["dni"]
    direccion = cuentas.Direccion(arcparse["direccion"]["calle"], arcparse["direccion"]["numero"], arcparse["direccion"]["ciudad"], arcparse["direccion"]["provincia"], arcparse["direccion"]["pais"])
    transacciones = arcparse["transacciones"]
except:
    cuentas.salir("Error de lectura del archivo JSON")

if arcparse["tipo"] == "CLASSIC":
    c = cuentas.Classic(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)
elif arcparse["tipo"] == "GOLD":
    c = cuentas.Gold(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)
elif arcparse["tipo"] == "BLACK":
    c = cuentas.Black(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)

for i in transacciones:
    try:
        if i["estado"] == "RECHAZADA":
            c.account.monto = i["saldoEnCuenta"]

            c.curtarcred = i["totalTarjetasDeCreditoActualmente"]

            c.curcheq = i["totalChequerasActualmente"]

            if i["tipo"] == "ALTA_CHEQUERA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecAltaChequera(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecRetEfec(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "ALTA_TARJETA_CREDITO":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecAltaTarcred(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "COMPRA_DOLAR":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecDolar(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "TRANSFERENCIA_RECIBIDA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecTranfRec(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "TRANSFERENCIA_ENVIADA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecTranfEnv(i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            print("Transacción", rejectedt[f"tr {i['numero']}"].tnum)
            rejectedt[f"tr {i['numero']}"].solve()
            print("-------")
        else:
            print("La transacción", i["numero"], "se encuentra aceptada")
            print("-------")
    except:
        cuentas.salir("Error de lectura del archivo JSON al recorrer el listado de transacciones")

arc.close()

print("")