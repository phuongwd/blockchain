import _ from 'lodash'
import is from 'is_js'
import Axios from 'axios'

import config from '../client.config'
import Status from '../status'
import Log from './log'
import queryBuild from '../../common/query_build'

const axios = Axios.create({
  baseURL: config.SERVER_ROOT,
  timeout: 10000,
  responseType: 'json',
})

const handleThen = (response) => {
  return _.get(response, 'data', null)
}

const handleCatch = (err) => {
  if(err.response) {
    // The request was made and the server responded with a failure
    const res = _.get(err.response, 'data', null)
    Log.warn(res)
    return res
  }
  else if(err.request) {
    // The request was made but no response was received
    const payload = { status: Status.ConnectionError, data: err }
    Log.err(payload)
    return { error: true, payload }
  }
  else {
    // Something happened in setting up the request
    const payload = { status: Status.ApplicationError, data: err }
    Log.err(payload)
    return { error: true, payload }
  }
}

class Fetch {
  static request = (method) => (url, data, config) => {
    return axios({ method, url, data, ...config })
      .then(handleThen)
      .catch(handleCatch)
  }

  static get = (url, query, config = {}) => {
    let urlWithQuery = url

    if(is.existy(query)) {
      urlWithQuery = queryBuild(url, query)
    }

    return axios({
      method: 'get',
      url: urlWithQuery,
      ...config,
    })
      .then(handleThen)
      .catch(handleCatch)
  }

  static post = Fetch.request('post')

  static update = Fetch.request('update')

  static delete = Fetch.request('delete')

  static put = Fetch.request('put')

  static patch = Fetch.request('patch')
}

export default Fetch
