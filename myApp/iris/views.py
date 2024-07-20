from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
import json
from myApp.serializer import irisSerializer
from rest_framework.response import Response
from myApp.models import irisModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
@api_view(['GET'])
def irisData(request):
    if request.method == 'GET':
        try:
            irisModel.objects.all()[0]
        except:
            # Ruta donde se encuentra nuestro archivo:
            # ./media/iris.csv
            X = settings.MEDIA_ROOT + '/iris.csv'
            # Cargamos el dataset con ayuda de pandas:
            X_df = pd.read_csv(X)
            # Lo transformamos a json para poder gestionarlo desde el html:
            data = X_df.to_json(orient="index")
            data = json.loads(data)
            # Insertar datos en BBDD:
            for key, value in data.items():
                serializer = irisSerializer(data=value)
                if serializer.is_valid():   
                    serializer.save()
         # Visualizar los datos de base de datos:        
        data_db = irisModel.objects.all().values()
        # Context son los datos que pasamos al html:
        return render(request, 'iris/main.html', 
                      context={'data': data_db}, 
                      status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def insertData(request):
    result = ''
    if request.method == 'GET':
        return render(request, 'iris/insert.html')
    elif request.method == 'POST':
        # definir 'data' como el conjunto de datos
        # que se reciben a través del front-end:
        data = request.data
        # Pasaremos los datos por el serializer
        # para comprobar si los datos siguien el modelo esperado:
        serializer = irisSerializer(data=data)
        if serializer.is_valid():
            # Guardamos los datos en base de datos:
            serializer.save()
            # Redireccionamos a la página principal para comprobar el dataset:
            messages.add_message(request, messages.SUCCESS, "Item creado correctamente.")
            return redirect('/iris/')
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def updateData(request, id):
    if request.method == 'GET':
        try:
            object = irisModel.objects.get(id=id)
            return render(request, 'iris/update.html', 
                        context={'sepal_length': str(object.sepal_length),
                                'sepal_width': str(object.sepal_width), 
                                'petal_length': str(object.petal_length),
                                'petal_width': str(object.petal_width),
                                'specie': str(object.species)})
        except:
            messages.add_message(request, messages.ERROR, "Id no existe en la base de datos.")
            return redirect('/iris/')
    elif request.method == 'POST':
        # definir 'data' como el conjunto de datos
        # que se reciben a través del front-end:
        data = request.data
        # Pasaremos los datos por el serializer
        # para comprobar si los datos siguien el modelo esperado:
        serializer = irisSerializer(data=data)
        if serializer.is_valid():
            # Guardamos los datos actualizados:
            change = irisModel(id=id, 
                               sepal_length=serializer.data['sepal_length'],
                               sepal_width=serializer.data['sepal_width'],
                               petal_length=serializer.data['petal_length'],
                               petal_width=serializer.data['petal_width'],
                               species=serializer.data['species'])
            change.save()
            # Redireccionamos a la página principal para comprobar el dataset:
            messages.add_message(request, messages.SUCCESS, "Item actualizado correctamente.")
            return redirect('/iris/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def deleteData(request, id):
    if request.method == 'GET':
        try:
            object = irisModel.objects.get(id=id)
            return render(request, 'iris/delete.html', 
                        context={'sepal_length': str(object.sepal_length),
                                'sepal_width': str(object.sepal_width), 
                                'petal_length': str(object.petal_length),
                                'petal_width': str(object.petal_width),
                                'specie': str(object.species)})
        except:
            messages.add_message(request, messages.ERROR, "Id no existe en la base de datos.")
            return redirect('/iris/')
    # Método DELETE pero a través del front-end:
    elif request.method == 'POST':
        # Eliminamos el último dato:
        irisModel.objects.get(id=id).delete()
        # Redireccionamos a la página principal para comprobar el dataset:
        messages.add_message(request, messages.SUCCESS, "Item eliminado correctamente.")
        return redirect('/iris/')
