from langchain.tools import BaseTool
from pydantic import Field, BaseModel
import requests
import json
from typing import Dict

class BoldPaymentAgentTool(BaseModel):
    name: str = Field(
        "BoldPaymentAgent",
        description="Herramienta para generar enlaces de pago usando Bold"
    )
    description: str = Field(
        "Genera enlaces de pago usando la API de Bold con el monto especificado",
        description="Descripción de la herramienta de pagos Bold"
    )
    api_key: str
    
    def _run(self, amount: float) -> Dict:
        """
        Genera un enlace de pago en Bold.

        Args:
            amount (float): Monto a cobrar en COP

        Returns:
            Dict: Información del enlace de pago generado
        """
        reqUrl = "https://integrations.api.bold.co/online/link/v1"
        
        headersList = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"x-api-key {self.api_key}"
        }

        payload = json.dumps({
            "amount_type": "CLOSE",
            "amount": {
                "currency": "COP",
                "total_amount": amount
            },
            "description": "Pago de vuelo",
            "callback_url": "https://vivecolombia.com.co/",
            "payment_methods": ["CREDIT_CARD", "PSE", "NEQUI"],
            "payer_email": "gustavochipantiza316@gmail.com",
            "image_url": "https://res.cloudinary.com/gregoryinnovo/image/upload/v1732491073/testOther/LOGO_VIVE_COLOMBIA_02_REDONDO_zqecy1.png"
        })

        try:
            response = requests.request("POST", reqUrl, data=payload, headers=headersList)
            response_data = response.json()
            
            if "payload" in response_data:
                payment_info = {
                    "payment_link": response_data["payload"]["payment_link"],
                    "url": response_data["payload"]["url"]
                }
                print(f"Link de pago generado: {payment_info['url']}")
                return payment_info
            else:
                return {"error": "No se pudo generar el link de pago"}
                
        except Exception as e:
            return {"error": f"Error al generar el link de pago: {str(e)}"}

    async def _arun(self, amount: float) -> Dict:
        raise NotImplementedError("Esta herramienta no soporta llamadas asíncronas.") 