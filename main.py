from fastapi import FastAPI
from pydantic import BaseModel
from core.single_agent_setup import get_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Modelo de datos para la petición
class Query(BaseModel):
    message: str

# Modelo de datos para la respuesta
class Response(BaseModel):
    response: str

# Inicializar el agente una sola vez
agent = get_agent()

@app.get("/")
def root_page():
    return Response(response="Alive")


@app.post("/chat", response_model=Response)
async def chat_with_agent(query: Query):
    try:
        response = agent.run(query.message)
        return Response(response=response)
    except Exception as e:
        return Response(response=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50160)