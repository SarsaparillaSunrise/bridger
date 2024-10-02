import react from "@vitejs/plugin-react-swc";
import tailwindcss from "tailwindcss";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  test: {
    global: true,
    environment: "jsdom",
    setup: "./setupTest.ts",
  },
  plugins: [react()],
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: ["./tsconfig.json", "./tsconfig.node.json"],
    tsconfigRootDir: __dirname,
  },
  server: {
    // Prevent browser from stealing focus upon encountering writev/write
    // hmr: false
    host: "0.0.0.0",
    port: 3000,
  },
});
