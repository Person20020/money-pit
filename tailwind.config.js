/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  	"./website/templates/**/*.html",
    "./website/static/**/*.css",
    "./website/static/**/*.js"
  ],
  theme: {
    extend: {
      boxShadow: {
        'custom-light': '0 0 10px rgba(0, 0, 0, 0.3), 0 0 50px rgba(255, 255, 255, 0.15)',
      }
    },
    screens: {
      '2xs': '25rem',
      'xs': '30rem'
    },
  },
  plugins: [],
}

