# Chatobot Amazon Lex y Whatsapp (Twilio): Guía paso a paso

# 1. Introduccion 

TO DO

## 1.1 Objetivo

En este Workshow vamos a implemntar un Chabot usando Amazon Lex y lo vamos a integrar con la plataforma de mensajería instantánea WhatsApp. Esta integración se realizará a través de la plataforma (twilio) que nos permitirá recibir mensajes directamente desde la aplicación whatsapp (web o smartphone).

Se trata de un caso de uso para el agenda miento de horas al dentista, no obstante puede extenderse para cualquier tipo de interacción Con un asistente virtual, por ejemplo preguntas y respuestas frecuentes, información del estado de un caso de soporte, solicitud de información personalizada, ejecución de un procesamiento automático, etc.


## 1.2 Arquitectura

Arquitectura está compuesta por un Chat Bot Lex configurado para interactuar con el usuario y resolver la información necesaria para el agendamiento (motivo,  hora y día). Una vez resuelta la información, se envía la solicitud a una función Lambda que procesa el requerimiento insertando la cita en la tabla DynamoDB (para este ejercicio no existe ninguna validación de negocio en la función Lambda, sólo inserta la cita).

Hacia el cliente la interacción se realiza a través de una integración con Twilio que permite enviar y recibir mensajes de WhatsApp hacia el Chatbot.


!["arquitectura"](img/whatsapp_lex.jpg)

## 1.3 Costos

Los costos de la solución vienen dados por el uso de acuerdo a las transacciones realizadas:
* Amazon Lex: 0.004 USD por request de voz y 0.00075 USD por request de texto
* Lambda: [0.2 USD por Millón de solicitudes + 0.0000166667 USD por GB-segundo](https://aws.amazon.com/lambda/pricing/) 
* DynamoDB: 0.25 USD por GB (después de los 25 GB Gratuitos) + 1.25 USD por millon de unidades de escritura y 0.25 USD por millon de unidades de lectura

**Ejemplo:**

Supongamos el caso de nuestro Chat Bot intercambia 10 mensajes con el usuario para intento de agendamiento que realizamos, durante el mes tenemos 1000 conversaciones y 500 agendamientos. Cada registro de agendamiento pesa 1 KB.

**Lex:** 
* Mensajes  = 1000 x 10 = 10.000 
* Costo  = 10000 x 0.00075 = 7,5 USD

**Lambda:**
* Solicitudes: 500
* Costo Invocaciones = 500 / 1.000.000 x 0.2 USD = 0.0001 USD
* GB-Segundo = 500 x (100 milisegundos) x (256 MB)  =  500 x 0.1 x 0.25 = 12.5 GB-Segundo
* Costo por GB-Segundo = 12.5 x 0.0000166667 USD = 0.0002 USD

**DynamoDB**
* Unidades de Escritura: 500 x 1 KB / 1 KB= 500 WCU
* Costo por escritura: 500 / 1.000.000 x 1.25 = 0.000625
* Costo por almacenamiento: 500 KB / 1.000.000 x 0.25 = 0.000125 USD (adicional por cada mes)
* Costo por escritura: Depende de la cantidad de lecturas. Si se lee 5 veces el costo es 0.000625 USD.

**Twilio**
Los costos de twilio deben ser revisados en https://www.twilio.com/whatsapp/pricing/us
Al momento de la redacción de esta guía los costos de twilio son 0.005 USD por mensaje.

<br/><br/>
___
<br/><br/>


# 2. Despliegue de la solución

## 2.1 Amazon Lex Chatbot (En español)

Amazon Lex es un servicio para crear interfaces de conversación con voz y texto. Ofrece las funcionalidades de deep learning como reconocimiento automático de voz para convertir voz en texto y tecnología de comprensión del lenguaje natural para reconocer la intención del texto. [Más información de Lex](https://aws.amazon.com/es/lex/)

### [Paso a paso armar el bot ➡️ ](README_Step_by_Step_Lex.md)

<br/><br/>

## 2.2 La Base de Datos de Agendas

Amazon DynamoDB es un servicio de base de datos NoSQL totalmente administrado que ofrece un rendimiento rápido, confiable y escalable. Vamos a utilizar este servicio para crear una tabla donde almacenaremos las agendas. 

### [Tabla DynamoDB de Agendas ➡️ ](README_Step_by_Step_Dynamo.md)

<br/><br/>


## 2.3 Función Lambda de Agendamiento

Con AWS Lambda, puede ejecutar código sin aprovisionar ni administrar servidores. Solo tiene que cargar el código y Lambda se encargará de todo lo necesario para ejecutar y escalar el código con alta disponibilidad. Esta función Lambda será la encargada de tomar el `Fulfillment`de Lex y convertirlo en una cita en la base de datos.

### [Paso a Paso Funcion Lambda ➡️ ](README_Step_by_Step_Lambda.md)

<br/><br/>


## 2.3 Cumplimiento (Fulfillment) de la Intención utilizando la función Lambda.

Antes de continuar, asegúrese de haber realizado los pasos anteriores y confirmar que todo funciona correctamente (pruebas del Bot de Lex y pruebas de la función Lambda). Ahora lo que haremos será enganchar nuestro Bot con la función al momento del Fulfillment del intent, para eso vamos a la Consola de Lex y editamos el intent.

### [Paso a Paso integrar con la Funcion Lambda ➡️ ](README_Step_by_Step_Integracion_Lambda.md)
<br/><br/>

## 2.5 Agregar la interfaz web (front end opcional)

Nuestro Bot de agendamientos ya está listo y funcionando completamente, pero no cuenta con una interfaz web que permita interactuar directamente con el. En este paso opcional podemos generar una UI (user interface).

### [Paso a Paso Web UI ➡️ ](README_Step_by_Step_Web.md)
<br/><br/>

## 2.6 Utilizando Nuestro Bot con Whatsapp

### [Paso a Paso integrar Whatsapp ➡️ ](README_Step_by_Step_Integracion_Whatsapp.md)
<br/><br/>

### 2.7 Análisis de Sentimiento (opcional)

### 2.7 Visualización de los datos (opcional)

## 3 Limpieza

## 4 Material adicional