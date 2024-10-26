from enum import StrEnum, IntEnum


class EnumComparer:
    def is_in(cls, value) -> bool:
        return len([val for val in cls]) > 0


class MimeType(StrEnum):
    HTML = "text/html"
    PLAIN = "text/plain"
    CSS = "text/css"
    JS = "application/javascript"
    JSON = "application/json"
    PNG = "image/png"
    JPG = "image/jpeg"
    SVG = "image/svg+xml"
    ICO = "image/x-icon"
    WOFF = "font/woff"
    WOFF2 = "font/woff2"
    TTF = "font/ttf"
    OTF = "font/otf"
    UNKNOWN = "application/octet-stream"


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    TRACE = "TRACE"
    UNKNOWN = "UNKNOWN"


class Header(StrEnum):
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    CONNECTION = "Connection"
    KEEP_ALIVE = "Keep-Alive"
    SERVER = "Server"
    DATE = "Date"
    ACCEPT = "Accept"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_CHARSET = "Accept-Charset"
    USER_AGENT = "User-Agent"
    HOST = "Host"
    ORIGIN = "Origin"
    REFERER = "Referer"
    COOKIE = "Cookie"
    SET_COOKIE = "Set-Cookie"
    LOCATION = "Location"
    CACHE_CONTROL = "Cache-Control"
    EXPIRES = "Expires"
    PRAGMA = "Pragma"
    LAST_MODIFIED = "Last-Modified"
    ETAG = "ETag"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    IF_NONE_MATCH = "If-None-Match"
    VARY = "Vary"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_DISPOSITION = "Content-Disposition"
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
    ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
    ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
    ACCESS_CONTROL_REQUEST_METHOD = "Access-Control-Request-Method"
    ACCESS_CONTROL_REQUEST_HEADERS = "Access-Control-Request-Headers"
    AUTHORIZATION = "Authorization"
    WWW_AUTHENTICATE = "WWW-Authenticate"


class Status(IntEnum):
    # Success
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    EARLY_HINTS = 103
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    SWITCH_PROXY = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    # Error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    # Server error
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511
    NETWORK_READ_TIMEOUT_ERROR = 598
    NETWORK_CONNECT_TIMEOUT_ERROR = 599