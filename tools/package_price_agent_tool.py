# package_price_agent.py
import pandas as pd
from langchain.tools import BaseTool
from pydantic import Field

class PackagePriceAgentTool(BaseTool):
    name: str = Field(
        "PackagePriceAgent",
        description="Nombre de la herramienta para obtener precios de paquetes turísticos."
    )
    description: str = Field(
        "Obtiene información de precios de paquetes turísticos. Proporciona los detalles del paquete basado en el país, ciudad y moneda especificada.",
        description="Descripción de la herramienta para obtener precios de paquetes turísticos."
    )
    
    excel_path: str = Field(
        ...,
        description="Path to the Excel file containing package data."
    )
    
    packages_df: pd.DataFrame = Field(
        default_factory=pd.DataFrame,
        description="DataFrame containing package data."
    )
    
    def __init__(self, excel_path: str):
        super().__init__(excel_path=excel_path)
        self.packages_df = self.load_packages()
    
    def load_packages(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.excel_path)
            # Convertir columnas a minúsculas
            df.columns = [col.lower() for col in df.columns]
            # Limpiar símbolos de moneda y convertir a números usando raw strings
            df['cost_pesos'] = df['cost_pesos'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
            df['cost_dolares'] = df['cost_dolares'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
            return df
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            return pd.DataFrame()
    
    def _run(self, country: str, city: str, currency: str = "pesos") -> str:
        try:
            # Filtrar paquetes por país y ciudad
            filtered = self.packages_df[
                (self.packages_df['country'].str.lower() == country.lower()) &
                (self.packages_df['city'].str.lower() == city.lower())
            ]

            if filtered.empty:
                return "Paquete no encontrado para el país y ciudad especificados."

            package = filtered.iloc[0]
            price = package['cost_pesos'] if currency.lower() == 'pesos' else package['cost_dolares']

            response = (
                f"**Paquete Turístico**\n"
                f"País: {package['country']}\n"
                f"Ciudad: {package['city']}\n"
                f"Precio: ${price} {currency}\n"
                f"Requisitos: {package['requirements'] if pd.notnull(package['requirements']) else 'N/A'}\n"
                f"Descripción del Plan: {package['plan_description']}"
            )

            return response
        except Exception as e:
            return f"Error al obtener el precio del paquete: {e}"
    
    async def _arun(self, country: str, city: str, currency: str = "pesos") -> str:
        raise NotImplementedError("Esta herramienta no soporta llamadas asíncronas.")
