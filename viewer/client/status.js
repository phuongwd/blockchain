const codes = {
  SUCCESS: 'SUCCESS',
  CONNECTION_ERROR: 'CONNECTION_ERROR',
  APPLICATION_ERROR: 'APPLICATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORISED: 'UNAUTHORISED',
  USER_ALREADY_EXISTS: 'USER_ALREADY_EXISTS',
  SIGNUP_INFO_INVALID: 'SIGNUP_INFO_INVALID',
  CREDENTIALS_INVALID: 'CREDENTIALS_INVALID',
  UNABLE_TO_SEND_EMAIL: 'UNABLE_TO_SEND_EMAIL',
  CSRF_TOKEN_INVALID: 'CSRF_TOKEN_INVALID',
}

const Status = {
  ...codes,

  Success: {
    httpCode: 200,
    errCode: codes.SUCCESS,
    message: {
      en: 'Operation successful',
    },
  },

  ConnectionError: {
    httpCode: 0,
    errCode: codes.CONNECTION_ERROR,
    message: {
      en: 'There was an error when connecting to the server',
    },
  },

  ApplicationError: {
    httpCode: 0,
    errCode: codes.APPLICATION_ERROR,
    message: {
      en: 'There was an error in the application',
    },
  },

  NotFound: {
    httpCode: 404,
    errCode: codes.NOT_FOUND,
    message: {
      en: 'Not found',
    },
  },

  Unauthorised: {
    httpCode: 200,
    errCode: codes.UNAUTHORISED,
    message: {
      en: 'Access to this resource requires authentication',
    },
  },

  UserAlreadyExists: {
    httpCode: 200,
    errCode: codes.USER_ALREADY_EXISTS,
    message: {
      en: 'User already exists',
    },
  },

  SignupInfoInvalid: {
    httpCode: 200,
    errCode: codes.SIGNUP_INFO_INVALID,
    message: {
      en: 'User information provided is invalid',
    },
  },

  CredentialsInvalid: {
    httpCode: 200,
    errCode: codes.CREDENTIALS_INVALID,
    message: {
      en: 'Email and/or password are invalid',
    },
  },

  UnableToSendEmail: {
    httpCode: 200,
    errCode: codes.UNABLE_TO_SEND_EMAIL,
    message: {
      en: 'Unable to send email to this address',
    },
  },

  CSRFTokenInvalid: {
    httpCode: 200,
    errCode: codes.CSRF_TOKEN_INVALID,
    message: {
      en: 'CSRF token is invalid',
    },
  },

  CSPReportAck: {
    httpCode: 204,
    errCode: codes.CSP_REPORT_ACK,
    message: {
      en: 'CSP report has been received successfully',
    },
  },

  httpCode: 200,
  errCode: codes.CSRF_TOKEN_INVALID,
  message: {
    en: 'The requested range is out of bounds',
  },
}

export default Status
