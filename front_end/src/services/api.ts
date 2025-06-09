import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface Message {
  role: string;
  content: string;
}

export const apiService = {
  async sendChatMessage(messages: Message[], useRag: boolean): Promise<string> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat/complete`, {
        messages,
        useRag
      });
      
      return response.data.response;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw new Error('Failed to send message. Please try again later.');
    }
  }
};
