# Función Lambda de Agendamiento

Con AWS Lambda, puede ejecutar código sin aprovisionar ni administrar servidores. Solo tiene que cargar el código y Lambda se encargará de todo lo necesario para ejecutar y escalar el código con alta disponibilidad. Esta función Lambda será la encargada de tomar el `Fulfillment`de Lex y convertirlo en una cita en la base de datos.

### 1. Primero vamos a la [consola de AWS Lambda](https://console.aws.amazon.com/lambda) y creamos una nueva función.

* Utilizamos **Crear desde cero**
* Nombre de la funcion: **FulFillmentLambda**
* Tiempo de ejecución: **Python 3.6 o 3.7**

Para el resto utilice la configuración por defecto y cree la nueva funcion.
![](img/Lambda_1.jpg)

<br/><br/>
Una vez generada, en la pestaña `configuración` vamos a configurar la Memoria, Timeout y Variables de entorno.
![](img/Lambda_5.jpg)

### 2. Agregamos como variable de entorno 
Vamos a **`configuración > Variables de entorno`**
![](img/Lambda_2.jpg)
utilizamos:
* Clave: **APPOINTMENTS_TABLE**
* Valor: **agendamientos** (o el nombre que utilizó para crear la table en DynamoDB)

![](img/Lambda_3.jpg)
Click en **Guardar**

<br/><br/>

### 3. modificamos nuestra configuración de RAM Aprovisionada y timeout.
Vamos a  **`configuración > Configuración básica`**
* Memoria: **256MB**
* Tiempo de espera: **20s**

![](img/Lambda_4.jpg)
Click en **Guardar**

## 4. Modificamos los permisos del rol de ejecución.
Para ello vamos directamente a **`permisos > rol de ejecución`**, con un click accedemos a la consola de IAM para editar la politica del rol.

![](img/Lambda_6.jpg)


### 2.3 Cumplimiento (Fulfillment) de la Intención.
### 2.4 Pruebas de Bot agendando.

### 2.5 Agregar la interfaz web (front-end)

### 2.6 Utilizando Whatsapp
### 2.6.1 Crear una cuenta gratuita de Twilio
### 2.6.2 Twilio account SID y AUTH Token
### 2.6.3 Lex endopoint url de Twilio channel
### 2.6.5 Pruebas end to end.

### 2.7 Análisis de Sentimiento (opcional)

### 2.7 Visualización de los datos (opcional)

## 3 Limpieza

## 4 Material adicional