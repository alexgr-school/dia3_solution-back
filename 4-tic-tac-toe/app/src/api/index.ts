import axios, { AxiosResponse } from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8080',
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface BoardDataResponse {
    message?: string;
    board: number[][];
    current_player: number;
    winner: number | null;
}
export const getBoard = () => api.get<BoardDataResponse>('/board');

export const makeMove = async (
    cell: number,
    player: number
): Promise<BoardDataResponse> => {
    const response = await api.post<BoardDataResponse>('/move', {
        row: Math.floor(cell / 8),
        col: cell % 8,
        player,
    });

    return response.data; // Retourne les données de la réponse
};

interface ResetDataResponse {
    data: {
        message: string;
    };
}
export const resetBoard = () => api.post<ResetDataResponse>('/reset');
