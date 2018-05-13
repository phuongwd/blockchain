import _ from 'lodash'

import datetime from '../common/datetime'

const createWebsocketsServer = (server, config) => {
  const WebSocket = require('ws')

  const wss = new WebSocket.Server({ server })

  wss.broadcast = (action) => {
    if(!action) {
      return
    }

    // const oldLength = wss.clients.size

    let clients = Array.from(wss.clients)

    // clients = _.filter(clients, client => {
    //   console.log(client.ip, client.isClosed)
    //   return !client.isClosed
    // })
    // clients = _.uniqBy(clients, 'ip')
    //
    // console.log('wss.clients.length: ', oldLength, ' -> ', clients.length)

    _.forEach(clients, client => {
      if(client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(action))
      }
    })
  }

  wss.on('connection', (client, req) => {
    const ip = req.connection.remoteAddress
    console.info(`${datetime()} wesocket connection: ${ip}`)
    // client.isClosed = false
    client.ip = ip

    // client.on('error', () => { client.isClosed = true })
    // client.on('close', () => { client.isClosed = true })
  })
  return wss
}

export default createWebsocketsServer
