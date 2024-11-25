from langchain_aws import BedrockLLM
import os
from dotenv import load_dotenv
# Cargar variables de entorno
load_dotenv()
inference_profile_arn = "arn:aws:bedrock:us-east-1:977098983325:inference-profile/us.meta.llama3-1-70b-instruct-v1:0"
def get_llama3_2_3b_instruct_bedrock_llm():
    llm = BedrockLLM(
        model_id=inference_profile_arn,
        region_name='us-east-1',
        provider='meta'
    )
    llm.provider_stop_sequence_key_name_map['meta'] = ''
    return llm

