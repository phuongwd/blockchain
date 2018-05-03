import { applyMiddleware, createStore } from 'redux'
import createSagaMiddleware from 'redux-saga'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import config from '../client.config'

import reducer from './reducer'
import { clientOnlySagas, clientServerSagas } from './sagas'

const sagaMiddleware = createSagaMiddleware()
const middleware = [sagaMiddleware, thunk]

if(!config.IS_PRODUCTION) {
  middleware.push(require('redux-immutable-state-invariant').default())
}

let enhancer = applyMiddleware(...middleware)
enhancer = composeWithDevTools(enhancer)

const initStore = (state, { isServer, req, query }) => {
  const store = createStore(
    reducer,
    state,
    enhancer,
  )

  if(isServer) {
    store.runSagaTask = () => {
      store.sagaTask = sagaMiddleware.run(clientServerSagas)
    }
  }
  else {
    store.runSagaTask = () => {
      store.sagaTask = sagaMiddleware.run(clientOnlySagas)
      store.sagaTask = sagaMiddleware.run(clientServerSagas)
    }
  }

  store.runSagaTask()

  return store
}

export default initStore
