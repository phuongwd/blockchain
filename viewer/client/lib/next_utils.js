const appendPlugin = (config, pluginObject) => {
  config.plugins.push(pluginObject)
}

const findPlugin = (config, pluginConstructorName) => {
  const i = config.plugins.findIndex((plugin) =>
    plugin.constructor.name === pluginConstructorName,
  )

  let plugin = null
  if(i && config.plugins.length > i) {
    return { plugin: config.plugins[i], i }
  }

  return { plugin, i }
}

const prependPlugin = (config, pluginObject) => {
  config.plugins.unshift(pluginObject)
}

const removePlugin = (config, pluginConstructorName) => {
  const filtered = config.plugins = config.plugins.filter((plugin) =>
    plugin.constructor.name !== pluginConstructorName,
  )

  if(filtered && filtered.length === 1) {
    return filtered[0]
  }

  return filtered
}

module.exports = { appendPlugin, findPlugin, prependPlugin, removePlugin }
