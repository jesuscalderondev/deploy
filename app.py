from flask import Flask, jsonify, render_template, redirect, request, send_file
from DATABASE import *
from datetime import datetime
import time
from PDFGASTO import PDFGASTO
app = Flask("SERVIDOR PRIVAO")


@app.route('/')
def principal():
    return render_template('base.html')


@app.route('/contabilidad')
def contabilida():
    return render_template('catalogo_cuentas.html')

# Gastos


@app.route('/alta_gastos')
def alta_gastos():
    return render_template('alta_gastos.html', poliza=session.query(func.coalesce(func.max(ComprasGeneral.NO_POLIZA)+1, 1)).scalar(), proveedores=session.query(CatalogoCuentasEstandar).filter(or_(CatalogoCuentasEstandar.ORIGEN == '2120-000-000', CatalogoCuentasEstandar.ORIGEN == '2110-000-000'), CatalogoCuentasEstandar.CUENTA != '').order_by(
        CatalogoCuentasEstandar.DESCRIPCION.asc()).all(), registros=session.query(ComprasDetalleTemporal).all())


@app.route('/api/forma_pago/<string:forma>', methods=['GET'])
def api_forma_pago(forma):
    lista = []
    cuentas_obj = []
    if forma == "EFECTIVO":
        cuentas_obj = session.query(CatalogoCuentasEstandar).filter(
            CatalogoCuentasEstandar.ORIGEN == '1110-000-000', CatalogoCuentasEstandar.NIVEL == 2).all()
    elif forma == "TARJETA CREDITO":
        cuentas_obj = session.query(CatalogoCuentasEstandar).filter(
            CatalogoCuentasEstandar.ORIGEN == "2120-000-000", CatalogoCuentasEstandar.BANCARIO == "Si").all()
    elif forma in ['TARJETA DEBITO', 'TRANSFERENCIA', 'CHEQUE']:
        cuentas_obj = cuentas_obj = session.query(CatalogoCuentasEstandar).filter(
            CatalogoCuentasEstandar.ORIGEN == "1120-000-000", CatalogoCuentasEstandar.DESCRIPCION != "Bancos").all()
    for i in cuentas_obj:
        lista.append(i.DESCRIPCION)
    return jsonify(lista)


@app.route('/api/concepto/<string:concepto>', methods=['GET'])
def api_concepto(concepto):
    lista = []
    lista_gastos_generales = session.query(CatalogoCuentasEstandar).filter(
        CatalogoCuentasEstandar.ORIGEN == "6100-000-000", CatalogoCuentasEstandar.CUENTA != " ").all()
    lista_otros_generales = session.query(CatalogoCuentasEstandar).filter(
        CatalogoCuentasEstandar.ORIGEN == "7400-000-000", CatalogoCuentasEstandar.CUENTA != " ").all()
    lista_financieros_generales = session.query(CatalogoCuentasEstandar).filter(
        CatalogoCuentasEstandar.ORIGEN == "7200-000-000", CatalogoCuentasEstandar.CUENTA != " ").all()
    lista_compras = ["COMPRAS"]
    lista_inversiones = ["INVERSIONES"]
    lista_obj = []
    if concepto == "GASTOS_GENERALES":
        lista_obj = lista_gastos_generales
    elif concepto == "COMPRAS":
        lista_obj = lista_compras
    elif concepto == "INVERSIONES":
        lista_obj = lista_inversiones
    elif concepto == "OTROS_GASTOS":
        lista_obj = lista_otros_generales
    elif concepto == "GASTOS_FINANCIEROS":
        lista_obj = lista_financieros_generales

    if concepto not in ['COMPRAS', 'INVERSIONES']:
        for i in lista_obj:
            lista.append(i.DESCRIPCION)
    elif concepto == 'COMPRAS':
        lista = lista_compras
    else:
        lista = lista_inversiones
    return jsonify(lista)


@app.route('/agregar_registro', methods=['POST'])
def agregar_registro():
    datos = request.get_json()
    try:
        fecha = datetime.now().date().strftime("%d-%m-%Y")
        actual = datetime.strptime(fecha, "%d-%m-%Y")
        hora = datetime.now().time()
        nuevo_folio = session.query(func.coalesce(
            func.max(ComprasGeneral.NO_POLIZA)+1, 1)).scalar()
        nueva_compra_temporal = ComprasDetalleTemporal(
            NO_POLIZA=nuevo_folio,
            FORMA_PAGO=datos['forma_pago'],
            CATEGORIA=datos['categoria'],
            FECHA_CREACION=actual,
            HORA_CREACION=hora,
            FECHA_POLIZA=datos['fecha_pago'],
            DESCRIPCION=datos['descripcion'],
            CTA_PAGO=datos['cta_pago'],
            PROVEEDOR=datos['proveedor'],
            NO_DOCUMENTO=datos['no_documento'],
            CONCEPTO=datos['concepto'],
            AUTORIZA=datos['autorizo'],
            AREA=datos['area'],
            VEHICULO=datos['vehiculo'],
            KILOMETRAJE=datos['kilometraje'],
            IMPORTE=datos['importe'],
            IVA=datos['iva'],
            TOTAL=datos['total'],
            DETALLE=datos['detalle'],
            EDITOR_USER="ADMIN",
            ESTATUS='VIGENTE'
        )
        session.add(nueva_compra_temporal)
        session.commit()
        return jsonify(Operacion='Exitosa', no_registro=nueva_compra_temporal.NO_REGISTRO)
    except:
        return jsonify(Operacion='Fallida')


@app.route('/api/verificar_registros', methods=['GET'])
def verificar_registros():
    registros = session.query(ComprasDetalleTemporal).all()

    if len(registros) > 0:
        i = registros[-1]
        print(i.CTA_PAGO)
        datos = {
            'respuesta': 'true',
            'forma_pago': i.FORMA_PAGO,
            'ct_pago': i.CTA_PAGO,
            'fecha_pago': i.FECHA_POLIZA.strftime("%Y-%m-%d"),
            'descripcion': i.DESCRIPCION
        }
        return jsonify(datos)
    else:
        return jsonify(respuesta='false')


@app.route('/prueba_envio', methods=['POST'])
def recibir_datos():
    datos = request.get_json()
    # Procesa los datos recibidos del cliente
    # Realiza cualquier otra operación necesaria
    # Devuelve una respuesta al cliente si es necesario
    # Por ejemplo, puedes devolver una respuesta JSON con el mensaje "Datos recibidos"
    return jsonify(message="Datos recibidos")


@app.route('/borrar/detalle_temporal/<int:registro>', methods=['GET'])
def borrar_registro(registro):
    seleccion = session.query(ComprasDetalleTemporal).filter(
        ComprasDetalleTemporal.NO_REGISTRO == registro).first()
    session.delete(seleccion)
    session.commit()
    return redirect('/alta_gastos')


@app.route('/guardar_poliza', methods = ['GET'])
def guardar_poliza():
    datos = session.query(ComprasDetalleTemporal).all()
    fecha = datetime.now().date().strftime("%d-%m-%Y")
    actual = datetime.strptime(fecha, "%d-%m-%Y")
    hora = datetime.now().time()
    totales_float = 0.0
    print("Estos deben ser los datos", len(datos))
    for i in datos:
        nueva_detalle = ComprasDetalle(
            NO_POLIZA=i.NO_POLIZA,
            FORMA_PAGO=i.FORMA_PAGO,
            CATEGORIA=i.CATEGORIA,
            FECHA_CREACION=i.FECHA_CREACION,
            HORA_CREACION=i.HORA_CREACION,
            FECHA_POLIZA=i.FECHA_POLIZA,
            DESCRIPCION=i.DESCRIPCION,
            CTA_PAGO=i.CTA_PAGO,
            PROVEEDOR=i.PROVEEDOR,
            NO_DOCUMENTO=i.NO_DOCUMENTO,
            CONCEPTO=i.CONCEPTO,
            AUTORIZA=i.AUTORIZA,
            AREA=i.AREA,
            VEHICULO=i.VEHICULO,
            KILOMETRAJE=i.KILOMETRAJE,
            IMPORTE=i.IMPORTE,
            IVA=i.IVA,
            TOTAL=i.TOTAL,
            DETALLE=i.DETALLE,
            EDITOR_USER=i.EDITOR_USER,
            ESTATUS=i.ESTATUS
        )
        session.add(nueva_detalle)
        
        totales_float += float(i.TOTAL)

    nueva_general = ComprasGeneral(
        NO_POLIZA = session.query(func.coalesce(func.max(ComprasGeneral.NO_POLIZA)+1, 1)).scalar(),
        FECHA_CREACION=actual,
        HORA_CREACION=hora,
        FECHA_POLIZA=datos[-1].FECHA_POLIZA,
        DESCRIPCION=datos[-1].DESCRIPCION,
        TOTAL_GENERAL=totales_float,
        EDITOR_USER="ADMIN",
        ESTATUS='VIGENTE'
    )
    for i in datos:
        session.query(ComprasDetalleTemporal).filter(
            ComprasDetalleTemporal.NO_POLIZA == i.NO_POLIZA).delete()

    session.add(nueva_general)
    session.commit()
    return jsonify(respuesta = 'Exitosa')

@app.route('/gastos')
def gastos():
    return render_template('gastos.html', registros = session.query(ComprasGeneral).order_by(ComprasGeneral.NO_POLIZA.asc()).all())

@app.route('/gastos/info/<int:poliza>', methods = ['GET'])
def info_gasto(poliza):
    gasto = session.query(ComprasGeneral).filter(ComprasGeneral.NO_POLIZA == poliza).first()
    
    return render_template('info_gasto.html', gasto = gasto)

@app.route('/api/cuentas_recibos/<int:poliza>', methods= ['GET'])
def cuentas_recibo(poliza):
    servicio = {}
    detalles = session.query(ComprasDetalle).filter(ComprasDetalle.NO_POLIZA == poliza).all()
    cuenta = ""
    cuenta_total = ""
    for i in detalles:
        no_cuenta = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == i.CONCEPTO).first()
        info_cuenta_pago = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == i.CTA_PAGO).first()
        if no_cuenta.CUENTA != "":
            cuenta = no_cuenta.CUENTA
        elif no_cuenta.SUBCUENTA != "":
            cuenta = no_cuenta.SUBCUENTA
        else:
            cuenta = no_cuenta.ORIGEN
        movimiento_1 = {'no_cuenta': cuenta, 'nombre' : no_cuenta.DESCRIPCION, 'movimiento' : f'{i.NO_DOCUMENTO} {i.PROVEEDOR}', 'debe': i.IMPORTE, 'haber': 0}
        if i.IVA > 0:
            cuenta_iva = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == 'IVA ACREDITABLE PAGADO').first()
            iva = {'no_cuenta': cuenta_iva.CUENTA, 'nombre' : cuenta_iva.DESCRIPCION, 'movimiento' : f'{i.NO_DOCUMENTO} {i.PROVEEDOR}', 'debe': i.IVA, 'haber': 0}
        if info_cuenta_pago.CUENTA != "":
            cuenta_total = info_cuenta_pago.CUENTA
        elif info_cuenta_pago.SUBCUENTA != "":
            cuenta_total = info_cuenta_pago.SUBCUENTA
        else:
            cuenta_total = info_cuenta_pago.ORIGEN
        movimiento_total = {'no_cuenta': cuenta_total, 'nombre' : info_cuenta_pago.DESCRIPCION, 'movimiento' : f'{i.NO_DOCUMENTO} {i.PROVEEDOR}', 'debe': 0, 'haber': i.TOTAL}

        servicio[str(i.NO_REGISTRO)] = {'movimiento1': movimiento_1, 'iva' : iva, 'movimiento_total' : movimiento_total}
    
    return jsonify(servicio)

@app.route('/gastos/busqueda/<string:filtrado>', methods = ['GET'])
def busquea_gastos(filtrado):
    time.sleep(3)
    envio = {}
    consulta1 = session.query(ComprasGeneral).filter(or_(ComprasGeneral.NO_POLIZA.like(f'%{filtrado}%'),
                                                                     ComprasGeneral.DESCRIPCION.like(f'%{filtrado}%'),
                                                                     ComprasGeneral.FECHA_POLIZA.like(f'%{filtrado}%'))).all()
    for i in consulta1:
        envio[str(i.NO_POLIZA)] = {'fecha' : i.FECHA_POLIZA.strftime("%d-%m-%Y"), 'poliza': i.NO_POLIZA, 'descripcion' : i.DESCRIPCION, 'total': i.TOTAL_GENERAL, 'revisado': i.REVISADO}
    return jsonify(envio)

@app.route('/cancelar_gastos', methods = ['GET'])
def cancelar_gastos():
    registros = session.query(ComprasDetalleTemporal).all()
    if len(registros) >= 1:
        for i in registros:
            session.delete(i)
        session.commit()
        return jsonify(respuesta = 'Exitosa')
    else:
        return jsonify(respuesta = 'Fallido')

@app.route('/poliza/descarga/<int:poliza>', methods = ['GET'])
def generar_poliza(poliza):
    general = session.query(ComprasGeneral).filter(ComprasGeneral.NO_POLIZA == poliza).first()
    PDFGASTO(general)
    archivo = f'documents/polizas/reporte_poliza.pdf'
    return send_file(archivo, as_attachment=True)
    

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)