import path from 'path'

import _ from 'lodash'

const dotenv = require('dotenv')
dotenv.config()

const dotenvExtended = require('dotenv-extended')
const dotenvParseVariables = require('dotenv-parse-variables')

let envFromFile = dotenvExtended.load({
  silent: false,
})

const env = dotenvParseVariables(_.merge({}, process.env, envFromFile))

const rootDir = path.join(__dirname, '..')

const modes = {
  production: 'production',
  development: 'development',
  testing: 'testing',
}

const MODE = env.NODE_ENV ? env.NODE_ENV.toLowerCase() : 'production'
const IS_DEVELOPMENT = MODE === modes.development
const IS_PRODUCTION = MODE === modes.production
const IS_TESTING = MODE === modes.testing

let config = {
  APP_NAME: env.APP_NAME,
  APP_NAME_FRIENDLY: env.APP_NAME_FRIENDLY,

  PUBLIC_PAGES: [
    '/',
    '/about',
  ],

  HTTP_PORT: `${env.HTTP_PORT}`,
  HTTP_HOST: env.HTTP_HOST,

  USE_SSL: env.USE_SSL,

  MODE,
  IS_DEVELOPMENT,
  IS_PRODUCTION,
  IS_TESTING,

  ROOT_DIR: rootDir,
  STATIC_DIR: path.join(rootDir, 'static'),
  // LOG_DIR: env.LOG_DIR || path.join(rootDir, 'log'),
  // LOG_ACCESS: env.LOG_ACCESS || 'access.log',
  // LOG_ACCESS_VERBOSE: env.LOG_ACCESS_VERBOSE || false,

  PROTOCOL: 'http://',
  HOST: 'http://' + env.HOST,
  SERVER_ROOT: 'http://' + env.HOST,
  API_ROOT: 'http://' + env.HOST + '/api',

  GRPC_PROTO_PATH: env.GRPC_PROTO_PATH,
  GRPC_SERVICE_NAME: env.GRPC_SERVICE_NAME,
  GRPC_PACKAGE_NAME: env.GRPC_PACKAGE_NAME,
  GRPC_SERVER_HOST: env.GRPC_SERVER_HOST,
  GRPC_SERVER_PORT: env.GRPC_SERVER_PORT,

  WEBSOCKET_URL: `ws://${env.HOST}/`,
  WEBSOCKET_PROTOCOL: `${env.APP_NAME.toLowerCase()}-protocol`,
}

if(config.USE_SSL) {
  config = _.merge(config, {
    PROTOCOL: 'https://',
    HOST: 'https://' + env.HOST,
    SSL_KEY: env.SSL_KEY,
    SSL_CERT: env.SSL_CERT,
    SSL_CA: env.SSL_CA,
    SSL_PASSPHRASE: env.SSL_PASSPHRASE,
  })
}

// WARNING!!!
// This is the part of the config that will be exposed to the client-side
// JavaScript. Do not put any secrets here!
process.env['configClient'] = JSON.stringify({
  MODE,
  IS_DEVELOPMENT,
  IS_PRODUCTION,
  IS_TESTING,
  APP_NAME: config.APP_NAME,
  APP_NAME_FRIENDLY: config.APP_NAME_FRIENDLY,
  SERVER_ROOT: config.SERVER_ROOT,
  API_ROOT: config.API_ROOT,
  WEBSOCKET_URL: config.WEBSOCKET_URL,
  WEBSOCKET_PROTOCOL: config.WEBSOCKET_PROTOCOL,
})

export default config
