import React from 'react'

import { Collapse, Card, CardHeader } from 'reactstrap'

class Accordion extends React.Component {
  constructor(props) {
    super(props)
    this.state = { openIdx: 0 }
  }

  handleHeaderClick = (event) => {
    const i = Number(event.target.dataset.event)
    this.setState({
      openIdx: (this.state.openIdx === i) ? 0 : i,
    })
  }

  render() {
    const { openIdx } = this.state
    const { items } = this.props

    return (
      <>
        {
          items.map((item, i) => {
            return (
              <Card style={{ marginBottom: '0.25rem' }} key={i}>

                <CardHeader onClick={this.handleHeaderClick} data-event={i}>
                  {item.header}
                </CardHeader>

                <Collapse isOpen={openIdx === i}>
                  <div style={{ width: '100%', padding: 0, margin: 0 }}>
                    {item.body}
                  </div>
                </Collapse>

              </Card>
            )
          })}
      </>
    )
  }
}

export default Accordion
