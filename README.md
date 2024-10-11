# Challenge Next Technologies

## Stack / Technologías utilizadas
+ Python 3.11
+ + Beanie - ODM para operar con MongoDB con validación de esquemas
+ Docker

## Descripción
### Punto 1.1 Carga de Información
Base de datos seleccionada: [__MongoDB__](https://www.mongodb.com/)
Se eligió esta base de datos NoSQL debido a la versatilidad de manejo de datos. Este al ser su punto fuerte, de igual manera es su punto débil a la hora de trabajar de manera estructurada. Por eso en la implementación del código se utiliza un __Validador de Datos__
Validador de datos seleccionado: [__BeanieODM__](https://beanie-odm.dev)
Beanie es un ODM, Object Document Mapper, que como un ORM, estructura mediante código los Documentos y a la vez valida la integridad de estos. A diferencia de otros, se utiliza esta opción porque utiliza el driver asíncrono [Motor](https://motor.readthedocs.io/), y permite ejecutar operaciones primitivas directamente.
Ademas de ser un complemento, Beanie puede ejecutar y sincronizar índices y _aggregates_ al inicio, eg:
```python
    client = AsyncIOMotorClient(MONGODB_URI)

    await init_beanie(
        database=client.next_technologies_challenge, # inicializa la base de datos 'next_technologies_challenge'
        document_models=[Payments, InvalidPayments, Companies], # inicializa las collecciones Payments, InvalidPayments y Companies y en caso de tenner índices o aggregates, los configura
    )

    # setup de otra db
    await init_beanie(
        database=client.OTRA_DB,
        document_models=[OtraColeccion],
    )
```
Con el _patrón_ de que al inicio de la app se ejecuten estos ``` init_beanie ```, se puede decir que se comporta como _pseudo migraciones_ que mantienen los datos íntegros

Ahora, las colecciones se describen mediante clases, cuyos atributos se validan con [Pydantic](https://docs.pydantic.dev/latest/), eg:
```python
    from beanie import Document
    from enum imoprt Enum


    class PaymentStatus(str, Enum):
        voided = "voided"
        pending = "pending_payment"
        paid = "paid"
        pre_authorized = "pre_authorized"
        refunded = "refunded"
        charged_back = "charged_back"
        expired = "expired"
        partially_refunded = "partially_refunded"

    class PaymentDoc(Document):
        id: str
        name: str
        company_id: str
        amount: float
        status: PaymentStatus
        created_at: datetime
        paid_at: datetime | None = None

        class Settings:
            name = "Charges" # determina el nombre de la colección en MongoDB
```
Los datos para crear un documento en la colección puede ser un diccionario arbitrario o un JSON, Pydantic valida cada atributo con el tipo de dato que se le especifica, incluso documentos embebidos, éstos siendo descritos con BaseModel, eg:

```python
    from beanie import Document
    from pydantic import BaseModel

    class Contacto(BaseModel):
        telefono: str
        direccion: str

    class Persona(Document):
        nombre: str
        contacto: Contacto
```

### Punto 1.2 Extracción
Se extrajo la información desde un csv. Se hizo uso de la librería estándar para extraer la información (csv)
Este se dividió en varios pasos
1. Extraer headers y datos
2. _Armar_ una lista de diccionarios con los headers y diccionarios
3. Validar la lista de diccionarios con _Pydantic_
4. Cargar los datos a la base de datos con _Beanie_

Al cargar la información se ignoraron las _newlines_ vacías. De igual modo al validar se encontró que hubo datos sucios, como
+ status erróneos
+ ids inválidos
+ campos vacíos cuando no deben estarlo

Para evitar la pérdida de datos, implementé una colección especial llamada __InvalidPayments__, cuya función es almacenar los registro erróneos para posteriormente corregirlos de manera orgánica.

### Punto 1.3 Transformación
Los datos se modelaron con base a la siguiente clase

```python
    from beanie import Document
    from enum imoprt Enum


    class PaymentStatus(str, Enum):
        voided = "voided"
        pending = "pending_payment"
        paid = "paid"
        pre_authorized = "pre_authorized"
        refunded = "refunded"
        charged_back = "charged_back"
        expired = "expired"
        partially_refunded = "partially_refunded"

    class PaymentDoc(Document):
        id: str
        name: str
        company_id: str
        amount: float
        status: PaymentStatus
        created_at: datetime
        paid_at: datetime | None = None

        class Settings:
            name = "Charges" # determina el nombre de la colección en MongoDB
```

Donde _PaymentStatus_ es una enumeración de posibles estatus que podría tener un pago/cargo. Se eligió este patrón para tener un control de los estatus
_PaymentDoc_ describe el pago como tal con los respectivos tipos, siendo None el equivalente a NULL

### 1.4 Dispersión de la información
Al igual que con los pagos/cargos, se elaboró una clase para describir a las empresas/_companies_

```python
    from beanie import Document


    class CompanyDoc(Document):
    id: str
    name: str

    class Settings:
        name = "Companies"
```

Para la extracción, se utilizaron los datos ya cargados en el punto 1.2 verificando los campos de interés ``` company_id, name ``` para posteriormente validarlos con _Pydantic_ y darlos de alta con _Beanie_

Hubieron detalles, como datos con ``` company_id ``` o ``` name ``` nulos. Para mitigar, se asociaron los ids en un diccionario con sus valores (names) respectivos y se limpiaron evaluando que no estuvieran en un _set_ de datos inválidos


## Instalación
Se debe acceder y clonar el repositiorio. De preferencia utilizar una __línea de comando__ compatible con ´bash´ en un sistema operativo basado en unix (MacOS/Linux), debido a las herramientas utilizadas. En caso de Windows, utilziar CMDer.
Al utilizar Python, este se debe configurar con las siguientes herramientas
+ Pyenv: permite manejar/seleccionar entre varios intérpretes de python. Este proyecto utiliza la versión 3.11.10. Seguir la [guía de instalación](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
+ Pipenv: maneja las dependencias y permite instalaciones reproducibles mendiante un ´lockfile´ _à la_ nodejs/npm. Seguir la [guía de instalación](https://pipenv-es.readthedocs.io/es/latest/)
+ docker: utilizado para "empaquetar" el siguiente software: mongodb


### Procedimiento
> Ya se debe tener instalado el software correspondiente
1. Colocarse con la línea de comando en la carpeta donde se haya clonado el proyecto
2. Activar el intérprete de Python con ``` pyenv local ```. En caso de que no se active, seguir el [troubleshooting](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv)
3. Instalar las dependencias con Pipenv mediante ``` pipenv install ```
4. Levantar la instancia de MongoDB con docker mediante ``` docker run -e MONGO_INITDB_ROOT_USERNAME=$MONGO_USER -e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD -p 27017:27017 -v $MONGO_VOLUME:/data/db:z --name $DB_NAME -d docker.io/mongodb/mongodb-community-server ```.
+ + Hay que verificar los permisos de lectura/escritura del volúmen que se vaya a compartir con la instancia de MongoDB mendiante ``` sudo chmod -R a+rw $MONGO_VOLUME ```

> 