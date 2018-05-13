import { applyMiddleware, createStore } from 'redux'
import createSagaMiddleware from 'redux-saga'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import config from '../client.config'

import reducer from './reducer'
import { clientSagas, serverSagas } from './sagas'
import Actions from './actions'

const sagaMiddleware = createSagaMiddleware()
const middleware = [sagaMiddleware, thunk]

if(!config.IS_PRODUCTION) {
  middleware.push(require('redux-immutable-state-invariant').default())
}

let enhancer = applyMiddleware(...middleware)
enhancer = composeWithDevTools(enhancer)

const initStore = (state, { isServer }) => {
  const store = createStore(
    reducer,
    state,
    enhancer,
  )

  if(isServer) {
    store.runSagaTask = () => {
      store.sagaTask = sagaMiddleware.run(serverSagas)
    }
  }
  else {
    store.runSagaTask = () => {
      store.sagaTask = sagaMiddleware.run(clientSagas)
    }
  }

  store.runSagaTask()

  return store
}

export default initStore
