import dotenv from 'dotenv'
import path from 'path'

dotenv.config()

const modes = {
  production: 'production',
  development: 'development',
  testing: 'testing',
}

const MODE = process.env.NODE_ENV ? process.env.NODE_ENV.toLowerCase() : 'production'
const IS_DEVELOPMENT = MODE === modes.development
const IS_PRODUCTION = MODE === modes.production
const IS_TESTING = MODE === modes.testing

let config = {
  APP_NAME: 'blockchain-visualization',
  APP_NAME_FRIENDLY: 'Visual Blockchain',

  PUBLIC_PAGES: [
    '/',
    '/about',
  ],

  HTTP_PORT: process.env.HTTP_PORT,
  HTTP_HOST: process.env.HTTP_HOST,

  USE_SSL: process.env.USE_SSL,

  MODE,
  IS_DEVELOPMENT,
  IS_PRODUCTION,
  IS_TESTING,

  STATIC_DIR: path.join(__dirname, '../static'),

  LOG_DIR: process.env.LOG_DIR || path.join(__dirname, '../log'),
  LOG_ACCESS: process.env.LOG_ACCESS || 'access.log',
  LOG_ACCESS_VERBOSE: process.env.LOG_ACCESS_VERBOSE || false,

  PROTOCOL: 'http://',
  HOST: 'http://' + process.env.HOST,
  SERVER_ROOT: 'http://' + process.env.HOST,
  API_ROOT: 'http://' + process.env.HOST + '/api',
}

if(config.USE_SSL && config.USE_SSL !== 0) {
  config = {
    ...config,

    PROTOCOL: 'https://',
    HOST: 'https://' + process.env.HOST,

    SSL_KEY: process.env.SSL_KEY,
    SSL_CERT: process.env.SSL_CERT,
    SSL_CA: process.env.SSL_CA,
    SSL_PASSPHRASE: process.env.SSL_PASSPHRASE,
  }
}

// WARNING!!!
// This is the part of the config that will be exposed to the client-side
// JavaScript. Do not put any secrets here!
process.env['configClient'] = JSON.stringify({
  APP_NAME: config.APP_NAME,
  APP_NAME_FRIENDLY: config.APP_NAME_FRIENDLY,
  SERVER_ROOT: config.SERVER_ROOT,
  API_ROOT: config.API_ROOT,
})

export default config
