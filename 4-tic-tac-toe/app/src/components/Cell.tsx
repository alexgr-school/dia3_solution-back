import React from 'react';
import RedCross from './RedCross';
import BlueCircle from './BlueCircle';

type CellProps = {
    index: number;
    player1SelectedCells: number[];
    player2SelectedCells: number[];
    handleCellClick: (index: number) => void;
};

const Cell = ({
    index,
    player1SelectedCells,
    player2SelectedCells,
    handleCellClick,
}: CellProps) => {
    return (
        <div
            className="relative w-12 h-12 flex items-center justify-center border rounded-lg bg-gray-100 border-gray-100 dark:bg-gray-600 dark:border-gray-600"
            onClick={() => handleCellClick(index)}
        >
            <div className="absolute text-gray-300 dark:text-gray-800 select-none">
                {index}
            </div>
            {player1SelectedCells.includes(index) && <RedCross />}
            {player2SelectedCells.includes(index) && <BlueCircle />}
        </div>
    );
};

export default Cell;
