from django.http import JsonResponse


def testCors(request):

    return JsonResponse({'msg': 'CORS is ok'})