import fs from 'fs'
import rfs from 'rotating-file-stream'
import path from 'path'

import _ from 'lodash'
import is from 'is_js'
import pythonFormat from 'python-format'
import onHeaders from 'on-headers'
import onFinished from 'on-finished'
import platform from 'platform'

import clientIP from './client_ip'
import * as utils from 'util'
import handleError from './handle_error'

const _openRotatingFile = (params) => {
  let fileStream = null

  try {
    if(params.filename) {
      const filename = path.basename(params.filename)
      const dir = path.dirname(params.filename)

      fs.existsSync(dir) || fs.mkdirSync(dir)

      fileStream = rfs(filename, {
        size: params.maxFileSize,
        interval: params.interval,
        path: dir,
        compress: 'gzip',
        initialRotation: true,
      })
    }
  } catch(err) {
    handleError(err)
  }

  return fileStream
}

const _colorize = (str, color, bright = 1) => {
  const br = bright ? '1' : '0'
  return `\x1b[${br};${color}m${String(str)}\x1b[0m`
}

const _headersSent = (res) => {
  return typeof res.headersSent !== 'boolean' ? Boolean(res._header)
    : res.headersSent
}

const getUrl = (req, { colorize, format, filters, maxLen } = {}) => {
  let urlPath = String(req.originalUrl) || String(req.url) || ''

  if(is.array(filters) && filters.some(s => urlPath.includes(s))) {
    return null
  }

  if(maxLen && urlPath.length > maxLen) {
    urlPath = urlPath.slice(0, maxLen - 3) + '...'
  }

  if(format) {
    urlPath = pythonFormat(`{:${maxLen}}`, urlPath)
  }

  if(colorize) {
    if(urlPath.startsWith('/api/auth')) {
      urlPath = _colorize(urlPath, 31, false)
    }
    else if(urlPath.startsWith('/api')) {
      urlPath = _colorize(urlPath, 94, false)
    }
  }

  return String(urlPath)
}

let getResponseTime = (req, res, { colorize, format } = {}) => {
  let responseTime = ''
  if(req.begin && res.begin) {
    const ms = (res.begin[0] - req.begin[0]) * 1e3 + (res.begin[1] - req.begin[1]) * 1e-6

    if(format) {
      if(ms > 999) {
        responseTime = (ms / 1000).toFixed(0) + ' s '
      }
      else {
        responseTime = ms.toFixed(0) + ' ms'
      }

      responseTime = pythonFormat('{:>6}', responseTime)
    }
    else {
      responseTime = String(ms.toFixed(0))
    }

    if(colorize) {
      const color = ms >= 500 ? 31
        : ms >= 100 ? 33
          : 32

      responseTime = _colorize(responseTime, color, false)
    }
    else {
      responseTime = String(responseTime)
    }
  }
  return responseTime
}

let getLag = (req, { colorize, format } = {}) => {
  let lag = ''
  if(req.lag) {
    const ms = req.lag || 0

    if(format) {
      if(ms > 999) {
        lag = (ms / 1000).toFixed(0) + ' s '
      }
      else {
        lag = ms.toFixed(0) + ' ms'
      }

      lag = pythonFormat('{:>6}', lag)
    }
    else {
      lag = String(ms.toFixed(0))
    }

    if(colorize) {
      const color = ms >= 500 ? 31
        : ms >= 100 ? 33
          : 32

      lag = _colorize(lag, color, false)
    }
    else {
      lag = String(lag)
    }
  }
  return lag
}

let getStatus = (res, { colorize } = {}) => {
  let statusStr = ''
  if(_headersSent(res)) {
    const status = res.statusCode

    const color = status >= 500 ? 31
      : status >= 400 ? 33
        : status >= 300 ? 36
          : status >= 200 ? 32
            : 0

    if(colorize) {
      statusStr = _colorize(status, color)
    }
    else {
      statusStr = String(status)
    }
  }
  return statusStr
}

let getUserId = (req) => {
  let userId = ''
  if(req.user) {
    userId = req.user.user_id
  }
  return userId
}

let getUserAgent = (req) => {
  let userAgent = ''
  if(req.headers) {
    userAgent = req.headers['user-agent'] || ''
  }
  return userAgent
}

let getSessionId = (req, { maxLen = 32 } = { maxLen: 32 }) => {
  let sessionID = ''
  if(req.sessionID) {
    sessionID = String(req.sessionID)
    if(sessionID.length > maxLen) {
      sessionID = sessionID.slice(0, maxLen)
    }
  }
  return sessionID
}

let getSessionHits = (req) => {
  let sessionHits = ''
  if(req.session && req.session.hits) {
    const hits = Number(req.session.hits)
    if(hits) {
      sessionHits = String(hits)
    }
  }
  return sessionHits
}

let getBrowserInfo = (req) => {
  const userAgent = getUserAgent(req)
  let browserStr = ''
  const browser = platform.parse(userAgent)
  if(browser && browser.name) {
    browserStr = String(browser.name)

    if(browser.version) {
      browserStr += ' ' + String(browser.version)
    }

    if(browser.os) {
      let os = String(browser.os)
      if(_.startsWith(os, 'Ubuntu')) {
        os = 'Ubuntu'
      }

      browserStr += '/' + os
    }
  }

  if(browserStr.length === 0) {
    browserStr = userAgent.slice(0, 16)
  }
  return { browserStr, userAgent }
}

let getHttpVersion = (req) => {
  if(is.existy(req.httpVersionMajor) && is.existy(req.httpVersionMinor)) {
    return pythonFormat('{}.{}', req.httpVersionMajor, req.httpVersionMinor)
  }
  return ''
}

let getProtocol = (req) => {
  let protocol = req.protocol
  if(is.existy(req.isSpdy) && req.isSpdy) {
    protocol = 'spdy'
  }
  return protocol
}

let getReferrer = (req) => {
  return req.headers.referrer || req.headers.referer || ''
}

let getIsXhr = (req) => {
  return req.xhr || false
}

let getMethod = (req, { maxLen } = {}) => {
  let method = String(req.method) || 'UNK'
  if(maxLen && method.length > maxLen) {
    method = maxLen.slice(0, 4)
  }
  return method
}

const prepareConsoleString = (req, res, params) => {
  const urlPath = getUrl(req, {
    colorize: true,
    maxLen: 32,
    format: true,
    filters: [
      'on-demand-entries-ping',
      'webpack-hmr',
      'hot-update',
      // '/_next/',
    ],
  })

  if(is.not.existy(urlPath)) {
    return null
  }

  const beginTimestamp = req.beginTimestamp || 0
  const beginDatetime = req.beginDatetime || ''

  const statusStr = getStatus(res, { colorize: true })
  let method = getMethod(req, { maxLen: 4 })
  if(getIsXhr(req)) {
    method += '*'
  }

  const responseTime = getResponseTime(req, res, {
    colorize: true,
    format: true,
  })
  const lag = getLag(req, { colorize: true, format: true })

  const ip = clientIP(req)
  const userId = getUserId(req)

  const sidLen = params.verbose ? 32 : 8
  const sessionID = getSessionId(req, { maxLen: sidLen })
  const sessionHits = getSessionHits(req)
  const { browserStr, userAgent } = getBrowserInfo(req)

  const protocol = getProtocol(req)

  //@formatter:off
  let fields = [
    { fmt: '{:13}'       , value: beginTimestamp    , def: '', show: false }         ,
    { fmt: '{:19}'       , value: beginDatetime     , def: '', show: params.verbose },
    { fmt: '{:>6}'       , value: lag               , def: '', show: params.verbose },
    { fmt: '{:>6}'       , value: responseTime      , def: '', show: params.verbose },
    { fmt: '{:3}'        , value: statusStr         , def: '', show: true }          ,
    { fmt: '{:15}'       , value: ip                , def: '', show: true }          ,
    { fmt: '{:5}'        , value: protocol          , def: '', show: params.verbose },
    { fmt: '{:5}'        , value: method            , def: '', show: true }          ,
    { fmt: '{:32}'       , value: urlPath           , def: '', show: true }          ,
    { fmt: '{:>4}'       , value: userId            , def: '', show: true }          ,
    { fmt: '{:>5}'       , value: sessionHits       , def: '', show: true }          ,
    { fmt: `{:${sidLen}}`, value: sessionID         , def: '', show: true }          ,
    { fmt: '{:16}'       , value: browserStr        , def: '', show: params.verbose },
    { fmt: '{:16}'       , value: userAgent         , def: '', show: false }         ,
  ]
  //@formatter:on

  fields = _.filter(fields, e => e.show)
  const fmt = _.map(fields, e => e.fmt).join(' | ')
  const values = _.map(fields, e => e.value || e.def)
  return pythonFormat(fmt, ...values)
}


const prepareFileString = (req, res, params) => {
  const urlPath = getUrl(req)
  if(is.not.existy(urlPath)) {
    return null
  }

  const beginTimestamp = req.beginTimestamp || 0
  const statusStr = getStatus(res)
  const method = getMethod(req)
  const isXhr = getIsXhr(req)

  const responseTime = getResponseTime(req, res)
  const lag = getLag(req)

  const ip = clientIP(req)
  const userId = getUserId(req)
  const sessionID = getSessionId(req)
  const sessionHits = getSessionHits(req)
  const userAgent = getUserAgent(req)

  const protocol = getProtocol(req)
  const httpVersion = getHttpVersion(req)

  const referrer = getReferrer(req)
  const headers = req.headers || {} // TODO: trim if too long
  // const body = req.body || {} // TODO: trim if too long
  // const cookies = req.cookies || {} // TODO: trim if too long

  let fields = [
    beginTimestamp,
    lag,
    responseTime,
    statusStr,
    ip,
    protocol,
    httpVersion,
    method,
    isXhr,
    urlPath,
    userId,
    sessionHits,
    sessionID,
    userAgent,
    referrer,
    headers,
  ]

  return utils.inspect(fields)
}

const requestLogger = (params) => {
  let fileStream = _openRotatingFile(params)

  const _format = (req, res) => {
    if(params.printFunc) {
      const str = prepareConsoleString(req, res, params)
      if(str) {
        params.printFunc(str)
      }
    }

    if(fileStream) {
      const str = prepareFileString(req, res, params)
      if(str) {
        fileStream.write(str)
      }
    }
  }

  return (req, res, next) => {
    onHeaders(res, () => { res.begin = process.hrtime()})
    onFinished(res, () => { _format(req, res) })
    next()
  }
}

export default requestLogger
