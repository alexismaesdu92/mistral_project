import { useState, useCallback } from 'react';
import { apiService } from '../services/api';

interface Message {
    role: string;
    content: string;
}

interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string, useRag: boolean) => Promise<void>;
  clearMessages: () => void;
}

export const useChat = (): UseChatReturn => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);


  const sendMessage = useCallback(async (content: string, useRag: boolean) => {
    try {

      setError(null);
      
      const userMessage: Message = { role: 'user', content };
      setMessages(prevMessages => [...prevMessages, userMessage]);
      
      setIsLoading(true);
      

      const allMessages = [...messages, userMessage];
      

      const response = await apiService.sendChatMessage(allMessages, useRag);
      

      const assistantMessage: Message = { role: 'assistant', content: response };
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (err) {

      const errorMessage = err instanceof Error ? err.message : 'Une erreur est survenue';
      setError(errorMessage);
      console.error('Erreur lors de l\'envoi du message:', err);
    } finally {

      setIsLoading(false);
    }
  }, [messages]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages
  };
};
