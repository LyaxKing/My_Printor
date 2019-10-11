from django.shortcuts import render

def hello(request):
    context          = {}
    context['PrintorControl'] = 'Printor Control'
    context['State'] = 'State'
    context['id'] = 'id:'
    context['alive'] = 'alive:'
    context['printing'] = 'printing:'
    context['endprint'] = 'endprint:'
    context['startprint'] = 'startprint:'
    context['process'] = 'process:'
    context['chambertemperature'] = 'chambertemperature:'
    context['bedtemperature'] = 'bedtemperature:'
    return render(request, 'main.html', context)