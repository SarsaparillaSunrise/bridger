import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Prevent browser from stealing focus upon encountering writev/write
  // server: {hmr: false},
})
