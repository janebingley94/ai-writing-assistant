import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
    "./types/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ["var(--font-display)", "ui-sans-serif", "system-ui"],
        body: ["var(--font-body)", "ui-sans-serif", "system-ui"],
      },
      colors: {
        slate: {
          50: "#f5f7fb",
          100: "#e8edf5",
          200: "#d1dceb",
          300: "#b3c1de",
          400: "#8e9fcd",
          500: "#6f7eb8",
          600: "#5b6698",
          700: "#4a527b",
          800: "#3f4665",
          900: "#363d57",
        },
        amber: {
          50: "#fff6e5",
          100: "#ffe6b8",
          200: "#ffd58a",
          300: "#ffc45e",
          400: "#f5ab35",
          500: "#e19012",
          600: "#c3770a",
          700: "#9c5f07",
          800: "#7a4a06",
          900: "#5e3904",
        },
        ink: {
          50: "#f7f3ee",
          100: "#efe7da",
          200: "#d9cab2",
          300: "#bca37e",
          400: "#a1845d",
          500: "#86684c",
          600: "#6e5640",
          700: "#5a4735",
          800: "#4b3b2e",
          900: "#3d3026",
        },
      },
      boxShadow: {
        glass: "0 20px 60px -30px rgba(42, 46, 80, 0.5)",
      },
    },
  },
  plugins: [],
};

export default config;
