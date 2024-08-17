from django.views.decorators.csrf import csrf_exempt
from ..controllers import CompanyController

class CompanyView():
    @csrf_exempt
    def companyAPI(request, id = 0):
        if request.method == 'POST':
            return CompanyController.createCompany(request)
        elif request.method == 'GET':
            return CompanyController.getCompanies()
        elif request.method == 'PUT':
            return CompanyController.updateCompany(request)
        elif request.method == 'DELETE':
            return CompanyController.deleteCompany(id)
