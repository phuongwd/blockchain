import React from 'react'

import Document, { Head, Main, NextScript } from 'next/document'
import { CssBaseline, MuiThemeProvider } from 'material-ui'
import { createMuiTheme } from 'material-ui/styles'
import purple from 'material-ui/colors/purple'
import green from 'material-ui/colors/green'

import htmlescape from 'htmlescape'

const configClient = JSON.parse(process.env['configClient'])



const theme = createMuiTheme({
  palette: {
    primary: purple,
    secondary: green,
  },
  status: {
    danger: 'orange',
  },
})

class MyDocument extends Document {
  constructor(props, context) {
    super(props, context)
  }

  render() {
    return (
      <html>
        <Head>
          <meta charSet="utf-8"/>
          <meta httpEquiv="x-ua-compatible" content="ie=edge,chrome=1"/>
          <meta name="viewport"
            content="width=device-width, initial-scale=1.0, shrink-to-fit=no"/>

          <title>{configClient.APP_NAME_FRIENDLY}</title>

          <link
            rel="stylesheet"
            type='text/css'
            href="https://fonts.googleapis.com/css?family=Roboto|Roboto+Mono"
          />

          <link
            rel='stylesheet'
            type='text/css'
            href='/_next/static/style.css'
            crossOrigin='anonymous'
          />
        </Head>

        <body>
          <script
            dangerouslySetInnerHTML={{
              __html: '__configClient__ = ' + htmlescape(configClient),
            }}
          />

          <CssBaseline/>

          <MuiThemeProvider theme={theme}>
            <Main/>
          </MuiThemeProvider>
          <NextScript/>
        </body>
      </html>
    )
  }
}

export default MyDocument
