from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from ..models import Company
from ..serializers import CompanySerializer

class CompanyController():
    def createCompany(company):
        company_data = JSONParser().parse(company)
        company_serialized = CompanySerializer(data=company_data)
        if company_serialized.is_valid():
            company_serialized.save()
            return JsonResponse(company_serialized.data, safe=False)
        return JsonResponse("No se pudo crear la compañía.", safe=False)
    
    def getCompanies():
        companies = Company.objects.all()
        companies_serialized = CompanySerializer(companies, many = True)
        return JsonResponse(companies_serialized.data, safe=False)

    def updateCompany(company):
        company_data = JSONParser().parse(company)
        company_to_modificate = Company.objects.get(id = company_data["id"])
        company_serialized = CompanySerializer(company_to_modificate, data=company_data)
        if company_serialized.is_valid():
            company_serialized.save()
            return JsonResponse(company_serialized.data, safe=False)
        return JsonResponse("Falló al tratar de modificar la compañía.", safe=False)
    
    def deleteCompany(id):
        company_to_delete = Company.objects.get(id = id)
        company_to_delete.delete()
        return JsonResponse("Compañía eliminada con exito.", safe=False)
