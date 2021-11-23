import json
from django.http import JsonResponse
import haversine as hs
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import DriverState


# Create your views here.
@csrf_exempt
def setState(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        driver_object=DriverState(driver_id=body['driver_id'], latitude=body['latitude'], longitude=body['longitude'], state=body['state'], vehicle_type=body["vehicle_type"])
        if not DriverState.objects.filter(driver_id=body['driver_id']).exists():
            driver_object.save()
        else:
            t = DriverState.objects.get(driver_id=body['driver_id'])
            t.latitude=body['latitude']
            t.longitude=body['longitude']
            t.state=body['state']
            t.vehicle_type=body['vehicle_type']
            t.save()
        message="Successfully changed state."
        return JsonResponse({'status': 'true', 'message': message, 'driver_state': model_to_dict(driver_object)}, status=201)
    else:
        message="Oops, some error occurred."
        return JsonResponse({'status': 'false', 'message': message}, status=403)

@csrf_exempt
def getDriverList(request):
    if request.method == 'GET':
        curr_latitude = request.GET['latitude']
        curr_longitude=request.GET['longitude']
        vehicle_type = request.GET['vehicle_type']
        driver_list=dict()
        loc1 = (float(curr_latitude), float(curr_longitude))
        objects=DriverState.objects.all()
        for object in objects:
            if object.state=="idle" and object.vehicle_type == vehicle_type:
                loc2 = (object.latitude, object.longitude)
                driver_list["{}".format(object.driver_id)]=hs.haversine(loc1, loc2)
        driver_list = sorted(driver_list.items(), key=lambda x: x[1])
        sortdict = dict(driver_list)
        return JsonResponse(sortdict, status=200)
