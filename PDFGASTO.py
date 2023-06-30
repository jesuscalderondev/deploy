from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from math import ceil
from DATABASE import *

class PDFGASTO():
    def __init__(self, general:ComprasGeneral):
        c = canvas.Canvas("documents/polizas/reporte_poliza.pdf", pagesize=A4)
        width, height = A4

        locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')
        locale._override_localeconv = {
            'int_curr_symbol': '',
            'currency_symbol': '',}



        posiciones = []


        registros = session.query(ComprasDetalle).filter(
            ComprasDetalle.NO_POLIZA == general.NO_POLIZA).all()
        
        def encabezado():

            c.setFont("Helvetica-Bold", 14)

            titulo = "EMPRESA DE PRUEBA SA CV"
            c.drawCentredString(width / 2, height-20, titulo)
            titulo2 = "R.F.C. EMX180425T90"
            c.drawCentredString(width / 2, height-35, titulo2)

            c.setFont("Helvetica", 12)

            poliza_la = "POLIZA NO.:"
            c.drawString(50, height-70, poliza_la)

            # Obtener la longitud de la primera palabra
            longitud_poliza_la = c.stringWidth(poliza_la)

            c.setFont("Helvetica-Bold", 12)
            # Escribir el segundo fragmento de texto al lado del primero
            poliza = f"{general.NO_POLIZA} Eg"
            c.drawString(longitud_poliza_la*2 - 8, height-70, poliza)


            c.setFont("Helvetica", 12)

            fecha_la = "FECHA:"
            c.drawString(width-170, height-70, fecha_la)

            # Obtener la longitud de la primera palabra
            longitud_fecha_la = c.stringWidth(fecha_la)

            c.setFont("Helvetica-Bold", 12)
            # Escribir el segundo fragmento de texto al lado del primero
            fecha = general.FECHA_POLIZA.strftime("%d/%m/%Y")
            c.drawString(width - 200 + longitud_fecha_la*2 - 8, height-70, fecha)


            c.setFont("Helvetica", 12)

            concepto_la = "CONCEPTO:"
            c.drawString(50, height-100, concepto_la)

            # Obtener la longitud de la primera palabra
            longitud_concepto_la = c.stringWidth(concepto_la)

            c.setFont("Helvetica-Bold", 12)
            # Escribir el segundo fragmento de texto al lado del primero
            concepto = general.DESCRIPCION
            c.drawString(longitud_concepto_la*2 - 10, height-100, concepto)

            c.line(10, height-120, width-10, height-120)
            c.line(10, height-170, width-10, height-170)
            c.setFont("Helvetica-Bold", 12)
            # Escribir el segundo fragmento de texto al lado del primero
            NO_CUENTA = "NO. CUENTA"
            c.drawString(35, height-140, NO_CUENTA)

            posiciones.append(35)

            NOMBRE_CUENTA = "NOMBRE DE LA CUENTA"
            c.drawString(c.stringWidth(NO_CUENTA)*2 - 5, height-140, NOMBRE_CUENTA)

            posiciones.append(c.stringWidth(NO_CUENTA)*2 - 5)

            CONCEPTO_MO = "CONCEPTO O MOVIMIENTO"
            c.drawString((c.stringWidth(NO_CUENTA)*2) + 14, height-155, CONCEPTO_MO)

            posiciones.append(c.stringWidth(NO_CUENTA)*2 + 25)

            DEBE = "DEBE"
            c.drawString(c.stringWidth(NOMBRE_CUENTA)*2 +
                        c.stringWidth(NO_CUENTA) + 40, height-140, DEBE)

            posiciones.append(c.stringWidth(NOMBRE_CUENTA) *
                            2 + c.stringWidth(NO_CUENTA) + 40)

            HABER = "HABER"
            c.drawString(c.stringWidth(NOMBRE_CUENTA)*2 + c.stringWidth(NO_CUENTA) +
                        c.stringWidth(DEBE)*3 + 40, height-140, HABER)
            posiciones.append(c.stringWidth(NOMBRE_CUENTA)*2 +
                            c.stringWidth(NO_CUENTA) + c.stringWidth(DEBE)*3 + 40)

        def pie():
            
            c.rect(10, 30, 230, 40)
            c.rect(10+230, 30, 230, 40)
            c.rect(10+460, 30, width-10-470, 40)

            c.setFont("Helvetica-Bold", 12)
            HECHO_POR = "HECHO POR:"
            c.drawString(15, 55, HECHO_POR)
            c.setFont("Helvetica", 10)
            HECHO_POR = general.EDITOR_USER
            c.drawString(15, 40, HECHO_POR)

            c.setFont("Helvetica-Bold", 12)
            REVISADO_POR = "REVISADO POR:"
            c.drawString(245, 55, REVISADO_POR)
            c.setFont("Helvetica", 10)
            if general.REVISADO != None:
                REVISADO_POR = f'{general.REVISADO}'
                c.drawString(245, 40, REVISADO_POR)

            c.setFont("Helvetica-Bold", 12)
            REVISADO_POR = "POLIZA NO.:"
            c.drawString(475, 55, REVISADO_POR)
            c.setFont("Helvetica", 10)
            REVISADO_POR = f'EGRESOS {general.NO_POLIZA}'
            c.drawString(475, 40, REVISADO_POR)
            

        encabezado()
        pie()


        filas = 0
        contador_registros = 0
        total = ceil(len(registros)/5)
        actual = 1
        for i in registros:

            no_cuenta = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == i.CONCEPTO).first()
            info_cuenta_pago = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == i.CTA_PAGO).first()
            cuenta_iva = session.query(CatalogoCuentasEstandar).filter(CatalogoCuentasEstandar.DESCRIPCION == 'IVA ACREDITABLE PAGADO').first()
            c.setFont("Helvetica", 12)
            NO_CUENTA = no_cuenta.CUENTA
            c.drawString(posiciones[0], height-190-filas, NO_CUENTA)

            if len(i.CONCEPTO) > 25:
                NOMBRE_CUENTA = i.CONCEPTO[:25]
            else:
                NOMBRE_CUENTA = i.CONCEPTO
            c.drawString(posiciones[1], height-190-filas, NOMBRE_CUENTA)


            if len(i.PROVEEDOR) > 20:
                i.PROVEEDOR = i.PROVEEDOR[:20]
            CONCEPTO_MO = f'{i.NO_DOCUMENTO} {i.PROVEEDOR}'
            c.drawString(posiciones[2]-10, height-205-filas, CONCEPTO_MO)

            c.setFont("Helvetica-Bold", 12)

            DEBE = locale.currency(i.IMPORTE, grouping=True)
            c.drawString(posiciones[3]-c.stringWidth(DEBE)+50, height-190-filas, DEBE)

            c.setFont("Helvetica", 12)
            
            DEBE = locale.currency(i.IVA, grouping=True)
            if i.IVA > 0:
                NO_CUENTA = cuenta_iva.CUENTA
                c.drawString(posiciones[0], height-220-filas, NO_CUENTA)

                NOMBRE_CUENTA = cuenta_iva.DESCRIPCION
                c.drawString(posiciones[1], height-220-filas, NOMBRE_CUENTA)


                CONCEPTO_MO = f'{i.NO_DOCUMENTO} {i.PROVEEDOR}'
                c.drawString(posiciones[2]-10, height-235-filas, CONCEPTO_MO)

                c.setFont("Helvetica-Bold", 12)

                
                c.drawString(posiciones[3]-c.stringWidth(DEBE)+50, height-220-filas, DEBE)
            
            else:
                filas-=30

            c.setFont("Helvetica", 12)

            NO_CUENTA = info_cuenta_pago.CUENTA
            c.drawString(posiciones[0], height-250-filas, NO_CUENTA)

            NOMBRE_CUENTA = info_cuenta_pago.DESCRIPCION
            c.drawString(posiciones[1], height-250-filas, NOMBRE_CUENTA)


            CONCEPTO_MO = f'{i.NO_DOCUMENTO} {i.PROVEEDOR}'
            c.drawString(posiciones[2]-10, height-265-filas, CONCEPTO_MO)

            c.setFont("Helvetica-Bold", 12)

            HABER = locale.currency(i.TOTAL, grouping=True)
            c.drawString(posiciones[4]-c.stringWidth(HABER)+50, height-250-filas, HABER)


            filas += 110
            contador_registros += 1

            if contador_registros %5 == 0:
                c.setFont("Helvetica", 10)
                enum = "{} de {}".format(actual, total)
                c.drawCentredString(width / 2, 10, enum)
                c.showPage()
                filas=0
                pie()
                encabezado()
                actual+=1
                
            
            if contador_registros == len(registros):
                c.line(10, 110, width-10, 110)
                c.line(10, 80, width-10, 80)

                c.setFont("Helvetica-Bold", 12)
                CONCEPTO_MO = "SUMA IGUALES: "
                c.drawString(posiciones[2]+14, 90, CONCEPTO_MO)

                c.setFont("Helvetica-Bold", 12)

                DEBE = locale.currency(general.TOTAL_GENERAL, grouping=True)
                c.drawString(posiciones[3]-c.stringWidth(DEBE)+50, 90, DEBE)

                HABER = locale.currency(general.TOTAL_GENERAL, grouping=True)
                c.drawString(posiciones[4]-c.stringWidth(HABER)+50, 90, HABER)
                c.setFont("Helvetica", 10)
                enum = "{} de {}".format(actual, total)
                c.drawCentredString(width / 2, 10, enum)
                 
        c.save()