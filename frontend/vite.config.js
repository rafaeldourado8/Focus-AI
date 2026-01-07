import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Essencial para funcionar no Docker
    host: true, 
    strictPort: true,
    port: 5173, 
    // Correção para hot-reload no Windows/WSL2 via Docker
    watch: {
      usePolling: true,
    },
  },
})