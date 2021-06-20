from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request, id=None):

    if request.method == 'GET':
        if not id:

            is_favourite = request.GET.get('is_favourite', None)
            order_by = request.GET.get('order_by', None)

            # filters = {""}
            print(is_favourite)
            if is_favourite and is_favourite == 'true':
                blog = Blog.objects.filter(favourite=True)
            elif order_by:
                blog = Blog.objects.order_by(order_by)
            else:
                blog = Blog.objects.all()


        else:
            blog = Blog.objects.filter(id=id)

        resp_blog = []
        for each in blog:
            _obj = dict()
            _obj['id'] = each.id
            _obj['description'] = each.description
            _obj['title'] = each.title
            _obj['favourite'] = each.favourite
            _obj['vote'] = each.vote
            resp_blog.append(_obj)
        
        if not resp_blog:
            return JsonResponse({"blog": resp_blog, "message": "No Blogs exist"})

        return JsonResponse({"blog": resp_blog})

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        model_blog= Blog(title = body['title'], description=body['description'])
        model_blog.save()
        return JsonResponse({"message":"Blog created successfully"})

    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if not id:
            return JsonResponse({"message": "Please mention ID"})
        
        model_blog =  Blog.objects.filter(id=id)
        if not model_blog:
            return JsonResponse({"message": "No such ID exist"})

        model_blog = model_blog[0]
        model_blog.title = body['title']
        model_blog.description = body['description']
        model_blog.save()
        return JsonResponse({"message":"Blog updated successfully"})

    if request.method == 'DELETE':

        if not id:
            return JsonResponse({"message": "Please mention ID"})
        
        model_blog =  Blog.objects.filter(id=id)
        if not model_blog:
            return JsonResponse({"message": "No such ID exist"})

        model_blog = model_blog[0]
        model_blog.delete()
        return JsonResponse({"message" : "Blog deleted sucessesfully"})


@csrf_exempt
def favourite(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id'] if body and 'id' in body else None

    model_blog = Blog.objects.filter(id=id)
    if not model_blog:
        return JsonResponse({'message' : 'No such id exists'})

    model_blog = model_blog[0]
    model_blog.favourite = True
    model_blog.save()
    return JsonResponse({'message': 'Blog is selected as favourite sucessfully'})

@csrf_exempt
def vote(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id'] if body and 'id' in body else None
    action = body['action'] if body and 'action' in body else None

    if not id:
            return JsonResponse({"message": "Please mention ID"})

    model_blog = Blog.objects.filter(id=id)
    model_blog = model_blog[0]

    if action == 'like':
        model_blog.vote += 1
    elif action == 'dislike':
        model_blog.vote -= 1
    model_blog.save()
    return JsonResponse({'message': 'Blog is voted sucessfully'})
    





  


        

    

    
