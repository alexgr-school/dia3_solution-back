import { Inter } from 'next/font/google';
import { useEffect, useState } from 'react';

import {
    GridDataResponse,
    MoveDataResponse,
    getGrid,
    makeMove,
    resetGrid,
    setMode,
} from '@/api';
import { Button } from '@/components/ui/button';
import Cell from '@/components/Cell';
import PlayerSelectedCells from '@/components/PlayerSelectedCells';
import AlertModal from '@/components/AlertModal';
import GameModeSwitch from '@/components/GameModeSwitch';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

const Home = () => {
    const [player1SelectedCells, setPlayer1SelectedCells] = useState<number[]>(
        []
    );
    const [player2SelectedCells, setPlayer2SelectedCells] = useState<number[]>(
        []
    );
    const [isPvEGameMode, setIsPvEGameMode] = useState<boolean>(false);
    const [winner, setWinner] = useState<number | null>(null);
    const [winningPositions, setWinningPositions] = useState<number[]>([]);
    const [isPlayer1Turn, setIsPlayer1Turn] = useState(true);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getGrid().then((res) => syncGrid(res.data));
    }, []);

    const handleCellClick = async (index: number) => {
        if (winner !== null) return;
        if (
            player1SelectedCells.includes(index) ||
            player2SelectedCells.includes(index)
        )
            return;
        try {
            if (isPvEGameMode) setLoading(true);
            const data = await makeMove(index, isPlayer1Turn ? 1 : 2);
            await syncGrid(data);
            if (isPvEGameMode) setLoading(false);
            console.log(data);
        } catch (error) {
            console.error(error.response.data.error);
            setError(error.response.data.error);
        }
    };

    const handleReset = async () => {
        setPlayer1SelectedCells([]);
        setPlayer2SelectedCells([]);
        setWinner(null);
        setIsPlayer1Turn(true);
        setWinningPositions([]);
        await resetGrid();
    };

    const handleGameModeChange = async () => {
        try {
            const newGameMode = isPvEGameMode ? 'pvp' : 'pve';
            await setMode(newGameMode);
            setIsPvEGameMode(!isPvEGameMode);
            await handleReset();
        } catch (error) {
            console.error(error.response.data.error);
            setError(error.response.data.error);
        }
    };

    const syncGrid = async (data: GridDataResponse | MoveDataResponse) => {
        const grid = data.grid;
        const player1Cells: number[] = [];
        const player2Cells: number[] = [];
        const localWinningPositions: number[] = [];

        grid.forEach((row: number[], rowIndex: number) => {
            row.forEach((cell: number, cellIndex: number) => {
                if (cell === 1) {
                    player1Cells.push(rowIndex * 8 + cellIndex);
                } else if (cell === 2) {
                    player2Cells.push(rowIndex * 8 + cellIndex);
                }
                if (
                    data.winning_cells?.some(
                        (pos) => pos[0] === rowIndex && pos[1] === cellIndex
                    ) &&
                    data.winner != 0
                ) {
                    localWinningPositions.push(rowIndex * 8 + cellIndex);
                }
            });
        });

        if (data.game_mode) setIsPvEGameMode(data.game_mode === 'pve');
        setPlayer1SelectedCells(player1Cells);
        setPlayer2SelectedCells(player2Cells);
        setWinner(data.winner);
        setWinningPositions(localWinningPositions);
        setIsPlayer1Turn(data.current_player === 1);
        setError(null);
    };

    return (
        <main
            className={`flex min-h-screen flex-col items-center justify-between p-10 xl:p-24 ${inter.className}`}
        >
            <div></div>

            <div className="flex flex-col items-center xl:flex-row xl:item justify-center gap-10 xl:gap-20 w-screen">
                {/* Game Info */}
                <div className="flex flex-col items-center xl:items-end gap-5 xl:gap-10">
                    <div className="flex flex-col items-end gap-2">
                        <h1 className="text-4xl font-bold">Tic Tac Toe</h1>
                        <p className="text-mg">
                            Click on the grid to select a cell.
                        </p>
                    </div>

                    <div className="flex xl:flex-col items-end gap-10">
                        <div className="flex flex-col items-end gap-1">
                            <h2 className="text-lg font-bold">Turn</h2>
                            <p>{isPlayer1Turn ? 'Player 1' : 'Player 2'}</p>
                        </div>

                        <div className="flex flex-col items-end gap-1">
                            <h2 className="text-lg font-bold">Winner</h2>
                            <p>
                                {winner === null
                                    ? 'No winner yet'
                                    : winner === 0
                                    ? 'Draw'
                                    : `Player ${winner}`}
                            </p>
                        </div>
                    </div>

                    <div>
                        <Button onClick={() => handleReset()}>Reset</Button>
                    </div>

                    <GameModeSwitch
                        checked={isPvEGameMode}
                        onChange={handleGameModeChange}
                    />

                    {error && <AlertModal title="Error" message={error} />}
                    {winner && (
                        <AlertModal
                            title="Winner"
                            message={
                                winner === 0
                                    ? 'Draw'
                                    : isPvEGameMode && winner === 2
                                    ? `AI has won!`
                                    : `Player ${winner}`
                            }
                            actionText="Reset"
                            actionFunction={handleReset}
                        />
                    )}

                    {loading && (
                        <div className="flex items-center gap-2">
                            <p>Loading...</p>
                            <div className="w-5 h-5 border-t-2 border-b-2 border-blue-500 rounded-full animate-spin"></div>
                        </div>
                    )}
                </div>

                {/* Tic Tac Toe Grid */}
                <div className="grid grid-cols-8 w-fit h-fit gap-2 bg-gray-300 dark:bg-gray-800 p-2 rounded-xl">
                    {Array.from({ length: 64 }).map((_, index) => (
                        <Cell
                            key={index}
                            index={index}
                            winningCell={
                                winningPositions.length > 0 &&
                                winningPositions.includes(index)
                            }
                            player1SelectedCells={player1SelectedCells}
                            player2SelectedCells={player2SelectedCells}
                            handleCellClick={handleCellClick}
                        />
                    ))}
                </div>

                {/* Selected Cells */}
                <div className="flex flex-col items-center gap-5">
                    <h2 className="text-lg font-bold">Selected Cells</h2>
                    <div className="flex items-center gap-10">
                        <PlayerSelectedCells
                            player="player1"
                            selectedCells={player1SelectedCells}
                        />
                        <hr className="w-0.5 min-h-48 xl:min-h-80 bg-gray-900 rounded-3xl" />
                        <PlayerSelectedCells
                            player="player2"
                            selectedCells={player2SelectedCells}
                        />
                    </div>
                </div>
            </div>

            <div></div>
        </main>
    );
};

export default Home;
