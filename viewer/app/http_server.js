import fs from 'fs'
import http from 'http'
import spdy from 'spdy'
import sendJson from './lib/send_json'
import datetime from '../common/datetime'
import isXhr from './lib/is_xhr'
import requestLogger from './lib/request_logger'
import timestamp from '../common/timestamp'
import express from 'express'
import cookieParser from 'cookie-parser'
import bodyParser from 'body-parser'
import clientIP from './lib/client_ip'


const createHttpServer = (config) => {
  class HttpServer {
    constructor() {
      this._app = express()

      // Add timestamps for better logging
      this._app.use((req, res, next) => {
        req.begin = process.hrtime()
        req.beginDatetime = datetime()
        req.beginTimestamp = timestamp()
        return next()
      })

      // Disable common vulnerabilities
      this._app.disable('x-powered-by')
      this._app.disable('query parser')

      // Add convenience function to send JSON reply
      this._app.use(sendJson)

      // Add AJAX request detection for better logging
      this._app.use(isXhr)

      // Add client IP to request for better logging
      this._app.use((req, res, next) => {
        req.srcIP = clientIP(req)
        return next()
      })

      // Use body and cookie parsers
      this._app.use(bodyParser.json({
        limit: '1kb',
        type: ['json', 'application/json'],
      }))

      this._app.use(cookieParser())

      // Logger
      this._app.use(requestLogger({
        printFunc: console.info,
        maxFileSize: '100M',
        interval: '7d',
        verbose: config.LOG_ACCESS_VERBOSE,
      }))

      // If USE_SSL is 0, insecure HTTP/1.1 server will run.
      // If USE_SSL is 1, secure SLL HTTP/2 (Google's SPDY actually) server
      // will run.
      if(config.USE_SSL) {
        let serverOptions = {
          key: fs.readFileSync(config.SSL_KEY, { encoding: 'utf-8' }),
          cert: fs.readFileSync(config.SSL_CERT, { encoding: 'utf-8' }),
          passphrase: config.SSL_PASSPHRASE,
        }

        // If certificate authority chain file is provided, use it
        if(config.SSL_CA) {
          serverOptions = {
            ca: fs.readFileSync(config.SSL_CA, { encoding: 'utf-8' }),
          }
        }

        this._server = spdy.createServer(serverOptions, this._app)
      }
      else /*(!config.USE_SSL)*/ {
        this._server = http.createServer(this._app)
      }
    }

    server = () => {
      return this._server
    }

    router = () => {
      return this._app
    }

    listen = () => {
      return new Promise((resolve, reject) => {
        this._server.listen(config.HTTP_PORT, (err) => {
          if(err) {
            reject(err)
          }
          resolve(`Listening on ${config.PROTOCOL}${config.HTTP_HOST}:${config.HTTP_PORT}`)
        })
      })
    }
  }

  return new HttpServer
}

export default createHttpServer
