import WebSocket from 'isomorphic-ws'

import { eventChannel } from 'redux-saga'
import { all, call, put, take, takeLatest } from 'redux-saga/effects'

import Actions from './actions'
import Api from './api'

import { api } from '../lib/redux_saga_utils'
import config from '../client.config'

function* refresh() {
  console.info('SAGA: refresh')
  yield api(Actions.REFRESH_SUCCEEDED, Api.refresh)
}


function* listenWebsockets() {
  const channel = new eventChannel(emit => {
    const ws = new WebSocket(config.WEBSOCKET_URL, config.WEBSOCKET_PROTOCOL)

    ws.onmessage = (message) => {
      return emit(JSON.parse(message.data))
    }

    return ws.close
  })

  while(true) {
    const action = yield take(channel)
    yield put(action)
  }
}


function* clientOnlySagas() {
  yield all([
    call(listenWebsockets),
  ])
}

function* clientServerSagas() {
  yield all([
    takeLatest(Actions.REFRESH_REQUESTED, refresh),
  ])
}

export { clientOnlySagas, clientServerSagas }
