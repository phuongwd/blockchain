class Log {
  static info = (...args) => {
    console.info(...args)
  }

  static warn = (...args) => {
    console.warn(...args)
  }

  static err = (...args) => {
    console.error(...args)
  }
}

export default Log
