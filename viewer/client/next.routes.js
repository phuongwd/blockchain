const routes = module.exports = require('next-routes')()

routes
  .add('/', 'index')
  .add('/blocks', 'index')
  .add('nodes')
  .add('transactions')
