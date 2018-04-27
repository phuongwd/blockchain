import path from 'path'
import fs from 'fs'
import express from 'express'
import nextjs from 'next'
import spdy from 'spdy'
import bodyParser from 'body-parser'
import cookieParser from 'cookie-parser'

import clientIP from './lib/client_ip'
import datetime from '../common/datetime'
import handleError from './lib/handle_error'
import isXhr from './lib/is_xhr'
import requestLogger from './lib/request_logger'
import sendJson from './lib/send_json'
import timestamp from '../common/timestamp'

import nextjsRoutes from '../client/next.routes'
import config from './app.config'

const nextjs_app = nextjs({
  dir: 'client/',
  dev: config.IS_DEVELOPMENT,
  quiet: true,
})

nextjs_app.prepare()
  .then(() => {
    let app = express()

    // Add timestamps for betetr logging
    app.use((req, res, next) => {
      req.begin = process.hrtime()
      req.beginDatetime = datetime()
      req.beginTimestamp = timestamp()
      return next()
    })

    // Disable common vulnerabilities
    app.disable('x-powered-by')
    app.disable('query parser')

    // Add convenience function to send JSON reply
    app.use(sendJson)

    // Add AJAX request detection for betetr logging
    app.use(isXhr)

    // Add _client IP to request for betetr logging
    app.use((req, res, next) => {
      req.srcIP = clientIP(req)
      return next()
    })

    // Use body and cookie parsers
    app.use(bodyParser.json({
      limit: '1kb',
      type: ['json', 'application/json'],
    }))

    app.use(cookieParser())

    // Logger
    app.use(requestLogger({
      printFunc: console.info,
      filename: path.join(config.LOG_DIR, config.LOG_ACCESS),
      maxFileSize: '100M',
      interval: '7d',
      verbose: config.LOG_ACCESS_VERBOSE,
    }))

    // Serve static content
    const staticHandler = (path) => {
      return express.static(path, { index: false })
    }

    app.use('/', staticHandler('.build/_client'))
    app.use('/_next/static', staticHandler('.build/_client/static'))

    app.use('/_next/-', staticHandler('.build/_client'))
    app.use('/_next/*/-', staticHandler('.build/_client'))

    app.use('/_next/-/page', staticHandler('.build/_client/bundles/pages'))
    app.use('/_next/*/-/page', staticHandler('.build/_client/bundles/pages'))

    // Serve Next.js dynamic content
    const nextjs_handler = nextjsRoutes.getRequestHandler(
      nextjs_app, ({ req, res, route, query }) => {
        return nextjs_app.render(req, res, route.page, query)
      })

    app.use(config.PUBLIC_PAGES, (req, res) => {
      return nextjs_handler(req, res)
    })

    if(config.IS_DEVELOPMENT) {
      app.get('/_next/*', (req, res) => {
        return nextjs_handler(req, res)
      })
    }

    // Send 404 if nothing found
    app.use('*', (req, res) => {
      return res.sendStatus(404)
    })

    // Setup a server and listen.
    // If USE_SSL is 0, insecure HTTP/1.1 server will run.
    // If USE_SSL is 1, secure SLL HTTP/2 (Google's SPDY actually) server will
    // run.
    let protocol = 'http'
    let serverOptions = {}
    if(config.USE_SSL !== '0') {
      // Using secure HTTPS connection requires SSL certificate and key files
      protocol = 'https'
      serverOptions = {
        ...serverOptions,
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

      app = spdy.createServer(serverOptions, app)
    }

    app.listen(config.HTTP_PORT, (err) => {
      if(err) throw err
      console.info(
        `Listening on ${protocol}://${config.HTTP_HOST}:${config.HTTP_PORT}`
      )
    })


  })
  .catch(handleError)

