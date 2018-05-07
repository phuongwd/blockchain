import { put, call } from 'redux-saga/effects'

export function* act(type, payload, error) {
  yield put({ type, payload: payload || null, error: error || false })
}

export function* api(successAction, apiFunc, ...args) {
  const { error, payload } = yield call(apiFunc, ...args)
  if(error) {
    yield act(successAction.replace('SUCCEEDED', 'FAILED'), payload, error)
  }
  else {
    yield act(successAction, payload, error)
  }
}
