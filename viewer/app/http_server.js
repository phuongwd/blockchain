import fs from 'fs'
import path from  'path'
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
import nextjsRoutes from '../client/next.routes'


const createHttpServer = (controller, app, nextjs_app, config) => {
  // Add timestamps for better logging
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

  // Add AJAX request detection for better logging
  app.use(isXhr)

  // Add client IP to request for better logging
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
    maxFileSize: '100M',
    interval: '7d',
    verbose: config.LOG_ACCESS_VERBOSE,
  }))

  // Serve static content
  const staticHandler = (path) => {
    return express.static(path, { index: false })
  }

  app.get('/api/refresh', (req, res) => {
    const data = controller.all()
    return req.sendJson({ data })
  })

  app.use('/', staticHandler('.build/client'))
  app.use('/_next/static', staticHandler('.build/client/static'))

  app.use('/_next/-', staticHandler('.build/client'))
  app.use('/_next/*/-', staticHandler('.build/client'))

  app.use('/_next/-/page', staticHandler('.build/client/bundles/pages'))
  app.use('/_next/*/-/page', staticHandler('.build/client/bundles/pages'))

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

  // If USE_SSL is 0, insecure HTTP/1.1 server will run.
  // If USE_SSL is 1, secure SLL HTTP/2 (Google's SPDY actually) server will
  // run.
  let server = null
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

    server = spdy.createServer(serverOptions, app)
  }
  else /*(!config.USE_SSL)*/ {
    server = http.createServer(app)
  }

  return server
}

export default createHttpServer
