import { Inter } from 'next/font/google';
import { useState } from 'react';

import Cell from '@/components/Cell';
import PlayerSelectedCells from '@/components/PlayerSelectedCells';
import exp from 'constants';

const inter = Inter({ subsets: ['latin'] });

const Home = () => {
    const [player1SelectedCells, setPlayer1SelectedCells] = useState<number[]>(
        []
    );
    const [player2SelectedCells, setPlayer2SelectedCells] = useState<number[]>(
        []
    );
    const [winner, setWinner] = useState<number | null>(null);
    const [isPlayer1Turn, setIsPlayer1Turn] = useState(true);

    const handleCellClick = (index: number) => {
        if (winner !== null) return;
        if (
            player1SelectedCells.includes(index) ||
            player2SelectedCells.includes(index)
        )
            return;

        if (isPlayer1Turn) {
            setPlayer1SelectedCells((prev) => [...prev, index]);
            setIsPlayer1Turn(false);
        } else {
            setPlayer2SelectedCells((prev) => [...prev, index]);
            setIsPlayer1Turn(true);
        }

        if (player1SelectedCells.length + player2SelectedCells.length >= 63) {
            setWinner(-1);
            return;
        }
    };

    return (
        <main
            className={`flex min-h-screen flex-col items-center justify-between p-10 lg:p-24 ${inter.className}`}
        >
            <div></div>

            <div className="flex flex-col items-center lg:flex-row lg:item justify-center gap-10 lg:gap-20 w-screen">
                {/* Game Info */}
                <div className="flex flex-col items-center lg:items-end gap-5 lg:gap-10">
                    <div className="flex flex-col items-end gap-2">
                        <h1 className="text-4xl font-bold">Tic Tac Toe</h1>
                        <p className="text-mg">
                            Click on the grid to select a cell.
                        </p>
                    </div>

                    <div className="flex lg:flex-col items-end gap-10">
                        <div className="flex flex-col items-end gap-1">
                            <h2 className="text-lg font-bold">Turn</h2>
                            <p>{isPlayer1Turn ? 'Player 1' : 'Player 2'}</p>
                        </div>

                        <div className="flex flex-col items-end gap-1">
                            <h2 className="text-lg font-bold">Winner</h2>
                            <p>
                                {winner === null
                                    ? 'No winner yet'
                                    : winner === -1
                                    ? 'Draw'
                                    : `Player ${winner}`}
                            </p>
                        </div>
                    </div>

                    <div>
                        <button
                            className="px-4 py-2 rounded-lg bg-gray-300 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
                            onClick={() => {
                                setPlayer1SelectedCells([]);
                                setPlayer2SelectedCells([]);
                                setWinner(null);
                                setIsPlayer1Turn(true);
                            }}
                        >
                            Reset
                        </button>
                    </div>
                </div>

                {/* Tic Tac Toe Grid */}
                <div className="grid grid-cols-8 w-fit h-fit gap-2 bg-gray-300 dark:bg-gray-800 p-2 rounded-xl">
                    {Array.from({ length: 64 }).map((_, index) => (
                        <Cell
                            key={index}
                            index={index}
                            player1SelectedCells={player1SelectedCells}
                            player2SelectedCells={player2SelectedCells}
                            handleCellClick={handleCellClick}
                        />
                    ))}
                </div>

                {/* Selected Cells */}
                <div className="flex flex-col gap-5">
                    <h2 className="text-lg font-bold">Selected Cells</h2>
                    <div className="flex gap-10">
                        <PlayerSelectedCells
                            player="player1"
                            selectedCells={player1SelectedCells}
                        />
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
