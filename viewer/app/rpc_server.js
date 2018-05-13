import _ from 'lodash'

import grpc from 'grpc'


class BlockchainRpcServer {
  constructor({ controller, proto_path, service_name, package_name, host, port }) {
    this._host = host
    this._port = port

    // Hardcoded address
    // (hardcoded address is fine as long as we run only one instance,
    // also this node does not generate any transactions, so we don't need
    // to bother with keys and signatures)
    this._address = Buffer.from('B4jFTP934QZFEQRsDdrYqfA2J7vZuP1h4')

    this._controller = controller

    const proto = grpc.load(proto_path)[package_name][service_name]
    this._server = new grpc.Server()

    this._server.addService(proto.service, {
      ping: this.ping,
      getPeers: this._getHandlerWrapper(() => []),
      getTransactions: this._getHandlerWrapper(() => []),
      getBlocks: this._getHandlerWrapper(() => []),
      sendPeers: this._sendHandlerWrapper(this._controller.addPeers),
      sendTransactions: this._sendHandlerWrapper(this._controller.addTransactions),
      sendBlocks: this._sendHandlerWrapper(this._controller.addBlocks),
    })

    this._server.bind(`${host}:${port}`, grpc.ServerCredentials.createInsecure())
    console.info(`Listening on port: ${port}`)
    this._server.start()
  }

  ping = (call, callback) => {
    const node = {
      host: this._host,
      port: this._port,
      address: this._address,
    }
    callback(null, { node })
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
