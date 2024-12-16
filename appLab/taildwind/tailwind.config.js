/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../apps/attendance/form.py',
    '../apps/core/forms.py',
  ],
  theme: {
    extend: {
      fontFamily: {
        "exo": ['"exo 2"'],
        "rale": ['"Raleway"'],
      },
    },
  },
  plugins: [],
}

