import json
from django.shortcuts import render, HttpResponse, Http404

# Create your views here.


def dismiss_marketing_message(request):
    if request.is_ajax():
        data = {"success": True}
        print("DATA: {0}".format(str(data)))
        json_data = json.dumps(data)
        print("JSON DATA {0}".format(str(json_data)))
        return HttpResponse(json_data, content_type="application/json")
    else:
        raise Http404
        #TODO return something else