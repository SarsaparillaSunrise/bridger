import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  test: {
    global: true,
    environment: "jsdom",
    setup: "./setupTest.ts",
  },
  plugins: [react()],
  server: {
    // Prevent browser from stealing focus upon encountering writev/write
    // hmr: false
    host: "0.0.0.0",
    port: 3000,
  },
});
