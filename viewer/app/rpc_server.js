import _ from 'lodash'

import grpc from 'grpc'


class BlockchainRpcServer {
  constructor({ controller, proto_path, service_name, package_name, host, port }) {
    this._controller = controller

    const proto = grpc.load(proto_path)[package_name][service_name]
    this._server = new grpc.Server()

    this._server.addService(proto.service, {
      ping: this.ping,
      getPeers: this._getHandlerWrapper(this._controller.peers),
      getTransactions: this._getHandlerWrapper(this._controller.transactions),
      getBlocks: this._getHandlerWrapper(this._controller.blocks),
      sendPeers: this._sendHandlerWrapper(this._controller.addPeers),
      sendTransactions: this._sendHandlerWrapper(this._controller.addTransactions),
      sendBlocks: this._sendHandlerWrapper(this._controller.addBlocks),
    })

    this._server.bind(`${host}:${port}`, grpc.ServerCredentials.createInsecure())
    console.info(`Listening on port: ${port}`)
    this._server.start()

  }

  ping = (call, callback) => {
    const message = _.get(call, 'request.message')
    callback(null, { message })
  }

  _getHandlerWrapper = (handler) => (
    (call) => {
      // Get items to be sent
      const items = handler()

      // Send items one by one
      _.forEach(items, (item) => {
        const response = { ...item }
        call.write(response)
      })

      // Close RPC call
      call.end()
    }
  )

  _sendHandlerWrapper = (handler) => (
    (call, callback) => {
      // Collect incoming items
      const items = []
      call.on('data', (item) => {
        items.push(item)
      })

      // Pass items to handler
      call.on('end', () => {
        handler(items)
        callback(null, {})
      })
    }
  )
}

export default BlockchainRpcServer
