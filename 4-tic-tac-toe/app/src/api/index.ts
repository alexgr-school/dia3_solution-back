import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8080',
});

type Cell = {
    index: number;
    player: 'player1' | 'player2';
};

const getAICell = () => api.post('/ai', {});

export default api;
