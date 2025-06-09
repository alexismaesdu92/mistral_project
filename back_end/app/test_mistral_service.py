import asyncio
import os
from services.mistral_service import MistralService

async def test_mistral_service():

    chatbot = MistralService()
    
    prompt = "Qu'est-ce que Mistral AI?"
    
    print(f"Envoi de la question: '{prompt}'")
    print("Attente de la réponse...")
    
    # Appeler la méthode generate_response
    response = await chatbot.generate_response(
        prompt=prompt,
        temperature=0.7,
        max_tokens=500
    )
    
    print("\nRéponse reçue:")
    print("-" * 50)
    print(response)
    print("-" * 50)
    
    return response

if __name__ == "__main__":

    response = asyncio.run(test_mistral_service())

    if response and not response.startswith("Error"):
        print("\nTest réussi! Le service fonctionne correctement.")
    else:
        print("\nTest échoué. Vérifiez les erreurs ci-dessus.")