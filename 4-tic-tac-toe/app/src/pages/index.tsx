import Image from 'next/image';
import { Inter } from 'next/font/google';
import { useState } from 'react';

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
    const [player1SelectedCells, setPlayer1SelectedCells] = useState<number[]>(
        []
    );
    const [player2SelectedCells, setPlayer2SelectedCells] = useState<number[]>(
        []
    );
    const [winner, setWinner] = useState<number | null>(null);
    const [isPlayer1Turn, setIsPlayer1Turn] = useState(true);

    const handleCellClick = (index: number) => {
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
    };

    return (
        <main
            className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
        >
            <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
                <p className="fixed left-0 top-0 flex w-full justify-center border-b font-bold border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
                    Tic Tac Toe
                </p>
            </div>

            <div className="flex gap-10">
                <div className="grid grid-cols-8 gap-2 bg-gray-600 p-2 rounded-xl">
                    {Array.from({ length: 64 }).map((_, index) => (
                        <div
                            key={index}
                            className="relative w-12 h-12 bg-white flex items-center justify-center border border-gray-200 rounded-lg dark:border-neutral-800/30 dark:bg-neutral-800/30"
                            onClick={() => handleCellClick(index)}
                        >
                            {player1SelectedCells.includes(index) && (
                                <>
                                    <div className="h-8 w-1 bg-red-500 absolute transform -rotate-45 rounded"></div>
                                    <div className="h-8 w-1 bg-red-500 absolute transform rotate-45 rounded"></div>
                                </>
                            )}
                            {player2SelectedCells.includes(index) && (
                                <div className="w-8 h-8 border-4 border-blue-500 rounded-full"></div>
                            )}
                        </div>
                    ))}
                </div>

                <div className="flex gap-5">
                    <div>
                        <h2 className="text-mg font-bold mb-2">Player 1</h2>
                        <div className="relative w-12 h-12 bg-white flex items-center justify-center border mb-5 border-gray-200 rounded-lg dark:border-neutral-800/30 dark:bg-neutral-800/30">
                            <div className="h-8 w-1 bg-red-500 absolute transform -rotate-45 rounded"></div>
                            <div className="h-8 w-1 bg-red-500 absolute transform rotate-45 rounded"></div>
                        </div>
                        <ul>
                            {player1SelectedCells.map((cell) => (
                                <li key={cell}>{cell}</li>
                            ))}
                        </ul>
                    </div>
                    <div>
                        <h2 className="text-mg font-bold mb-2">Player 2</h2>
                        <div className="relative w-12 h-12 bg-white flex items-center justify-center border mb-5 border-gray-200 rounded-lg dark:border-neutral-800/30 dark:bg-neutral-800/30">
                            <div className="w-8 h-8 border-4 border-blue-500 rounded-full"></div>
                        </div>
                        <ul>
                            {player2SelectedCells.map((cell) => (
                                <li key={cell}>{cell}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
                <a
                    href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
                    className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <h2 className={`mb-3 text-2xl font-semibold`}>
                        Docs{' '}
                        <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                            -&gt;
                        </span>
                    </h2>
                    <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                        Find in-depth information about Next.js features and
                        API.
                    </p>
                </a>
            </div>
        </main>
    );
}
