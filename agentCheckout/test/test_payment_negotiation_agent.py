import asyncio
from agentCheckout.test.payment_negotiation_agent import PaymentNegotiationAgent

async def test_conversation():
    agent = PaymentNegotiationAgent()
    
    # Ejemplo de conversación
    messages = [
        "Hola, quiero comprar un vuelo por 68000 pesos",
        "¿Puedes darme un descuento?",
        "Ok, genérame el link de pago",
        "Gracias, adiós"
    ]
    
    for message in messages:
        response = await agent.process_message(message)
        print(f"\nUsuario: {message}")
        print(f"Asistente: {response}")

if __name__ == "__main__":
    asyncio.run(test_conversation()) 