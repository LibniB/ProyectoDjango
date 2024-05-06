import os
from django.conf import settings
from django.shortcuts import render,redirect
from django.db import Error
from appPeliculas.models import Genero,Pelicula
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

def vistaAgregarGenero(request):
    return render(request,"agregarGenero.html")

@csrf_exempt
def agregarGenero(request):
    try:
        nombre=request.POST['txtNombre']
        #crear obejto de tipo genero
        genero= Genero(getNombre=nombre)
        #salvar el objeto, lo que permite que sea creado en la base de datos
        genero.save()
        mensaje="Genero agregado correctamente"
    except Error as error:
        mensaje=str(error)
        
    retorno ={"mensaje":mensaje}
    
    return JsonResponse(retorno)

def listarPeliculas(request):
    peliculas = Pelicula.objects.all()
    
    retorno={"peliculas":list(peliculas)}
    
    return render(request, "listarPeliculas.html",retorno)


def vistaAgregarPelicula(request):
    generos= Genero.objects.all()
    retorno={"generos":generos}
    
    return render(request, "agregarPelicula.html",retorno)



def agregarPelicula(request):
    try:
        codigo=request.POST['txtCodigo']
        titulo = request.POST['txtTitulo']
        protagonista = request.POST['txtProtagonista']
        duracion= int(request.POST['txtDuracion'])
        resumen= request.POST['txtResumen']
        foto =request.FILES['fileFoto']
        idGenero=int(request.POST['cbGenero'])
        
        genero= Genero.objects.get(pk=idGenero)
        
        #creando objeto pelicula
        
        pelicula =Pelicula(pelCodigo=codigo,
                           pelTitulo=titulo,
                           pelProtagonista=protagonista,
                           pelDuracion=duracion,
                           pelResumen=resumen,
                           pelFoto=foto,
                           pelGenero=genero)
        pelicula.save()
        mensaje="Pelicula agregada correctamente"
    except Error as error:
        mensaje=str(error)
    retorno={"mensaje":mensaje,'idPelicula':pelicula.id}
    #return JsonResponse(retorno)
    return render(request,"agregarPelicula.html",retorno)

def consultarPeliculaPorId(request, id):
    pelicula=Pelicula.objects.get(pk=id)
    generos=Genero.objects.all() 
    
    retorno={"pelicula":pelicula, "generos":generos}
    return render(request,"actualizarPelicula.html",retorno)

def actualizarPelicula(request):
    try:
        idPelicula= request.POST['idPelicula']
        
        peliculaActualizar =Pelicula.objects.get(pk=idPelicula)
        
        peliculaActualizar.pelCodigo= request.POST['txtCodigo']
        peliculaActualizar.pelTitulo = request.POST['txtTitulo']
        peliculaActualizar.pelProtagonista = request.POST['txtProtagonista']
        peliculaActualizar.pelDuracion = request.POST['txtDuracion']
        peliculaActualizar.pelResumen = request.POST['txtResumen']
        idGenero= int(request.POST['cbGenero'])
        
        genero= Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero= genero
        foto = request.FILES.get('fileFoto')
        
        if(foto):
            os.remove(os.path.join(settings.MEDIA_ROOT + "/" +
                                   str(peliculaActualizar.pelFoto)))
            peliculaActualizar.pelFoto= foto
        peliculaActualizar.save()    
        mensaje= "pelicula Actualizada"
    except Error as error:
        mensaje=str(error)
    retorno={"mensaje":mensaje}
    #return JsonResponse(retorno)
    return redirect('/listarPeliculas')

def eliminaPelicula(request,id):
    try:
        peliculaEliminar = Pelicula.objects.get(pk=id)
        peliculaEliminar.delete()
        mensaje="Pelicula eliminada correctamente"
    except Error as error:
        mensaje= str(error)
    #retorno ={"mensaje":mensaje}
    return redirect('/listarPeliculas')