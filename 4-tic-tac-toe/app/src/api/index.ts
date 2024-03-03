import axios, { AxiosResponse } from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8080',
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface BoardDataResponse {
    message?: string;
    game_mode: 'pvp' | 'pve';
    board: number[][];
    current_player: number;
    winning_positions?: number[][];
    winner: number | null;
}
export const getBoard = () => api.get<BoardDataResponse>('/board');

type SetModeDataResponse = {
    game_mode: 'pvp' | 'pve';
};
export const setMode = (mode: 'pvp' | 'pve') =>
    api.post<SetModeDataResponse>('/set_mode', { mode });

export interface MoveDataResponse {
    message?: string;
    game_mode: 'pvp' | 'pve';
    board: number[][];
    current_player: number;
    winner: number | null;
    winning_positions?: number[][];
    ai_move?: {
        row: number;
        col: number;
    };
}
export const makeMove = async (
    cell: number,
    player: number
): Promise<MoveDataResponse> => {
    const response = await api.post<MoveDataResponse>('/move', {
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
