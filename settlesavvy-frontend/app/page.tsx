
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <div className='flex min-h-screen flex-col'>
      <header className='bg-white shadow-sm'>
        <div className='container mx-auto flex h-16 items-center justify-between px-4'>
          <div className='text-2xl font-bold text-primary'>Settle Savvy</div>
          <div className='flex items-center gap-4'>
            <Link href='/auth/login'>
              <Button variant='outline'>Log In</Button>
            </Link>
            <Link href='/auth/register'>
              <Button>Sign Up</Button>
            </Link>
          </div>
        </div>
      </header>
      
      <main className='flex-1'>
        <section className='py-20 px-4 text-center bg-gradient-to-b from-blue-50 to-white'>
          <div className='container mx-auto max-w-3xl'>
            <h1 className='text-4xl md:text-5xl font-bold mb-6'>Find Your Perfect Neighborhood</h1>
            <p className='text-xl text-gray-600 mb-8'>
              Discover neighborhoods that match what matters most to you. School quality, commute time, 
              safety, affordability - you decide what's important.
            </p>
            <Link href='/auth/register'>
              <Button size='lg' className='text-lg px-8 py-6'>Get Started</Button>
            </Link>
          </div>
        </section>
        
        <section className='py-16 px-4 bg-white'>
          <div className='container mx-auto max-w-5xl'>
            <h2 className='text-3xl font-bold text-center mb-12'>How It Works</h2>
            <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
              <div className='text-center'>
                <div className='w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold'>1</div>
                <h3 className='text-xl font-semibold mb-2'>Define Your Preferences</h3>
                <p className='text-gray-600'>Select factors that matter to you and specify how they impact your decision.</p>
              </div>
              <div className='text-center'>
                <div className='w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold'>2</div>
                <h3 className='text-xl font-semibold mb-2'>Explore the Map</h3>
                <p className='text-gray-600'>View personalized neighborhood scores on an interactive map.</p>
              </div>
              <div className='text-center'>
                <div className='w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold'>3</div>
                <h3 className='text-xl font-semibold mb-2'>Connect with Realtors</h3>
                <p className='text-gray-600'>Find homes in your ideal neighborhoods with expert realtor assistance.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <footer className='bg-gray-50 py-8 px-4 border-t'>
        <div className='container mx-auto text-center text-gray-500'>
          <p>© {new Date().getFullYear()} Settle Savvy. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

