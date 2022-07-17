import json, cuentas, rechazos, sys, codecs
from simple_html.nodes import body, head, html, p, tr, td, tbody, th
from simple_html.render import render

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
            c.account.monto = i["saldoEnCuenta"]

            c.curtarcred = i["totalTarjetasDeCreditoActualmente"]

            c.curcheq = i["totalChequerasActualmente"]

            if i["tipo"] == "ALTA_CHEQUERA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecAltaChequera(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecRetEfec(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "ALTA_TARJETA_CREDITO":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecAltaTarcred(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "COMPRA_DOLAR":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecDolar(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "TRANSFERENCIA_RECIBIDA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecTranfRec(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            elif i["tipo"] == "TRANSFERENCIA_ENVIADA":
                rejectedt[f"tr {i['numero']}"] = rechazos.DecTranfEnv(i["estado"], i["tipo"], i["cuentaNumero"], i["cupoDiarioRestante"], i["monto"], i["fecha"], i["numero"], i["saldoEnCuenta"], c)
            print("Transacción", rejectedt[f"tr {i['numero']}"].tnum)
            rejectedt[f"tr {i['numero']}"].solve()
            print("-------")
        
    except:
        cuentas.salir("Error de lectura del archivo JSON al recorrer el listado de transacciones")

arc.close()

print("")

clientname=f"<h1>Transacciones de: {nombre} {apellido}</h1>"
htmllines=""

for i in rejectedt.values():
    node = tr(
    th.attrs(scope="row")(
        f"{i.tnum}"
    ),
    td(
        f"{i.state}"
    ),
    td(
        f"{i.date}"
    ),
    td(
        f"{i.t}"
    ),
    td(
        f"{i.solve()}"
    )
    )
    htmllines += f"              {render(node)}\n"

tablatemp = codecs.open("./files/template.html", "r", "utf-8")
filelines = tablatemp.readlines()
filelines[22] = htmllines
filelines[9] = clientname
tablatemp.close()

tabla = codecs.open("prueba.html", "w", "utf-8")
tabla.writelines(filelines)
tabla.close()
