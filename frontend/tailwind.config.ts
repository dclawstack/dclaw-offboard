import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: "#64748B",
      },
    },
  },
  plugins: [],
};

export default config;
