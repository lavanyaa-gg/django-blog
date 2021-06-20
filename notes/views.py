from django.shortcuts import render
from django.http import JsonResponse
from .models import Note
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request, id=None):

    if request.method == 'GET':
        if not id:

            is_favourite = request.GET.get('is_favourite', None)

            if is_favourite and is_favourite == 'true':
                notes = Note.objects.filter(favourite=True)
            else:
                notes = Note.objects.all()

        else:
            notes = Note.objects.filter(id=id)

        resp_notes = []
        for each in notes:
            _obj = dict()
            _obj['id'] = each.id
            _obj['text'] = each.text
            _obj['title'] = each.title
            _obj['favourite'] = each.favourite
            resp_notes.append(_obj)
        
        if not resp_notes:
            return JsonResponse({"notes": resp_notes, "message": "No Notes exist"})

        return JsonResponse({"notes": resp_notes})
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        model_note = Note(title = body['title'], text=body['text'])
        model_note.save()
        return JsonResponse({"message":"Notes created successfully"})


    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if not id:
            return JsonResponse({"message": "Please mention ID"})
        
        model_note = Note.objects.filter(id=id)
        if not model_note:
            return JsonResponse({"message": "No such ID exist"})

        model_note = model_note[0]    
        model_note.title = body['title']
        model_note.text = body['text']
        model_note.save()
        return JsonResponse({"message":"Notes updated successfully"})
        
    if request.method == 'DELETE':
        if not id:
            return JsonResponse({"message": "Please mention ID"})
        
        model_note = Note.objects.filter(id=id)
        if not model_note:
            return JsonResponse({"message": "No such ID exist"})
        
        model_note = model_note[0]
        model_note.delete()
        return JsonResponse({"message":"Notes deleted successfully"})


@csrf_exempt
def favourite(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    id = body['id'] if body and 'id' in body else None

    model_note = Note.objects.filter(id=id)
    if not model_note:
        return JsonResponse({"message": "No such ID exist"})
    
    model_note = model_note[0]
    model_note.favourite = True
    model_note.save()
    return JsonResponse({"message":"Note is added as a favourite one"})