import axios from 'axios';

const API_BASE_URL = "http://localhost:8080/api";

export const fetchEvaluationsByChannel = async (channel) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/evaluations/channel/${channel}`);
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    return [];
  }
};