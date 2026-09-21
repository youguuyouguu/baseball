import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: Number(process.env.PORT) || 5173,
    allowedHosts: ['baseball-production-ad28.up.railway.app'],
     proxy: {
      '/api': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
});