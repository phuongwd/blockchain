const path = require('path')

const CopyWebpackPlugin = require('copy-webpack-plugin')
const withSass = require('@zeit/next-sass')

const appendPlugin = (config, pluginObject) => {
  config.plugins.push(pluginObject)
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

let config = {
  distDir: path.join('../.build/client'),

  useFileSystemPublicRoutes: false,

  onDemandEntries: {
    maxInactiveAge: 60 * 60 * 1000,
    pagesBufferLength: 99,
  },

  sassLoaderOptions: {
    sourceMap: true,
    includePaths: [
      'node_modules',
      'client/styles',
    ],
  },

  webpack: async (config, { dev, isServer }) => {
    if(dev) {
      config.devtool = 'cheap-module-eval-source-map'
      config.output.crossOriginLoading = 'anonymous'
    }

    removePlugin(config, 'FriendlyErrorsWebpackPlugin')


    if(!isServer) {
      appendPlugin(config, new CopyWebpackPlugin([
        { context: '../', from: 'static/**' },
      ]))

      appendPlugin(config, new CopyWebpackPlugin([
        {
          test: /(favicon\.ico|robots\.txt)$/,
          context: '../static/',
          from: '**',
        },
      ]))

      config.module.rules.push({
        test: /\.(eot|svg|ttf|woff|woff2)(\?v=\d+(\.\d+){0,2})?$/,
        use: [{
          loader: 'file-loader',
          options: {
            limit: 50000,
            mimetype: 'application/font-woff',
            name: '[name].[ext]',
            publicPath: 'fonts',
            outputPath: 'static/fonts',
          },
        },
        ],
      })
    }
    else {
      config.module.rules.push({
        test: /\.(eot|svg|ttf|woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
        use: ['ignore-loader'],
      })
    }

    return config
  },

  webpackDevMiddleware: config => {
    return config
  },
}

config = withSass(config)
module.exports = config
