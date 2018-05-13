// import _ from 'lodash'

// import WebSocket from 'isomorphic-ws'

// import { eventChannel } from 'redux-saga'
import { all, call, cancelled, put, take, takeLatest } from 'redux-saga/effects'

import Actions from './actions'
import Api from './api'

import { api } from '../lib/redux_saga_utils'
// import config from '../client.config'
// import isServer from '../lib/is_server'


// if(!isServer()) {
//   const ws = new WebSocket(config.WEBSOCKET_URL, config.WEBSOCKET_PROTOCOL)
//
//   ws.onerror = () => {
//     console.log('ws.on(error)')
//   }
//
//   ws.onclose = () => {
//     console.log('ws.on(close)')
//   }
// }


function* refresh() {
  yield api(Actions.REFRESH_SUCCEEDED, Api.refresh)
}

// const createChannel = () => {
//   return eventChannel(emit => {
//     ws.onmessage = (message) => {
//       return emit(JSON.parse(message.data))
//     }
//
//     return () => {}
//   })
// }
//
// function* listenWebsockets() {
//   const channel = yield call(createChannel)
//
//   while(true) {
//     const action = yield take(channel)
//     yield put(action)
//   }
// }


function* clientSagas() {
  yield all([
    // call(listenWebsockets),
    takeLatest(Actions.REFRESH_REQUESTED, refresh),
  ])
}

function* serverSagas() {
  yield all([
    takeLatest(Actions.REFRESH_REQUESTED, refresh),
  ])
}

export { clientSagas, serverSagas }
