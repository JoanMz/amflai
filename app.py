import os
import re
from fastapi import FastAPI, Request, Response, BackgroundTasks
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flight_agent import obtener_informacion_viaje  # Importa tu función personalizada

app = FastAPI()

# Configura tus credenciales de Twilio
account_sid = 'TU_ACCOUNT_SID'  # Reemplaza con tu Account SID de Twilio
auth_token = 'TU_AUTH_TOKEN'    # Reemplaza con tu Auth Token de Twilio
client = Client(account_sid, auth_token)

@app.get('/')
def root_page():
    data = {'response': 200,
            'body': 'Esta es la página raíz'
            }
    return Response(content=data['body'], status_code=200)

@app.post('/webhook/message/bot')
async def response_from_bot(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    incoming_message = form.get('Body', '')
    from_number = form.get('From', '')
    to_number = form.get('To', '')
    user_name = form.get('ProfileName', '')
    message_sid = form.get('SmsMessageSid', '')
    print(f"Mensaje entrante: {incoming_message}")
    print(f"De: {from_number}")
    print(f"Nombre de usuario: {user_name}")

    # Enviar respuesta inmediata al usuario
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("Estamos procesando tu solicitud, te responderemos en breve.")
    response_body = str(resp)
    print(f"Respuesta inmediata enviada al usuario.")

    # Iniciar tarea en segundo plano para procesar y responder
    background_tasks.add_task(procesar_y_responder, incoming_message, from_number, to_number)

    return Response(content=response_body, media_type="application/xml")

def procesar_y_responder(incoming_message, from_number, to_number):
    try:
        # Procesar el mensaje que toma tiempo
        response = obtener_informacion_viaje(incoming_message)
        print(f"Respuesta del agente: {response}")

        # Enviar la respuesta final al usuario
        message = client.messages.create(
            body=response,
            from_=to_number,  # Reemplaza con tu número de WhatsApp de Twilio
            to=from_number
        )
        print(f"Mensaje enviado al usuario con SID: {message.sid}")
    except Exception as e:
        print(f"Error al procesar y responder: {e}")