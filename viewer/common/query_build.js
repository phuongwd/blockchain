import { stringify as qsStringify } from 'qs'
import querySanitize from './query_sanitize'

export default function queryBuild(url, query) {
  const querySanitized = querySanitize(query)
  return ''.concat(url, '?',
    qsStringify(querySanitized, { skipNulls: true }),
  )
}
