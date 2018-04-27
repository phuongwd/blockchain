export default ('undefined' !== typeof window ? window.__configClient__ : JSON.parse(process.env['configClient']))
