from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

class Booking(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    passenger_id=db.Column(db.Integer,nullable=False)
    pickup_location=db.Column(db.String(100),nullable=False)
    drop_location=db.Column(db.String(100),nullable=False)
    cost=db.Column(db.Integer,nullable=False)
    est=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,nullable=False)
    state=db.Column(db.String(10),nullable=False)

booking_api_get_args=reqparse.RequestParser()
booking_api_get_args.add_argument("booking_id",type=int,help="Booking Id is required!")
booking_api_get_args.add_argument("passenger_id",type=int,help="User Id is required!")

booking_api_post_args=reqparse.RequestParser()
booking_api_post_args.add_argument("passenger_id",type=int,help="User Id is required!",required=True)
booking_api_post_args.add_argument("pickup_location",type=str,help="Pickup location is required!",required=True)
booking_api_post_args.add_argument("drop_location",type=str,help="Drop location is required!",required=True)
booking_api_post_args.add_argument("vehicle_type",type=str,help="Vehicle type is required!",required=True)

booking_api_patch_args=reqparse.RequestParser()
booking_api_patch_args.add_argument("booking_id",type=int,help="Booking Id is required!",required=True)
booking_api_patch_args.add_argument("state",type=str,help="State of Booking is required!",required=True)

booking_api_delete_args=reqparse.RequestParser()
booking_api_delete_args.add_argument("booking_id",type=int,help="Booking Id is required!",required=True)

all_booking_api_get_args=reqparse.RequestParser()
all_booking_api_get_args.add_argument("passenger_id",type=int,help="User Id is required!",required=True)

# db.create_all()
resource_fields = {
        'passenger_id':fields.Integer,
        'pickup_location':fields.String,
        'drop_location':fields.String,
        'cost':fields.Integer,
        'est':fields.Integer,
        'created_at':fields.DateTime,
        'state':fields.String
}

class BookingApi(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = booking_api_get_args.parse_args()
        if args['booking_id']:
            booking=Booking.query.filter_by(id=args['booking_id']).first()
        elif args['passenger_id']:
            booking=Booking.query.filter_by(passenger_id=args['passenger_id']).order_by(Booking.created_at.desc()).first()
        else:
            abort(404, message="Booking Id or User Id is required")
        if not booking:
            abort(404,message="Booking doesn't exit")
        return booking

    def post(self):
        args = booking_api_post_args.parse_args()
        #------------------- Calculate distance through Google Map api--------------------
        # also calculate Estimatate time
        dist=12
        est=30
        #--------------------------------------------------------------------------------

        #--------------check vehichle type name is correct
        if args['vehicle_type']=='bike':
            cost = dist*3;
        elif args['vehicle_type']=='rickshaw':
            cost = dist * 5;
        elif args['vehicle_type']=='mini':
            cost = dist * 10;
        elif args['vehicle_type']=='sedan':
            cost = dist * 13;
        elif args['vehicle_type']=='SUV':
            cost = dist * 15;
        else:
            abort(404, message="Type of vehicle does not match!")

        created_at=datetime.now()
        booking = Booking(passenger_id=args['passenger_id'],pickup_location=args['pickup_location'],est=est,
                            drop_location=args['drop_location'],cost=cost,created_at=created_at,state="pending")
        db.session.add(booking)
        db.session.commit()
        booking_id = Booking.query.filter_by(passenger_id=args['passenger_id'], created_at=created_at).first()

        driver_list=[1,2,3,4,5]
        driver_id=driver_list[0]
        '''
        if driver_list api:
            if post request to ride:
                booking.state = 'accepted'
                db.session.commit()
            else:
                booking.state = 'cancelled'
                db.session.commit()
                abort(404, message="Internal Server Error")
        else:
            booking.state = 'cancelled'
            db.session.commit()
            abort(404, message="Internal Server Error")
        '''
        booking.state = 'accepted'
        db.session.commit()
        return {'booking_id':booking_id.id,'driver_id':driver_id,'cost':cost,'est':est}, 200

    @marshal_with(resource_fields)
    def patch(self):
        args = booking_api_patch_args.parse_args()
        booking = Booking.query.filter_by(id=args['booking_id']).first()
        if not booking:
            abort(404, message="Booking doesn't exist")

        booking.state = args['state']
        db.session.commit()
        return booking, 202

    def delete(self):
        args = booking_api_delete_args.parse_args()
        booking = Booking.query.filter_by(id=args['booking_id']).first()
        if not booking:
            abort(404, message="Booking doesn't exist")
        Booking.query.filter_by(id=args['booking_id']).delete()
        db.session.commit()
        return {'messgae': 'Deleted Successfully'}

class AllBookingApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = all_booking_api_get_args.parse_args()
        booking = Booking.query.filter_by(passenger_id=args['passenger_id']).all()
        if not booking:
            abort(404, message="Booking doesn't exit")
        return booking

api.add_resource(BookingApi, "/booking")
api.add_resource(AllBookingApi,"/allbooking")

if __name__ == '__main__':
    app.run()
