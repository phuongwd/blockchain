import React from 'react'

import Link from 'next/link'
import { AppBar, Toolbar, Button, Typography, Tabs, Tab } from 'material-ui'


class Navigation extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  render() {
    return (
      <>
        <AppBar position='static'>
          <Toolbar>
            <Link href={'/'}>
              <Typography variant="title" color="inherit">
                Blockchain
              </Typography>
            </Link>

            <Tabs>
              <Link href={'/'}>
                <Tab label="Home"/>
              </Link>
              <Link href={'/about'}>
                <Tab label="About"/>
              </Link>
            </Tabs>
          </Toolbar>
        </AppBar>
      </>
    )
  }
}

export default Navigation
