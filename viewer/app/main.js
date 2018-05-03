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
    let app = express()
    const controller = new BlockchainController()

    const http = createHttpServer(controller, app, nextjs_app, config)
    const wss = createWebsocketServer(http, config)

    const rpcServer = new BlockchainRpcServer({
      controller,
      proto_path: config.GRPC_PROTO_PATH,
      service_name: config.GRPC_SERVICE_NAME,
      package_name: config.GRPC_PACKAGE_NAME,
      host: config.GRPC_SERVER_HOST,
      port: config.GRPC_SERVER_PORT,
    })

    // const rpcClient = new BlockchainRpcClient({
    //   controller,
    //   proto_path: config.GRPC_PROTO_PATH,
    //   service_name: config.GRPC_SERVICE_NAME,
    //   package_name: config.GRPC_PACKAGE_NAME,
    //   host: config.GRPC_SERVER_HOST,
    //   port: config.GRPC_SERVER_PORT,
    // })

    controller.setWebsocketServer(wss)
    // controller.setRpcClient(rpcClient)

    // rpcClient.getPeers([])

    http.listen(config.HTTP_PORT, (err) => {
      if(err) throw err
      console.info(
        `Listening on ${config.PROTOCOL}://${config.HTTP_HOST}:${config.HTTP_PORT}`,
      )
    })
  })
  .catch(handleError)

