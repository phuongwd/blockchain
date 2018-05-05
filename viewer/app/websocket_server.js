import datetime from '../common/datetime'

const createWebsocketsServer = (server, config) => {
  const WebSocket = require('ws')

  const wss = new WebSocket.Server({ server })

  wss.broadcast = (action) => {
    if(!action) {
      return
    }

    wss.clients.forEach(function each(client) {
      if(client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(action))
      }
    })
  }

  wss.on('connection', (ws, req) => {
    const ip = req.connection.remoteAddress
    console.info(`${datetime()} Peer ${ip} requested connection.`)
  })

  return wss
}

export default createWebsocketsServer
