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

export const fetchExperimentsByChannel = async (channel) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/experiments/channel/${channel}`);
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    return [];
  }
};

export const fetchBestExperimentByChannel = async (channel) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/experiments/channel/${channel}/best`);
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        return null;
    }
};