import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const api = {
  checkHealth: async () => {
    const res = await client.get('/health');
    return res.data;
  },

  predictRisk: async (payload) => {
    const res = await client.post('/predict-risk', payload);
    return res.data;
  },

  diagnoseLeaf: async (formData) => {
    const res = await client.post('/diagnose', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  getRecommendation: async (diseaseId) => {
    const res = await client.get(`/recommend/${diseaseId}`);
    return res.data;
  },

  getDashboardData: async (cropFilter = null, alertFilter = null) => {
    const params = {};
    if (cropFilter && cropFilter !== 'ALL') params.crop_filter = cropFilter;
    if (alertFilter && alertFilter !== 'ALL') params.alert_filter = alertFilter;
    const res = await client.get('/dashboard-data', { params });
    return res.data;
  }
};
