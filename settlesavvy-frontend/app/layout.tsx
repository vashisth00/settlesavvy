import '@/app/globals.css';
import { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from '@/components/ui/sonner';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Settle Savvy - Find Your Perfect Neighborhood',
  description: 'Discover the perfect neighborhood for your next home based on what matters most to you',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='en'>
      <body className={inter.className}>
        {children}
        <Toaster />
      </body>
    </html>
  );
}