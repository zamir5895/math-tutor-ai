import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

tema = "Ecuaciones Lineales"  # Variable modificable
grado = "2"            # Variable modificable

# Generamos el prompt de búsqueda para YouTube (solo el texto)
youtube_prompt = (
    f"{tema} para estudiantes de {grado} grado de secundaria: "
  
    
)

print("Texto para buscar en YouTube:")
print(youtube_prompt)

# Si quieres que el modelo refine el prompt (opcional):
response = client.complete(
    messages=[
        SystemMessage("Eres un asistente que ayuda a crear prompts de búsqueda efectivos para YouTube."),
        UserMessage(f"Genera un texto para para buscar en YouTube y sea efectiva la busqueda. Solo devuelve el promt: '{youtube_prompt}'")
    ],
    model=model
)

# Imprime la respuesta del modelo (si la necesitas)
print("\nRespuesta optimizada del modelo:")
print(response.choices[0].message.content)