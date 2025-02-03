// api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const sendMessage = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat/chat`, { message });
    return response.data.response;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};