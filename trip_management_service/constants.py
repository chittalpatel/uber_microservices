class Routes:
    RIDE = "/ride"
    RIDE_OTP = "/ride/{ride}/otp"
    RIDE_START = "/ride/{ride}/start"
    RIDE_COMPLETE = "/ride/{ride}/complete"


class RideStates:
    ACCEPTED = "accepted"
    STARTED = "started"
    COMPLETED = "completed"
