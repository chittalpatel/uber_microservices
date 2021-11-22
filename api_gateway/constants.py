class Routes:
    BASE_API_STR = "/api/v1"

    # User Management
    LOGIN = BASE_API_STR + "/login"
    USER = BASE_API_STR + "/user"
    DRIVER = USER + "/driver"

    # Trip Management
    RIDE = BASE_API_STR + "/ride"
    RIDE_OTP = BASE_API_STR + "/ride/{ride}/otp"
    RIDE_START = BASE_API_STR + "/ride/{ride}/start"
    RIDE_COMPLETE = BASE_API_STR + "/ride/{ride}/complete"

    # Payment

