#*********************************** IMPORTACION PARA BASE DE DATOS SQLALCHEMY *****************************************

from sqlalchemy import func, UniqueConstraint, create_engine, Column, Integer, String, DECIMAL, VARCHAR, DateTime, Time, Float, Date, Numeric, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import locale
from sqlalchemy.sql import text
from dateutil.parser import parse

locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')
# ********************************************--INICIO DE SISTEMA--*****************************************************
connection_string = "DRIVER={ODBC Driver 17 for SQL server};SERVER=localhost;DATABASE=PRINCIPAL;UID=sa;PWD=crmmexico"
# Crea una instancia de la clase create_engine y establece la conexión con la base de datos
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(connection_string))

# Crea una sesión de la base de datos utilizando el objeto sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Define la estructura de la tabla utilizando la clase declarative_base
Base = declarative_base()


class Clientes(Base):
    __tablename__ = 'CLIENTES'
    NID_CLIENTE = Column(Integer, primary_key=True)
    FECHA_DE_ALTA = Column(Date, nullable=False)
    HORA = Column(Time, nullable=False)
    APELLIDO_PATERNO = Column(String(200), nullable=False)
    APELLIDO_MATERNO = Column(String(200), nullable=False)
    NOMBRE_S = Column(String(200), nullable=False)
    FECHA_DE_NACIMIENTO = Column(Date, nullable=False)
    NACIONALIDAD = Column(String(200), nullable=False)
    ESTADO_DE_NACIMIENTO = Column(String(200), nullable=False)
    GENERO = Column(String(20), nullable=False)
    RFC = Column(String(13), nullable=False)
    CURP = Column(String(18), nullable=False, unique=True)
    TIPO_IDENTIFICACION = Column(String(100), nullable=False)
    FOLIO_IDENTIFICACION = Column(String(100), nullable=False, unique=True)
    ESTADO_CIVIL = Column(String(100), nullable=False)
    CALLE = Column(String(200), nullable=False)
    NO_EXTERIOR = Column(String(50), nullable=False)
    NO_INTERIOR = Column(String(50), nullable=False)
    COLONIA = Column(String(200), nullable=False)
    ENTRE_CALLE = Column(String(200), nullable=False)
    Y_CALLE = Column(String(200), nullable=False)
    CIUDAD = Column(String(200), nullable=False)
    ESTADO_DOM = Column(String(200), nullable=False)
    CODIGO_POSTAL = Column(String(10), nullable=False)
    CARACTERISTICAS_DOM = Column(String(200), nullable=False)
    ANTIGUEDAD_DOM = Column(String(100), nullable=False)
    TIPO_VIVIENDA = Column(String(100), nullable=False)
    DEPENDIENTES = Column(String(100), nullable=False)
    EMAIL = Column(String(200), nullable=False)
    TELEFONO = Column(String(12), nullable=False)
    NOMBRE_NEGOCIO = Column(String(200), nullable=False)
    GIRO_NEGOCIO = Column(String(200), nullable=False)
    HORARIO = Column(String(50), nullable=False)
    ANTIGUEDAD_NEGOCIO = Column(String(50), nullable=False)
    INGRESOS_DIARIOS = Column(Numeric(11,2), nullable=False)
    OTROS_INGRESOS = Column(Numeric(11,2), nullable=False)
    CALLE_NEGOCIO = Column(String(200), nullable=False)
    NO_EXTERIOR_NEGOCIO = Column(String(50), nullable=False)
    NO_INTERIOR_NEGOCIO = Column(String(50), nullable=False)
    COLONIA_NEGOCIO = Column(String(200), nullable=False)
    ENTRE_CALLE_NEGO = Column(String(200), nullable=False)
    Y_CALLE_NEGOCIO = Column(String(200), nullable=False)
    CIUDAD_NEGOCIO = Column(String(200), nullable=False)
    ESTADO_NEGOCIO = Column(String(200), nullable=False)
    CP_NEGOCIO = Column(String(10), nullable=False)
    CARACTERISTICAS_NEGOCIO = Column(String(200), nullable=False)
    CELULAR = Column(String(12), nullable=False)
    RUTA_ASIGNADA = Column(String(15), nullable=False)
    FOLIO_REF = Column(String(200), nullable = False)
    NOMBRE_REF_1 = Column(String(200), nullable=False)
    TELEFONO_REF_1 = Column(String(12), nullable=False)
    DIRECCION_REF_1 = Column(String(200), nullable=False)
    NOMBRE_REF_2 = Column(String(200), nullable=False)
    TELEFONO_REF_2 = Column(String(12), nullable=False)
    DIRECCION_REF_2 = Column(String(200), nullable=False)
    OBSERVACION_1 = Column(String(200), nullable=False)
    OBSERVACION_2 = Column(String(200), nullable=False)
    OBSERVACION_3 = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100), server_default='Jesus')
    ESTATUS = Column(String(10), nullable=False, server_default='VIGENTE')

class Prospectos(Base):
    __tablename__ = 'PROSPECTOS'
    FOLIO = Column(Integer, primary_key=True, autoincrement=True)
    FECHA = Column(Date, nullable=False)
    HORA = Column(Time, nullable=False, default=func.now())
    NOMBRE = Column(String(200), nullable=False)
    TELEFONO = Column(String(12), nullable=False)
    DIRECCION = Column(String(300), nullable=False)
    REFERENCIA_DOMICILIO = Column(String(200), nullable=False)
    MONTO_SOLICITADO = Column(DECIMAL(11,2), nullable=False)
    FORMA_DE_ENTERARSE = Column(String(50), nullable=False)
    PROMOTOR = Column(String(200), nullable=False)
    OBSERVACIONES = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100))
    ESTATUS = Column(String(10), nullable=False, default='VIGENTE')

class Empleados(Base):
    __tablename__ = 'EMPLEADOS'

    NID_EMPLEADO = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    FECHA_DE_INGRESO = Column(Date, nullable=False)
    HORA = Column(Time, nullable=False)
    APELLIDO_PATERNO = Column(String(200), nullable=False)
    APELLIDO_MATERNO = Column(String(200), nullable=False)
    NOMBRE_S = Column(String(200), nullable=False)
    FECHA_DE_NACIMIENTO = Column(Date, nullable=False)
    NACIONALIDAD = Column(String(200), nullable=False)
    ESTADO_DE_NACIMIENTO = Column(String(200), nullable=False)
    GENERO = Column(String(20), nullable=False)
    RFC = Column(String(13), nullable=False, unique=True)
    CURP = Column(String(18), nullable=False, unique=True)
    TIPO_IDENTIFICACION = Column(String(100), nullable=False)
    FOLIO_IDENTIFICACION = Column(String(100), nullable=False, unique=True)
    ESTADO_CIVIL = Column(String(100), nullable=False)
    CALLE = Column(String(200), nullable=False)
    NO_EXTERIOR = Column(String(50), nullable=False)
    NO_INTERIOR = Column(String(50), nullable=False)
    COLONIA = Column(String(200), nullable=False)
    ENTRE_CALLE = Column(String(200), nullable=False)
    Y_CALLE = Column(String(200), nullable=False)
    CIUDAD = Column(String(200), nullable=False)
    ESTADO_DOM = Column(String(200), nullable=False)
    CODIGO_POSTAL = Column(String(10), nullable=False)
    CARACTERTISTICAS_DOM = Column(String(200), nullable=False)
    ANTIGUEDAD_DOM = Column(String(100), nullable=False)
    TIPO_VIVIENDA = Column(String(100), nullable=False)
    DEPENDIENTES = Column(String(100), nullable=False)
    EMAIL = Column(String(200), nullable=False)
    CELULAR = Column(String(12), nullable=False)
    REGIMEN_CONTRATA = Column(String(100), nullable=False)
    NSS = Column(String(11), nullable=False, unique=True)
    SINDICALIZADO = Column(String(100), nullable=False)
    TIPO_JORNADA = Column(String(100), nullable=False)
    PUESTO = Column(String(200), nullable=False) # ForeignKey('GEN_PUESTOS.PUESTO')
    TIPO_CONTRATO = Column(String(100), nullable=False)
    RIESGO_PUESTO = Column(String(100), nullable=False)
    PERIODO_PAGO = Column(String(100), nullable=False)
    SDI = Column(Float(11,2), nullable=False)
    ESTADO_DONDE_LABORA = Column(String(200), nullable=False)
    NOMBRE_REF_1 = Column(String(200), nullable=False)
    TELEFONO_REF_1 = Column(String(12), nullable=False)
    DIRECCION_REF_1 = Column(String(200), nullable=False)
    NOMBRE_REF_2 = Column(String(200), nullable=False)
    TELEFONO_REF_2 = Column(String(12), nullable=False)
    DIRECCION_REF_2 = Column(String(200), nullable=False)
    OBSERVACION_1 = Column(String(200), nullable=False)
    OBSERVACION_2 = Column(String(200), nullable=False)
    OBSERVACION_3 = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100))
    ESTATUS = Column(String(10), nullable=False, default='VIGENTE')

class Vehiculos(Base):
    __tablename__ = 'VEHICULOS'
    NID_VEHICULO = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    FECHA = Column(Date, nullable=False)
    HORA = Column(Time, nullable=False, server_default=text("CONVERT(TIME(0), GETDATE())"))
    NO_SERIE = Column(String(100), nullable=False, unique=True)
    MARCA = Column(String(100), nullable=False)
    MODELO = Column(String(100), nullable=False)
    COLOR = Column(String(100), nullable=False)
    AÑO = Column(String(100), nullable=False)
    MOI = Column(Numeric(11, 2), nullable=False)
    PLACA = Column(String(100), nullable=False)
    EDITOR_USER = Column(String(100), nullable=True)
    ESTATUS = Column(String(10), nullable=False, server_default='VIGENTE')

class Proveedores(Base):
    __tablename__ = 'PROVEEDORES'

    NID_PROVEEDOR = Column(Integer, primary_key=True, autoincrement=True)
    FECHA_CREACION = Column(Date, nullable=False)
    FECHA_ULTIMA_EDICION = Column(DateTime, nullable=False)
    TIPO_EMPRESA = Column(String(100), nullable=False)
    DENOMINACION = Column(String(200), nullable=False, unique=True)
    CALLE = Column(String(200), nullable=False)
    NO_EXTERIOR = Column(String(50), nullable=False)
    NO_INTERIOR = Column(String(50), nullable=False)
    COLONIA = Column(String(200), nullable=False)
    ENTRE_CALLE = Column(String(200), nullable=False)
    Y_CALLE = Column(String(200), nullable=False)
    CIUDAD = Column(String(200), nullable=False)
    ESTADO_DOM = Column(String(200), nullable=False)
    CODIGO_POSTAL = Column(String(10), nullable=False)
    RFC = Column(String(13), nullable=False, unique=True)
    CURP = Column(String(18), nullable=False)
    CARACTERTISTICAS_DOM = Column(String(200), nullable=False)
    EMAIL = Column(String(200), nullable=False)
    TELEFONO = Column(String(12), nullable=False)
    PAGINA_WEB = Column(String(200), nullable=False)
    NOMBRE_CONT_1 = Column(String(200), nullable=False)
    TELEFONO_CONT_1 = Column(String(12), nullable=False)
    EMAIL_CONT_1 = Column(String(200), nullable=False)
    NOMBRE_CONT_2 = Column(String(200), nullable=False)
    TELEFONO_CONT_2 = Column(String(12), nullable=False)
    EMAIL_CONT_2 = Column(String(200), nullable=False)
    OBSERVACION_1 = Column(String(200), nullable=False)
    OBSERVACION_2 = Column(String(200), nullable=False)
    OBSERVACION_3 = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100), nullable=True)
    ESTATUS = Column(String(10), nullable=False, server_default='VIGENTE')


class Parametros(Base):
    __tablename__ = 'PARAMETROS'

    NID_EMPRESA = Column(Integer, primary_key=True, autoincrement=True)
    FECHA_CREACION = Column(DateTime, nullable=False)
    FECHA_ULTIMA_EDICION = Column(DateTime, nullable=False)
    FECHA_ACCION = Column(Date, nullable=False)
    TIPO_EMPRESA = Column(String(100), nullable=False)
    DENOMINACION = Column(String(200), nullable=False, unique=True)
    CALLE = Column(String(200), nullable=False)
    NO_EXTERIOR = Column(String(50), nullable=False)
    NO_INTERIOR = Column(String(50), nullable=False)
    COLONIA = Column(String(200), nullable=False)
    ENTRE_CALLE = Column(String(200), nullable=False)
    Y_CALLE = Column(String(200), nullable=False)
    CIUDAD = Column(String(200), nullable=False)
    ESTADO_DOM = Column(String(200), nullable=False)
    CODIGO_POSTAL = Column(String(10), nullable=False)
    RFC = Column(String(13), nullable=False, unique=True)
    CURP = Column(String(18), nullable=False)
    CARACTERTISTICAS_DOM = Column(String(200), nullable=False)
    EMAIL = Column(String(200), nullable=False)
    TELEFONO = Column(String(12), nullable=False)
    PAGINA_WEB = Column(String(200), nullable=False)
    FECHA_CONSTI = Column(Date, nullable=False)
    GIRO_NEGOCIO = Column(String(200), nullable=False)
    NACIONALIDAD = Column(String(200), nullable=False)
    REGIMEN = Column(String(200), nullable=False)
    NOMBRE_REPRE = Column(String(200), nullable=False)
    RFC_REPRE = Column(String(13), nullable=False)
    CURP_REPRE = Column(String(18), nullable=False)
    EDITOR_USER = Column(String(100), nullable=True)
    ESTATUS = Column(String(10), nullable=False, server_default='VIGENTE')

class ComprasDetalle(Base):
    __tablename__ = 'COMPRAS_DETALLE'
    NO_REGISTRO = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    NO_POLIZA = Column(Integer, nullable=False)
    FORMA_PAGO = Column(String(30), nullable=False)
    CATEGORIA = Column(String(30), nullable=False)
    FECHA_CREACION = Column(Date, nullable=False)
    HORA_CREACION = Column(Time(timezone=False), nullable=False)
    FECHA_POLIZA = Column(Date, nullable=False)
    DESCRIPCION = Column(String(200), nullable=False)
    CTA_PAGO = Column(String(200), nullable=False)
    PROVEEDOR = Column(String(200), nullable=False) # ForeignKey('GEN_PROVEEDORES.DENOMINACION')
    NO_DOCUMENTO = Column(String(10), nullable=False)
    CONCEPTO = Column(String(100), nullable=False)
    AUTORIZA = Column(String(200), nullable=False)
    AREA = Column(String(20), nullable=False)
    VEHICULO = Column(String(200), nullable=False) # ForeignKey('GEN_VEHICULOS.VEHICULO')
    KILOMETRAJE = Column(String(12), nullable=False)
    IMPORTE = Column(DECIMAL(11, 2), nullable=False)
    IVA = Column(DECIMAL(11, 2), nullable=False)
    TOTAL = Column(DECIMAL(11, 2), nullable=False)
    DETALLE = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100), nullable=False)
    ESTATUS = Column(String(10), nullable=False)

class ComprasGeneral(Base):
    __tablename__ = 'COMPRAS_GENERAL'
    
    NO_REGISTRO = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    NO_POLIZA = Column(Integer, nullable=False)
    FECHA_CREACION = Column(Date, nullable=False)
    HORA_CREACION = Column(Time, nullable=False, default=func.current_time())
    FECHA_POLIZA = Column(Date, nullable=False)
    DESCRIPCION = Column(String(200), nullable=False)
    TOTAL_GENERAL = Column(DECIMAL(11, 2), nullable=False)
    EDITOR_USER = Column(String(100), nullable=False)
    ESTATUS = Column(String(50), nullable=False)
    REVISADO = Column(String(100), nullable=True)

class ComprasDetalleTemporal(Base):
    __tablename__ = 'COMPRAS_DETALLE_TEMPORAL'

    NO_REGISTRO = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    NO_POLIZA = Column(Integer, nullable=False)
    FORMA_PAGO = Column(String(30), nullable=False)
    CATEGORIA = Column(String(30), nullable=False)
    FECHA_CREACION = Column(Date, nullable=False)
    HORA_CREACION = Column(Time(timezone=False), nullable=False)
    FECHA_POLIZA = Column(Date, nullable=False)
    DESCRIPCION = Column(String(200), nullable=False)
    CTA_PAGO = Column(String(200), nullable=False)
    PROVEEDOR = Column(String(200), nullable=False) # ForeignKey('GEN_PROVEEDORES.DENOMINACION')
    NO_DOCUMENTO = Column(String(10), nullable=False)
    CONCEPTO = Column(String(100), nullable=False)
    AUTORIZA = Column(String(200), nullable=False)
    AREA = Column(String(20), nullable=False)
    VEHICULO = Column(String(200), nullable=False) # ForeignKey('GEN_VEHICULOS.VEHICULO')
    KILOMETRAJE = Column(String(12), nullable=False)
    IMPORTE = Column(DECIMAL(11, 2), nullable=False)
    IVA = Column(DECIMAL(11, 2), nullable=False)
    TOTAL = Column(DECIMAL(11, 2), nullable=False)
    DETALLE = Column(String(200), nullable=False)
    EDITOR_USER = Column(String(100), nullable=False)
    ESTATUS = Column(String(10), nullable=False)

class GastosGenerales(Base):
    __tablename__ = "GASTOS_GENERALES"

    ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    CODIGO = Column(String(16), nullable=False, unique=True)
    DESCRIPCION = Column(String(50), nullable=False, unique=True)

class CatalogoCuentasEstandar(Base):

    __tablename__ = "CATALOGO_CUENTAS_ESTANDAR"
    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    ORIGEN = Column(String(30), nullable=False)
    CUENTA = Column(String(30), nullable=False)
    SUBCUENTA = Column(String(30), nullable=False)
    FECHA_CREACION = Column(DateTime, nullable=False)
    FECHA_ULTIMA_EDICION = Column(DateTime, nullable=False)
    RFC = Column(String(14), nullable=False)
    CUENTA_HEREDADA = Column(String(100), nullable=False)
    DESCRIPCION = Column(String(200), nullable=False)
    BANCARIO = Column(String(5))
    TIPO = Column(String(30), nullable=False)
    NIVEL = Column(Integer, nullable=False)
    CODIGO_AGRUPADOR = Column(String(30), nullable=False)
    NATURALEZA = Column(String(30), nullable=False)
    SALDO_INICIAL = Column(Float, nullable=False)
    CARGOS = Column(Float, nullable=False)
    ABONOS = Column(Float, nullable=False)
    SALDO_FINAL = Column(Float, nullable=False)
    USER_EDITOR = Column(String(50), nullable=False)

class CodigoAgrupador(Base):
    __tablename__ = "CODIGO_AGRUPADOR"
    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    NIVEL = Column(Integer, nullable=False)
    CODIGO = Column(String(7), nullable=False)
    NOMBRE = Column(String(200), nullable=False)