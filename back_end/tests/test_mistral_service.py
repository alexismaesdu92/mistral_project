import pytest
import asyncio
from unittest.mock import patch, MagicMock
from back_end.app.services.mistral_service import MistralService

@pytest.fixture
def mistral_service():
    return MistralService(model_name="mistral-large-latest")

@pytest.mark.asyncio
async def test_generate_response_success(mistral_service):
    # Créer un mock pour la réponse de l'API
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Ceci est une réponse de test"
    
    # Patcher la méthode chat_complete_async
    with patch.object(mistral_service, 'chat_complete_async', return_value=mock_response):
        response = await mistral_service.generate_response("Test question")
        
        # Vérifier que la réponse est correcte
        assert response == "Ceci est une réponse de test"
        
        # Vérifier que chat_complete_async a été appelé avec les bons arguments
        mistral_service.chat_complete_async.assert_called_once()
        args, kwargs = mistral_service.chat_complete_async.call_args
        assert kwargs["messages"][1]["content"] == "Test question"

@pytest.mark.asyncio
async def test_generate_response_error(mistral_service):
    # Patcher la méthode chat_complete_async pour lever une exception
    with patch.object(mistral_service, 'chat_complete_async', side_effect=Exception("Test error")):
        response = await mistral_service.generate_response("Test question")
        
        # Vérifier que l'erreur est correctement gérée
        assert response.startswith("Error generating response")
        assert "Test error" in response