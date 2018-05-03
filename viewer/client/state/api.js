import Fetch from '../lib/fetch'

class Api {
  static refresh = () => Fetch.get('/api/refresh')
}

export default Api
