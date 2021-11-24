from django.shortcuts import render


# Create your views here.

def saludo(request, id):
    suma = id + 1

    return render(request, 'hello.html', {'name': 'World', 'id': suma})
