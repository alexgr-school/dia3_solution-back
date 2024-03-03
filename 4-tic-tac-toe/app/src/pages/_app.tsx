import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import { cn } from '@/lib/utils';

const fontSans = Inter({ subsets: ['latin'], variable: '--font-sans' });

export default function App({ Component, pageProps }: AppProps) {
    return (
        <Component
            className={cn(
                'min-h-screen bg-background font-sans antialiased',
                fontSans.variable
            )}
            {...pageProps}
        />
    );
}
