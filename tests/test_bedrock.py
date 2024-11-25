#from langchain_community.llms import Bedrock
from langchain_aws import BedrockLLM
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
inference_profile_arn = "arn:aws:bedrock:us-east-1:977098983325:inference-profile/us.meta.llama3-2-3b-instruct-v1:0"
llm = BedrockLLM(
    model_id=inference_profile_arn,
    region_name='us-east-1',
    provider='meta'
)
prompt = "escribe un poema sobre un gato"
response = llm(prompt)
print(response)