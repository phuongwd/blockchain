import React from 'react'

import App, { Container } from 'next/app'

import withRedux from 'next-redux-wrapper'
import initStore from '../state/init_store'

import Content from '../components/Content'
import Navigation from '../components/Navigation'

import '../styles/layout.scss'

class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    return {
      pageProps: {
        ...(Component.getInitialProps ? await Component.getInitialProps(ctx) : {}),
      },
    }
  }

  render() {
    const { Component, pageProps, router } = this.props
    return (
      <Container>
        <nav className={'nav'}>
          <Navigation/>
        </nav>

        <section className={'content'}>
          <Content
            Component={Component}
            pageProps={pageProps}
            route={router.route}
          />
        </section>
      </Container>
    )
  }
}

export default withRedux(initStore)(MyApp)
