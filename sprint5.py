import json, cuentas, rechazos, sys, codecs

filename = str(sys.argv[1])
err = ""
keep = True

if len(sys.argv) != 2:
    err+= "Cantidad de argumentos inadecuada al llamar al script"
    keep = False

try:
    arc = open("./files/" + filename)
except:
    err += "Error al abrir el archivo JSON"
    keep = False   

if keep:
    try:
        arcparse = json.load(arc)
    except:
        err += "Error de procesado del archivo JSON"
        keep = False

rejectedt = {}
if keep:
    try:
        nombre = arcparse["nombre"]
        apellido = arcparse["apellido"]
        numeroc = arcparse["numero"]
        dni = arcparse["dni"]
        direccion = cuentas.Direccion(arcparse["direccion"]["calle"], arcparse["direccion"]["numero"], arcparse["direccion"]["ciudad"], arcparse["direccion"]["provincia"], arcparse["direccion"]["pais"])
        transacciones = arcparse["transacciones"]
    except:
        err += "Error de lectura del archivo JSON"
        keep = False

if keep:
    try:
        if arcparse["tipo"] == "CLASSIC":
            c = cuentas.Classic(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)
        elif arcparse["tipo"] == "GOLD":
            c = cuentas.Gold(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)
        elif arcparse["tipo"] == "BLACK":
            c = cuentas.Black(nombre, apellido, numeroc, dni, cuentas.Cuenta(), direccion)
    except:
        err += "Error de lectura de los datos del cliente"
        keep = False

if keep:
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
            #print("Transacción", rejectedt[f"tr {i['numero']}"].tnum)
            rejectedt[f"tr {i['numero']}"].solve()
            #print("-------")  
        except:
            err += "Error de lectura del archivo JSON al recorrer el listado de transacciones"

if keep:
    arc.close()

    clientname=f"    <h1 class='text-center titleformat text-light'>Transacciones de: {nombre} {apellido}</h1>\n"
    htmllines=""

for i in rejectedt.values():
    ttype = ""
    for w in i.t.split("_"):
        ttype+=f"{w} "
    e = f'              <tr><th scope="row">{i.tnum}</th><td>{ttype.capitalize()}</td><td>{i.date}</td><td>{i.state.capitalize()}</td><td>{i.solve()}</td></tr>\n'  
    htmllines += e

try:
    tablatemp = codecs.open("./res/template.html", "r", "utf-8")
    filelines = tablatemp.readlines()
    tablatemp.close()
    if err == "":
        filelines[10] = clientname
        filelines[23] = htmllines
        print(err)
    else:
        filelines[10] ='<h1 class="text-center titleformat text-light">Error</h1>\n'
        filelines[23] = f'            <tr><th scope="row">*</th><td>{err}</td>\n'
    tabla = codecs.open("./output/reporte.html", "w", "utf-8")
    tabla.writelines(filelines)
    tabla.close()
except:
    cuentas.salir("Error al crear el archivo.")

