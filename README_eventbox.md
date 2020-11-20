# Chatbot Amazon Lex y Whatsapp (Twilio): Guía paso a paso


En este Workshop vamos a implementar un Chatbot utilizando el servicio Amazon Lex y lo integraremos con la plataforma de mensajería instantánea WhatsApp. Esta integración se realizará a través de la plataforma (twilio) que nos permitirá recibir mensajes directamente desde la aplicación whatsapp (web o smartphone). Como pasos opcionales podemos integrar nuestro chatbot con Facebook Messenger o en nuestro propio sitio web.

Se trata de un caso de uso para el agendamiento de horas al dentista, no obstante puede extenderse para cualquier tipo de interacción con un asistente virtual, por ejemplo preguntas y respuestas frecuentes, información del estado de un caso de soporte, solicitud de información personalizada, ejecución de un procesamiento automático, etc.


## 1.2 Arquitectura

Arquitectura está compuesta por un Bot Lex configurado para interactuar con el usuario y resolver la información necesaria para el agendamiento (motivo,  hora y día). Una vez resuelta la información, se envía la solicitud a una función Lambda que procesa el requerimiento insertando la cita en la tabla DynamoDB (para este ejercicio no existe ninguna validación de negocio en la función Lambda, sólo inserta la cita).

Hacia el cliente la interacción se realiza a través de una integración con Twilio que permite enviar y recibir mensajes de WhatsApp hacia el Chatbot.


!["arquitectura"](img/whatsapp_lex.jpg)



### **[Acceder a la Guía Paso a Paso ➡️ ](https://github.com/ensamblador/whatsapp-lex/blob/master/README.md)**