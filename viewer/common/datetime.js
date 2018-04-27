import moment from 'moment/moment'

export default function datetime() {
  return moment().format('YYYY-MM-DD_HH:mm:ss')
}
