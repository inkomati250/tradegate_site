// Tailwind build for the TradeGate site. Rebuild with: bash scripts/build_css.sh
// Brand colours come from CSS variables set in base.html (editable in Site settings).
const path = require('path');
const root = path.resolve(__dirname, '..');
const v = (name) => `rgb(var(${name}) / <alpha-value>)`;
module.exports = {
  content: [
    path.join(root, 'website/templates/**/*.html'),
    path.join(root, 'website/**/*.py'),
  ],
  safelist: [{ pattern: /grid-cols-(1|2|3|4|5|6)/, variants: ['md', 'lg'] }],
  theme: {
    extend: {
      fontFamily: { display: ['Sora', 'sans-serif'], sans: ['DM Sans', 'sans-serif'] },
      colors: {
        brand: {
          primary: v('--tg-primary'), accent: v('--tg-accent'), muted: v('--tg-muted'),
          ink: '#07111F', copper: '#A56A43', ivory: '#F7F2EA',
        },
      },
      spacing: { 18: '4.5rem' },
      boxShadow: { soft: '0 20px 60px rgba(7,17,31,.10)', glow: '0 24px 80px rgba(214,179,106,.20)' },
    },
  },
};
