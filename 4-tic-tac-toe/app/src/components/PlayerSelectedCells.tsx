import React from 'react';
import BlueCircle from './BlueCircle';
import RedCross from './RedCross';

type PlayerSelectedCellsProps = {
    player: 'player1' | 'player2';
    selectedCells: number[];
};

const PlayerSelectedCells = ({
    player,
    selectedCells,
}: PlayerSelectedCellsProps) => {
    return (
        <div className="flex flex-col justify-center items-center gap-2">
            <h3 className="text-mg font-bold mb-2">
                {player === 'player1' ? 'Player 1' : 'Player 2'}
            </h3>
            <div className="relative w-12 h-12 flex items-center justify-center border rounded-lg bg-gray-200 border-gray-200 dark:bg-gray-800 dark:border-gray-800">
                {player === 'player1' ? <RedCross /> : <BlueCircle />}
            </div>
            {/* <ul className="flex flex-col flex-wrap gap-1 max-h-80"> */}
            <ul className="grid grid-cols-10 xl:grid-cols-4 grid-rows-4 xl:grid-rows-10 grid-flow-row xl:grid-flow-col gap-1">
                {selectedCells.length === 0 && (
                    <li className="w-6 h-6">No cells selected</li>
                )}
                {selectedCells.map((cell) => (
                    <li className="w-6 h-6 text-right" key={cell}>
                        {cell + 1}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PlayerSelectedCells;
