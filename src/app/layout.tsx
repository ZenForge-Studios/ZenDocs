import { RootProvider } from 'fumadocs-ui/provider/next';
import './global.css';
import { Geist } from 'next/font/google';
import type { Metadata } from 'next';

const geist = Geist({
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'ZenForge Docs',
  description: 'Documentación oficial y herramientas de desarrollo para servidores de Minecraft.',
  icons: {
    icon: [
      { url: '/logo.png', type: 'image/png' },
      { url: '/icon.png', type: 'image/png' },
    ],
    shortcut: '/logo.png',
    apple: '/logo.png',
  },
};

export default function Layout({ children }: LayoutProps<'/'>) {
  return (
    <html lang="es" className={geist.className} suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider
          search={{
            options: {
              api: '/api/search',
            },
          }}
        >
          {children}
        </RootProvider>
      </body>
    </html>
  );
}
