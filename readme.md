# PROYECTO CRM VERSIÓN WEB

Este proyecto está basado en el framework **Flask** de *Python*, interactuando con la base de datos a travez del **ORM SQLALCHEMY**.

## Conexión a la DB en el módulo DATABASE
Para realizar la conexión a la base de datos de **SQL SERVER**,importamos los reqursos necesarios paa trabajar la conexión, junto con la creación de las tablas que se explicará seguido de esto.

```python
from sqlalchemy import func, UniqueConstraint, create_engine, Column, Integer, String, DECIMAL, VARCHAR, DateTime, Time, Float, Date, Numeric, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
```

Luego creamos una cadena de texto para que nos sirva como parametro a la hora de conectarnos, en dicha cadena se observan lo siguiente:

*DRIVER*, que después del igual lleva el controlador que nos permitiría estar en contacto con nuestra base de datos SQL SERVER.

*SERVER*, donde pasamos el servidor al cual se va a conectar nuestra aplicación web.

*DATABASE*, otorgamos el nombre de la base de datos que está alojadda en nuestro servidor SQL SERVER.

*UID*, donde asignamos el usuario mediante el cual realizaremos nuestros registros y cambios en la base de datos.

*PWD*, en este campo pasamos la clave del usuario para acceder al servidor SQL SERVER.

```python
connection_string = "DRIVER={ODBC Driver 17 for SQL server};SERVER=DESKTOP-LQ7RKA1;DATABASE=CRM;UID=sa;PWD=crmmexico"
```

Después de haber creado la cadena de texto, se la pasamos a un engine, que funciona como motor para a conexión a la base de datos, luego hacemos uso del modulo *sessionmaker* para crear una sesión de trabajo con **SQLALCHEMY** y finalmente usamos el uso del método *declarative_base()* para crear todas las tablas en la base de datos de acuerdo a mapeo.

```python
#Código de referencia anterior
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(connection_string))
Session = sessionmaker(bind=engine)
session = Session()
```
### Creación de tablas, inserción y obtención de registros

El ORM **SQLALCHEMY** nos permite crear la tabla mediante el uso de clases (POO), en donde como parametro de la clase se le envía la variable de la última linea de código anterior, para crear la tabla, reconociendo las variables como columnas de la tabla y lo que se le asigna a dichas variables es la configuración de dichas columnas, a continuación un ejemplo:

```python
#Tenemos una tabla Usuarios en donde vamos a almacenar el id, el nombre de usuario y la clave
class Usuarios(Base):
    #id, es la llave primaria de nuestra tabla, automaticamente SQLALCHEMY la hace autoincrementable
    id = Column(Integer, primary_key=True)

    #Luego nombre_usuario, es una cadena de texto donde almacena máximo 16 cararacteres y no es posible dejarla vacía, además de que es único, dado el parametro unique
    nombre_usuario = Colum(String(16), nullable=False, unique=True)

    #Y la clave que comparte similitud con el nombre_usuario, exceptuando que es de máximo 12 caracteres y que esta no es única, ya que varios usuarios pueden tener la misma
    clave = Colum(String(12), nullable=False)

#Para insertar un dato en esta tabla basta con crear un objeto de la clase y usar el método add, así
nuevo_usuario = Usuarios(nombre_user="python_flask", clave="crmmexico")

#Llamamos a la sesión para interactuar, le damos el método add y le pasamos lo que va a agregar, automáticamente el ORM detecta en qué tabla va el registro por la clase del objeto
session.add(nuevo_usuario)

#En caso de querer obtener registros es así

un_usuario = session.query(Usarios).get(id=1)
#O también 
un_usuario = session.query(Usuarios).filter_by(id=1)
#Existen más maneras, pero estas son de las que más se usan en el proyecto

#Para obtener más de un registro, en este caso obtendremos todos los registros

usuarios = session.query(Usuarios).all()
```
### Vista de la tabla Usuarios

| id | nombre_usuario | clave |
| :---------: | :---------: | :---------: |
| 1 | python_flask | crmmexico |