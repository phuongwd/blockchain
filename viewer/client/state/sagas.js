import _ from 'lodash'

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


const createChannel = () => {
  return new eventChannel(emit => {
    const ws = new WebSocket(config.WEBSOCKET_URL, config.WEBSOCKET_PROTOCOL)

    ws.onmessage = (message) => {
      return emit(JSON.parse(message.data))
    }

    return ws.close
  })
}

function* listenWebsockets() {
  const channel = yield call(createChannel)

  while(true) {
    const action = yield take(channel)
    yield put(action)
  }
}


function* websocketSagas() {
  yield all([
    call(listenWebsockets),
  ])
}

function* normalSagas() {
  yield all([
    takeLatest(Actions.REFRESH_REQUESTED, refresh),
  ])
}

export { websocketSagas, normalSagas }
