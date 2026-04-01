import api from './api';

export const authService = {
  login: async (username, password) => {
    // Certifique-se de usar a URL completa configurada no seu urls.py
    const response = await api.post('/api/login/', { username, password });
    
    const { access } = response.data;

    if (access) {
      // Configura o token para TODAS as próximas chamadas imediatamente
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    }

    return { success: true, token: access, data: response.data };
  },

  // Removi a duplicata e padronizei a URL
  getPerfis: async (token) => {
    const response = await api.get('/api/perfis/', {
      headers: { 
        Authorization: `Bearer ${token}` 
      }
    });
    return response.data;
  },
};