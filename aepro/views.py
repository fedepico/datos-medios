from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction, IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
import subprocess

from .models import (
    ResultadoCEP as CEP,
    ResultadoFDA as FDA,
    Analisis,
    )

from .forms import (
    AnalisisModelForm,
    FormularioContacto, 
    UpdateResultadoFDA,
    ValidacionFicheroForm,
    )

#CBV
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

import os
import json
# import plotly.offline as opy
# import plotly.graph_objs as go
# import plotly.figure_factory as ff

from datetime import datetime

from subprocess import check_output

def get_pid(name):
    return list(map(int,check_output(["pidof",name]).split()))


class LoginRequired(object):
    #@method_decorator(login_required)
    def dispatch(self, *args,  **kwargs): #def dispatch(self, request ,*args,  **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs) #.dispatch(request, *args, **kwargs)

# Create your views here.
def inicio(request):
    titulo="Inicio"
    saludo = "Hola"
    if request.user.is_authenticated:
        saludo = "Bienvenido" 
    contexto = {
        "titulo":titulo,
        "saludo":saludo,
    }
    return render(request, 'index.html',contexto)

#@login_required(login_url='/accounts/login/')
def analisis_model_form_crear(request):
    titulo = "Crear Análisis"
    formulario = AnalisisModelForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():
        instancia = formulario.save(commit=False)
        instancia.user = request.user  # Set the user
        instancia.file = request.FILES['file']  # Handle file upload
        instancia.save()

        valores = formulario.cleaned_data.get("tipo_analisis")
        fec_1 = datetime.strftime(formulario.cleaned_data.get("fecha_inicio"), '%d,%m,%Y,%H,%M,%S')
        fec_2 = datetime.strftime(formulario.cleaned_data.get("fecha_paso"), '%d,%m,%Y,%H,%M,%S')
        fec_3 = datetime.strftime(formulario.cleaned_data.get("fecha_fin"), '%d,%m,%Y,%H,%M,%S')

        try:
            with transaction.atomic():
                for k in valores:
                    if k == 'CEP':
                        last_cep = CEP.objects.all().last()
                        new_id_cep = 1 if last_cep is None else last_cep.id_cep + 1
                        CEP.objects.get_or_create(id_cep=new_id_cep, analisis_id=instancia.id_analisis)
                    elif k == 'FDA':
                        last_fda = FDA.objects.all().last()
                        new_id_fda = 1 if last_fda is None else last_fda.id_fda + 1
                        FDA.objects.get_or_create(id_fda=new_id_fda, analisis_id=instancia.id_analisis)

                subprocess.Popen(f'python aepro/task_matlab.py {instancia.id_analisis} {fec_1} {fec_2} {fec_3}', shell=True)
        except Exception as e:
            print(e)

        return render(request, 'analisis_done.html')

    context = {
        "titulo_form": titulo,
        "form": formulario,
    }
    return render(request, "analisis_create_view.html", context)

class AnalisisListView(ListView):
    model = Analisis
    template_name = "analisis_list_view.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(AnalisisListView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AnalisisListView, self).get_context_data(**kwargs)
        context['procesos_activos'] = get_pid("MATLAB")
        return context


class AnalisisDetailView(DetailView):
    model = Analisis
    template_name= "analisis_detail_view.html"#template: object
    #method flowchart: metodos que se puede usar en DetailView
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDetailView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)



class AnalisisDeleteView(DeleteView):
    model = Analisis 
    template_name = 'analisis_delete_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDeleteView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)

    def get_success_url(self):
        return reverse('analisis_listcbv')

class AnalisisDeleteViewError(DeleteView):
    model = Analisis 
    template_name = 'analisis_delete_view_error.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(AnalisisDeleteViewError, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)
    def get_success_url(self):
        return reverse('analisis_listcbv')

class Analisis_FDA_UpdateView(UpdateView):#--> models:Analisis:get_absolute_url
    model = Analisis
    form_class = UpdateResultadoFDA,
    #fields = ['titulo_descriptivo','comentario']
    
    template_name = 'analisis_update_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(Analisis_FDA_UpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)

    def get(self, request,  *args, **kwargs):
        self.object = Analisis.objects.get(id_analisis=kwargs['pk'])
        id_analisis = kwargs['pk']
        analisis = self.model.objects.get(id_analisis=id_analisis)
        f=analisis.analisis_fda.id_fda
        
        form_class = self.get_form_class()
        form = UpdateResultadoFDA(initial={'titulo_descriptivo':analisis.titulo_descriptivo,
                                  'comentario':analisis.comentario,
                                  'nombre_grafica':analisis.analisis_fda.resultados['nombre_grafica'],
                                  'xasix':analisis.analisis_fda.resultados['xasix'],
                                  'yasix':analisis.analisis_fda.resultados['yasix'],
                                  })
        
        context = self.get_context_data(object=self.object, form=form)
        context['xasix'] = analisis.analisis_fda.resultados['xasix'] #whatever you would like
         
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
         context = super(Analisis_FDA_UpdateView, self).get_context_data(**kwargs)
         return context

    def post (self, request, *args, **kwargs):
        self.object = self.get_object
        id_analisis = kwargs['pk']
        analisis = self.model.objects.get(id_analisis=id_analisis)
        #res_fda = FDA.objects.get(analisis_id=id_analisis)
        #recoger la informacion del formulario
        #Para analisis guardamos el titulo y el comentario
        formulario = self.form_class(request.POST, instance=analisis) # sino se indica la instancia, generaria uno nuevo
        if formulario.is_valid():
          datos_formulario = formulario.cleaned_data
          #formulario['xasix']=analisis.analisis_fda.resultados['xasix']

          nombre_grafica=datos_formulario.get("nombre_grafica")
          xasix=datos_formulario.get("xasix")
          yasix=datos_formulario.get("yasix")

          #Para el resultado fda guardamos los ejes y el titulo de la grafica
          
          #analisis.analisis_fda.resultados['xasix']
          valores = {
                  "x":analisis.analisis_fda.resultados['x'],
                  "y":analisis.analisis_fda.resultados['y'],
                  "nombre_grafica":nombre_grafica,
                  "xasix":xasix,
                  "yasix":yasix,

          }
          FDA.objects.filter(analisis=id_analisis).update(resultados=valores)
          formulario.save()
          return HttpResponseRedirect(self.get_success_url())
        else:
          return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
      return reverse('detalle_resultado_fda', args=(self.kwargs['pk'],))
      #return reverse('detalle_resultado_fda', args=(self.object.id_analisis,))
    


class Analisis_CEP_UpdateView(UpdateView):#--> models:Analisis:get_absolute_url
    model = Analisis 
    fields = ['titulo_descriptivo','comentario']
    
    template_name = 'analisis_update_view.html'

    #Filtrar los resultados solo para el usuario que realiza la solicitud
    def get_queryset(self, *args,  **kwargs):
        qs = super(Analisis_CEP_UpdateView, self).get_queryset(*args, **kwargs).filter(user=self.request.user)
        return (qs)
        
    def get_success_url(self, **kwargs):
      return reverse('detalle_resultado_cep', args=(self.object.id_analisis,))

#@login_required(login_url='/accounts/login/')
def detalle_resultado_fda(request, pk):
    titulo = "Resultado del Analisis Funcional de Datos"
    analisis = get_object_or_404(Analisis, pk=pk, user=request.user)
    periodo = analisis.periodo

    x = analisis.analisis_fda.resultados['x']
    y = analisis.analisis_fda.resultados['y']

    # trace_r = [go.Scatter(y=x[i], mode="lines", name=f'{periodo}: {i+1}', marker={'color': 'grey'}) for i in range(len(x))]
    # trace_out = [go.Scatter(y=x[y[i]-1], mode="lines", name=f'Outlier ->: {periodo}: {y[i]}', marker={'color': 'red'}) for i in range(len(y))]

    # data = trace_r + trace_out
    # layout = go.Layout(title=analisis.analisis_fda.resultados['nombre_grafica'], xaxis={'title': analisis.analisis_fda.resultados['xasix']}, yaxis={'title': analisis.analisis_fda.resultados['yasix']})
    # figure = go.Figure(data=data, layout=layout)
    # div = opy.plot(figure, auto_open=False, output_type='div')

    contexto = {
        "titulo": titulo,
        "resultado_form": analisis,
        "resultado_id": pk,
        # 'graph2': div,
    }
    return render(request, "analisis_resultado_detail_fda.html", contexto)

#@login_required(login_url='/accounts/login/')
def detalle_resultado_cep(request, pk):
    # Controlar que cada usuario solo puede ver sus resultados
    titulo="Resultado del Analisis Vectorial"
    a=Analisis.objects.filter(user_id=request.user.id)
    template = "analisis_resultado_detail_cep2.html"
    resultado = get_object_or_404(a, pk=pk)
    periodo=resultado.periodo

    resultados = resultado.analisis_cep.resultados
    
    
    #GRAFICA 0 - HISTOGRAMA+CURVA
    x = resultados['datos'][0]  
    hist_data = [x]
    group_labels = ['valores']
    fig = ff.create_distplot(hist_data, group_labels,curve_type='normal')
    fig['layout'].update(title='Histograma')
    div0 = opy.plot(fig,auto_open=False,image='jpeg',output_type='div')#output_type='div' auto_open=False, output_type='div'



    #GRAFICA 1 - BOXPLOT
    trace1 = {
      #"x": resultados['datos'],
      "y": resultados['datos'][0],
      "marker": {"color": "#4CAF50"}, 
      "name": "C02", 
      "type": "box", 
      "xaxis": "x1", 
      "yaxis": "y1"
    }
    

    data=go.Data([trace1])
    layout=go.Layout(title = "Boxplot")
    figure=go.Figure(data=data,layout=layout)
    div1 = opy.plot(figure, auto_open=False, output_type='div')

    
    data2 = go.Data([trace0,trace1])
    layout=go.Layout()
    figure2=go.Figure(data=data2,layout=layout)
    div2 = opy.plot(figure2, auto_open=False, output_type='div')

    # #GRAFICA 3 - DISTRIBUCION NORMAL

    # #GRAFICA 4 - AUTOCORRELACION

    #GRAFICA 5 - X-BAR
    xbar_x=[] # eje x
    for i in range(len(resultados['imr_img']['pts'])):
      xkkk.append(i)

    outx = []
    outy = []

    for i in range(len(resultados['imr_img']['ooc'])):
      if resultados['imr_img']['ooc'][i]==1:
        outx.append(i)

    if len(outx)>0:
      j=0
      for i in range(len(resultados['imr_img']['ooc'])):
        if i==outx[j]:
          outy.append(resultados['imr_img']['pts'][i])
          j=j+1


    trace1 = {#PUNTOS
    
      "x": xbar_x,
      "y": resultados['imr_img']['pts'],
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(0,116,217)", 
        "thickness": 1, 
        "width": 1
      }, 
      "line": {
        "color": "rgb(0,116,217)", 
        "width": 2
      }, 
      "marker": {
        "color": "rgb(0,116,217)", 
        "size": 8, 
        "symbol": "circle"
      }, 
      "mode": "lines+markers", 
      "name": "Valores", 
      "showlegend": True, 
      "type": "scatter", 
      "uid": "cb8982", 
      "visible": True, 
      "xaxis": "x", 
      "yaxis": "y"
    }
    trace2 = {#OUTLIERS
      "x": outx,
      "y": outy,
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(255,65,54)", 
        "thickness": 1, 
        "width": 1
      }, 
      "line": {
        "color": "rgb(255,65,54)", 
        "width": 2
      }, 
      "marker": {
        "color": "rgb(255,65,54)", 
        "line": {"width": 3}, 
        "opacity": 0.5, 
        "size": 12, 
        "symbol": "circle-open"
      }, 
      "mode": "markers", 
      "name": "Outliers", 
      "showlegend": True, 
      "type": "scatter", 
      "uid": "d7228d", 
      "visible": True, 
      "xaxis": "x", 
      "yaxis": "y"
    }
    trace3 = {#LINEA CENTRAL
      "x": len(resultados['imr_img']['pts']),#[0.5, 36.5], 
      "y": resultados['imr_img']['cl'],#[-0.086389, -0.086389], 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(133,20,75)", 
        "thickness": 1, 
        "width": 1
      }, 
      "line": {
        "color": "rgb(133,20,75)", 
        "width": 2
      }, 
      "marker": {
        "color": "rgb(133,20,75)", 
        "size": 8, 
        "symbol": "circle"
      }, 
      "mode": "lines", 
      "name": "Centro", 
      "showlegend": True, 
      "type": "scatter", 
      "uid": "135942", 
      "visible": True, 
      "xaxis": "x", 
      "yaxis": "y"
    }
    trace4 = {#LIMITE SUPERIOR 
      "x": len(resultados['imr_img']['pts']),#[0.5, 36.5, None, 0.5, 36.5], 
      "y": resultados['imr_img']['ucl'],#[-0.281712, -0.281712, None, 0.108934, 0.108934], 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(255,133,27)", 
        "thickness": 1, 
        "width": 1
      }, 
      "line": {
        "color": "rgb(255,133,27)", 
        "width": 2
      }, 
      "marker": {
        "color": "rgb(255,133,27)", 
        "size": 8, 
        "symbol": "circle"
      }, 
      "mode": "lines", 
      "name": "Limite superior", 
      "showlegend": True, 
      "type": "scatter", 
      "uid": "df651f", 
      "visible": True, 
      "xaxis": "x", 
      "yaxis": "y"
    }
    trace5 = {#LIMITE INFERIOR
      "x": len(resultados['imr_img']['pts']),#[0.5, 36.5, None, 0.5, 36.5], 
      "y": resultados['imr_img']['lcl'],#[-0.281712, -0.281712, None, 0.108934, 0.108934], 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(255,133,27)", 
        "thickness": 1, 
        "width": 1
      }, 
      "line": {
        "color": "rgb(255,133,27)", 
        "width": 2
      }, 
      "marker": {
        "color": "rgb(255,133,27)", 
        "size": 8, 
        "symbol": "circle"
      }, 
      "mode": "lines", 
      "name": "Limite inferior", 
      "showlegend": True, 
      "type": "scatter", 
      "uid": "df651f", 
      "visible": True, 
      "xaxis": "x", 
      "yaxis": "y"
    }
    data5 = go.Data([trace1,trace2,trace3, trace4,trace5])#, trace2, trace3, trace4,trace5])
    layout=go.Layout(title=resultado.analisis_cep.resultados['xbar_nombre_grafica'], xaxis={'title':resultado.analisis_cep.resultados['xbar_xasix']}, yaxis={'title':resultado.analisis_cep.resultados['xbar_yasix']})
    #layout=go.Layout()
    figure5=go.Figure(data=data5,layout=layout)
    div5 = opy.plot(figure5, auto_open=False, output_type='div')



    contexto = {
        "titulo":titulo,
        "resultado_form":resultado,
        "resultado_id":pk,
        "al":resultados,
        'graph0':div0, #histogram con curva
        'graph1':div1,#bosplot
        'graph5':div5, #X-BAR

    }
    return render(request, template, contexto)



def contacto(request):
    formulario = FormularioContacto(request.POST or None)

    if formulario.is_valid():
        form_email =  formulario.cleaned_data.get("email")
        form_mensaje = formulario.cleaned_data.get("mensaje")
        form_nombre = formulario.cleaned_data.get("nombre")
        email_asunto = 'Email de Contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_from,"merc303@gmail.com"]
        email_mensaje = " %s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
        send_mail(
            email_asunto,
            email_mensaje,
            email_from,
            email_to,
            fail_silently=False
            )
    titulo = "contacto"
    contexto = {
        "titulo":titulo,
        "form":formulario,
    }
    plantilla = "aepro_contacto.html"

    #************** return HttpResponseRedirect('/') -> mensaje enviado
    return render (request,plantilla,contexto)

#@login_required(login_url='/accounts/login/')
def ValidarFichero(request):
  estado = ''
  if request.method == 'POST':
    formulario = ValidacionFicheroForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():
      estado = 'Formato correcto'

  else:
        formulario = ValidacionFicheroForm()

  titulo = "Validar Fichero"
  contexto = {
        "estado":estado,
        "titulo":titulo,
        "form":formulario,
    }
  plantilla = "validar_file.html"
  return render (request,plantilla,contexto)

