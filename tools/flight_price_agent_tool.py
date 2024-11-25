from serpapi import GoogleSearch
import re
from langchain.tools import BaseTool
from pydantic import Field, BaseModel

class FlightPriceAgentTool(BaseModel):
    name: str = Field(
        "FlightPriceAgent",
        description="Nombre de la herramienta para buscar precios de vuelos."
    )
    description: str = Field(
        "Busca el vuelo más barato utilizando SerpAPI. Proporciona detalles del vuelo más económico basado en la consulta de búsqueda.",
        description="Descripción de la herramienta para buscar precios de vuelos."
    )
    serpapi_key: str
    
    def _run(self, query: str) -> str:
        """
        Busca el vuelo más barato en Google usando SerpAPI.

        Args:
            query (str): Consulta de búsqueda (ejemplo: "vuelo desde Cali a Cartagena para el 28 de noviembre y volver el 3 de diciembre").

        Returns:
            str: Información del vuelo más barato encontrado o un mensaje de error.
        """
        #print(query)
        # Configuración de los parámetros para la API
        params = {
            "q": query,
            "hl": "es",
            "gl": "co",  # Cambiar a la región adecuada
            "google_domain": "google.com",
            "api_key": self.serpapi_key
        }
        
        try:
            # Realiza la búsqueda en Google
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extraer la sección de vuelos
            flights_data = results.get("answer_box", {}).get("flights", [])
            #print(flights_data)
            if not flights_data:
                return "No se encontraron vuelos en la respuesta."


            #def extract_price(price_str):
            #    print(price_str)
            #    match = re.search(r'from \$(\d+)', price_str)
            #    return float(match.group(1)) if match else float('inf')
            def extract_price(price_str):
                #print(price_str)
                # Ajustar la expresión regular para manejar ambos casos
                match = re.search(r'(?:desde \$|from \$)\s?([\d,.]+)', price_str, re.IGNORECASE)
                if match:
                    # Eliminar los separadores de miles (si existen) y convertir a float
                    return float(match.group(1).replace('.', '').replace(',', '.'))
                return float('inf')  # Retornar infinito si no se encuentra un precio válido
            # Inicializar variables para el vuelo más barato
            min_price = float('inf')
            min_price_flight = None

            # Buscar el vuelo más barato
            for flight in flights_data:
                try:
                    price = extract_price(flight['flight_info'][3])  # Precio en índice 3
                    if price < min_price:
                        min_price = price
                        min_price_flight = flight
                except (IndexError, KeyError):
                    print(f"Error procesando vuelo: {flight}")
            
            print("precio mas barato-----")
            #print(min_price_flight)
            
            # Retornar el vuelo más barato si existe
            if min_price_flight:
                return {
                    "airline": min_price_flight['flight_info'][0],
                    "duration": min_price_flight['flight_info'][1],
                    "flight_type": min_price_flight['flight_info'][2],
                    "price": min_price,
                    "link": min_price_flight.get('link', 'No link available')
                }
            else:
                print("No se encontraron vuelos con precios válidos.")
                return None    
        except Exception as e:
            return f"Error al buscar vuelos: {e}"
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Esta herramienta no soporta llamadas asíncronas.")
