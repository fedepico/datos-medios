from django import forms
#widget que permite usar datetiempicker en el formulario para seleccion dia y hora
from bootstrap3_datetime.widgets import DateTimePicker
#/Users/usuario/Desktop/DateTime/lib/python3.4/site-packages/bootstrap3_datetime/widgets.py
#from django.forms.utils import flatatt
from .models import Analisis

#comprobar el formato del archivo que suben los usuarios clean_file
from mimetypes import MimeTypes
from django.core.files.uploadedfile import TemporaryUploadedFile
import xlrd
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from itertools import takewhile
from datetime import datetime, timedelta
from django.forms.widgets import CheckboxSelectMultiple


def column_len(sheet, index):
	"""funcion que recibe una hoja y una columna y devuelve el numero de registros"""
	col_values = sheet.col_values(index)
	col_len = len(col_values)
	for _ in takewhile(lambda x: not x, reversed(col_values)):
		col_len -= 1
	return col_len



#Puede usarse en Admin, en vez de Meta: Modelo

class AnalisisModelForm(forms.ModelForm):
    file = forms.FileField(allow_empty_file=True, help_text="Solo se permite subir archivos en formato XLS!!!!")

    fecha_inicio = forms.DateTimeField(required=False, widget=DateTimePicker(options={
        "format": "YYYY-MM-DD HH:mm",
        "pickSeconds": False,
    }))
    fecha_paso = forms.DateTimeField(required=False, widget=DateTimePicker(options={
        "format": "YYYY-MM-DD HH:mm",
        "pickSeconds": False,
    }))
    fecha_fin = forms.DateTimeField(required=False, widget=DateTimePicker(options={
        "format": "YYYY-MM-DD HH:mm",
        "pickSeconds": False,
        'locale': 'es',
    }))
    tipo_analisis = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=Analisis.OPERACIONES,
        initial=('CEP',)
    )

    class Meta:
        model = Analisis
        fields = [
            "titulo_descriptivo",
            "periodo",
            "tipo_analisis",
            "fecha_inicio",
            "fecha_paso",
            "fecha_fin",
            "comentario",
        ]
        labels = {
            "titulo_descriptivo": 'Titulo',
            "periodo": 'Seleciona Periodo',
            "tipo_analisis": 'Selecciona el analisis a realizar',
            "comentario": 'Indica un comentario si es necesario',
            "file": 'Archivo'
        }
        widgets = {
            "tipo_analisis": forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            "file": "Solo se permite subir archivos en formato XLS",
        }
        error_messages = {
            # 'file': 'Solo se perminte XLS',
        }

    def clean(self):
        cleaned_data = super(AnalisisModelForm, self).clean()
        f1 = cleaned_data.get('fecha_inicio')
        f2 = cleaned_data.get('fecha_paso')
        f3 = cleaned_data.get('fecha_fin')
        pa = cleaned_data.get('periodo')
        ta = cleaned_data.get('tipo_analisis')

        if f1 and f2 and f3:
            if not f1 <= f2:
                raise forms.ValidationError("La fecha de paso es inferior a la inicio!")
            if not f1 < f3:
                raise forms.ValidationError("La fecha final es inferior a la inicio!")
            if not f2 < f3:
                raise forms.ValidationError("La fecha final es inferior a la de paso!")
            if pa == 'AÑO' and (f3 - f1).days <= 731:
                raise forms.ValidationError("El periodo de analisis tiene que comprender como minimo 2 años")
            if pa == 'MES' and (f3 - f1).days <= 60:
                raise forms.ValidationError("El periodo de analisis tiene que comprender como minimo 2 meses")
            if pa == 'DIA' and int((f3 - f1).total_seconds() / 3600) <= 48:
                raise forms.ValidationError("El periodo de analisis tiene que comprender como minimo 2 dias")
            if 'FDA' in ta and pa == 'DIA' and (f3 - f1).days >= 731:
                raise forms.ValidationError("El periodo de analisis NO puede ser superior a 2 años ...")

    def clean_file(self):
        file = self.files.get('file')
        if file:
            path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            mime = MimeTypes()
            mime_type = mime.guess_type(file.name)[0]

            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                try:
                    book = xlrd.open_workbook(tmp_file)
                    first_sheet = book.sheet_by_index(0)

                    if first_sheet.ncols == 2:
                        if self.column_len(first_sheet, 0) >= 24:
                            cell_0 = first_sheet.cell(0, 0)
                            cell_1 = first_sheet.cell(1, 0)
                            nn = self.column_len(first_sheet, 0)
                            cell_n = first_sheet.cell(nn - 1, 0)

                            cell0 = xlrd.xldate.xldate_as_datetime(cell_0.value, 0)
                            cell1 = xlrd.xldate.xldate_as_datetime(cell_1.value, 0)
                            celln = xlrd.xldate.xldate_as_datetime(cell_n.value, 0)

                            f11 = datetime.strftime(cell0, '%d/%m/%Y %H:%M:%S')
                            f22 = datetime.strftime(cell1, '%d/%m/%Y %H:%M:%S')
                            f33 = datetime.strftime(celln, '%d/%m/%Y %H:%M:%S')

                            f1 = self.cleaned_data['fecha_inicio']
                            f2 = self.cleaned_data['fecha_paso']
                            f3 = self.cleaned_data['fecha_fin']
                            f_11 = datetime.strftime(f1, '%d/%m/%Y %H:%M:%S')
                            f_22 = datetime.strftime(f2, '%d/%m/%Y %H:%M:%S')
                            f_33 = datetime.strftime(f3, '%d/%m/%Y %H:%M:%S')

                            if not (f_11 == f11 and f_22 == f22 and f_33 == f33):
                                raise forms.ValidationError("Las fechas introducidas y las del fichero no coinciden")

                            for reg in range(0, first_sheet.nrows):
                                if first_sheet.cell_type(reg, 0) != 3:
                                    raise forms.ValidationError("Error: algun registro no esta en formato fecha")
                                if not (first_sheet.cell_type(reg, 1) == 2 or first_sheet.cell_type(reg, 1) == 0):
                                    raise forms.ValidationError("Error: algun registro no esta en formato numero o blanco")

                            return file
                        else:
                            raise forms.ValidationError("No es un formato valido: requiere al menos 24 registros")
                    else:
                        raise forms.ValidationError("No es un formato valido: requiere exactamente 2 columnas")
                except xlrd.XLRDError:
                    raise forms.ValidationError("No es un fichero valido: error de lectura")
                finally:
                    os.remove(tmp_file)
            else:
                raise forms.ValidationError("No es un formato valido: se requiere un archivo '.xls' o '.xlsx'")
        else:
            raise forms.ValidationError("No se ha proporcionado ningún archivo")


class UpdateResultadoFDA(forms.ModelForm):
	nombre_grafica = forms.CharField(max_length=50)
	xasix = forms.CharField(max_length=20)
	yasix = forms.CharField(max_length=20)
 
	class Meta:
		model = Analisis
		fields = ['titulo_descriptivo','comentario']


class FormularioContacto(forms.Form):
	nombre = forms.CharField(max_length=100)#required=false
	email =  forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		#validaciones
		return email


class ValidacionFicheroForm(forms.Form):
	file = forms.FileField(label='Archivo',
							help_text="Solo se permite subir archivos en formato .xls o xlsx")
	
	#Validar el fichero
	def clean_file(self):
		file = self.files['file']
		#temporalmente se guarda el fichero para comprobar su formato y estructura
		path = default_storage.save(("tmp/{}").format(file), ContentFile(file.read()))
		tmp_file = os.path.join(settings.MEDIA_ROOT, path)
		
		if file:
			mime = MimeTypes()
			mime_type = mime.guess_type(file.name)[0]
			# xls = application/vnd.ms-excel
			# xlsx = application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
			if (mime_type == 'application/vnd.ms-excel'  or mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
				try:
					xlrd.open_workbook(tmp_file)#BLOQUE TRY CATCH ???
					book = xlrd.open_workbook(tmp_file)
					#if book.sheet_by_index(0)>0:
					first_sheet = book.sheet_by_index(0)#seleccionamos la primera hora del fichero excel
					# La columna 0 contiene fecha No puede tener registros en blanco
					if first_sheet.ncols==2:
						#definimos un funcion que permita saber cuantos registros tiene una columna, ya que recorremos todos los regitros de cada columna
						#comprobamos el numero de registros de la columna0
						if column_len(first_sheet,0)>=24:
							# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
							#Comprobar que la comlumna 0 sean valores: 3
							#Comprobar que la comlumna 1 sean valores: 2 o 6 # F=0 C=0/1
							#comprobar que los campos fecha son fecha
							for reg in range(0,first_sheet.nrows):
								if first_sheet.cell_type(reg,0)!=3: # Si no es un campo fecha Error
									raise forms.ValidationError("Error: algun registro no esta en formato fecha")
							#comprar que los valores de la columna 2 son : numeros vacios o blancos
							for reg in range(0,first_sheet.nrows):
								if not(first_sheet.cell_type(reg,1)==2 or first_sheet.cell_type(reg,1)==0): # Si no es un campo fecha Error
									raise forms.ValidationError("Error algun registro no esta en formato numero o blanco")
							
							return file#Devolvemos el fichero

						else:#column_len(first_sheet,0)>=24:
							raise forms.ValidationError("No es un formato valido: + >24 registros")
					
					else:
						raise forms.ValidationError("No es un formato valido: solo 2 columnas")



				except xlrd.XLRDError as e:# if xlrd.open_workbook(tmp_file): -->CATCH
					raise forms.ValidationError("No es un fichero valido: XLRDError")
				finally:
					os.remove(tmp_file)#ELEMINAR EL ARCHIVO TEMPORAL
					
			else: #if (mime_type == 'application/vnd.ms-excel'  or mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
				os.remove(tmp_file)#ELEMINAR EL ARCHIVO TEMPORAL	
				raise forms.ValidationError("No es un formato valido : '.xls'")
					

				