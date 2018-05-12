import path from 'path'

// import { docopt } from 'docopt'
// import docoptCleanse from 'docopt-cleanse'

import express from 'express'
import nextjs from 'next'

import createHttpServer from './http_server'
import createWebsocketServer from './websocket_server'
import BlockchainRpcServer from './rpc_server'
// import BlockchainRpcClient from './rpc_client'

import BlockchainController from './controller'

import config from './app.config'
import handleError from './lib/handle_error'
import nextjsRoutes from '../client/next.routes'

// const thisFile = 'app/' + path.basename(__filename)

// const doc = `
// Usage:
//   ${thisFile} seed [--host=<host>] [--port=<>port]
//   ${thisFile} full [--host=<host>] [--port=<>port] [--with-viewer]
//   ${thisFile} -h | --help | --version
// `
//
// const opt = docoptCleanse(docopt(doc, { version: '1.0.0' }))

const nextjs_app = nextjs({
  dir: 'client/',
  dev: config.IS_DEVELOPMENT,
  quiet: true,
})

nextjs_app.prepare()
  .then(() => {
    const controller = new BlockchainController()

    const httpServer = createHttpServer(config)
    const webSocketServer = createWebsocketServer(httpServer.server(), config)
    controller.setWebsocketServer(webSocketServer)

    const rpcServer = new BlockchainRpcServer({
      controller,
      proto_path: config.GRPC_PROTO_PATH,
      service_name: config.GRPC_SERVICE_NAME,
      package_name: config.GRPC_PACKAGE_NAME,
      host: config.GRPC_SERVER_HOST,
      port: config.GRPC_SERVER_PORT,
    })


    const router = httpServer.router()

    // Serve REST API for refreshing the data
    router.get('/api/refresh', (req, res) => {
      const data = controller.all()
      return res.sendJson({ data })
    })

    // Serve static content
    const staticHandler = (path) => {
      return express.static(path, { index: false })
    }

    router.use('/', staticHandler('.build/client'))
    router.use('/_next/static', staticHandler('.build/client/static'))

    router.use('/_next/-', staticHandler('.build/client'))
    router.use('/_next/*/-', staticHandler('.build/client'))

    router.use('/_next/-/page', staticHandler('.build/client/bundles/pages'))
    router.use('/_next/*/-/page', staticHandler('.build/client/bundles/pages'))

    // Serve Next.js dynamic content
    const nextjs_handler = nextjsRoutes.getRequestHandler(
      nextjs_app, ({ req, res, route, query }) => {
        return nextjs_app.render(req, res, route.page, query)
      })

    router.use(config.PUBLIC_PAGES, (req, res) => {
      return nextjs_handler(req, res)
    })

    if(config.IS_DEVELOPMENT) {
      router.get('/_next/*', (req, res) => {
        return nextjs_handler(req, res)
      })
    }

    // Send 404 if no matching route found
    router.use('*', (req, res) => {
      return res.sendStatus(404)
    })

    return httpServer.listen()
  })
  .then(console.info)
  .catch(handleError)

