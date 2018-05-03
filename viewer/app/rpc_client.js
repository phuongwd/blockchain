import grpc from 'grpc'

class BlockchainRpcClient {
  constructor({ proto_path, service_name, package_name, host, port }) {
    const proto = grpc.load(proto_path)[package_name][service_name]
    this._client = new proto(`${host}:${port}`, grpc.credentials.createInsecure())
  }

  _getWrapper(handler) {
    return () => {
      return new Promise((resolve, reject) => {
        const items = []
        const stream = this._client[handler]({})
        stream.on('error', reject)
        stream.on('data', (item) => items.push(item))
        stream.on('end', () => resolve(items))
      })
    }
  }

  _sendWrapper(handler) {
    return (items) => {
      new Promise((resolve, reject) => {
        // Open a stream and set response handler
        const stream = handler((error, response) => {
          if(error) {
            return reject(error)
          }
          return resolve(response)
        })

        // Write requests into the stream, one at a time
        items.map((item) => stream.write(item), (error) => {
          return reject(error)
        })

        // Close the stream
        stream.end()
      })
    }
  }

  getPeers = this._getWrapper('getPeers')

  sendPeers = this._sendWrapper('sendPeers')

  // getBlocks = this._getWrapper(this._client.getBlocks)
  //
  // sendBlocks = this._sendWrapper(this._client.getBlocks)
  //
  // getTransactions = this._getWrapper(this._client.getTransactions)
  //
  // sendTransactions = this._sendWrapper(this._client.getTransactions)
}

export default BlockchainRpcClient
