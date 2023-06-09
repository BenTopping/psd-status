/** @type {import('tailwindcss').Config} */

const defaultOptions = require("@sanger/ui-styling/tailwind.config.js");

export default {
  ...defaultOptions,
  content: [
    ...defaultOptions.content,
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  safelist: ["bg-gray-400"],
  theme: {
    ...defaultOptions.theme,
    extend: {},
  },
  plugins: [],
};
