import api from './api';

export const authService = {
  login: async (username, password) => {
    const response = await api.post('/api/login/', { username, password });
    
    const { access } = response.data;

    if (access) {
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    }

    return { success: true, token: access, data: response.data };
  },

  getPerfis: async (token) => {
    const response = await api.get('/api/perfis/', {
      headers: { 
        Authorization: `Bearer ${token}` 
      }
    });
    return response.data;
  },
};