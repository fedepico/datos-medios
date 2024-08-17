from rest_framework import serializers
from login.models import User, Account, Company
from .account_serializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta: 
       model = User
       fields = ['id', 'username', 'password', 'name', 'email', 'account']

    #deserializar de JSON a un Objeto 
    def create(self, validated_data):
        account_data = validated_data.pop('account', None)
        if not account_data:
            raise serializers.ValidationError({'account': 'Los datos de la cuenta son requeridos.'})
        
        company_data = account_data.pop('company', None)
        if not company_data:
            raise serializers.ValidationError({'account': {'company': 'La compañía es requerida.'}})
        
        try:
            company_instance = Company.objects.get(**company_data)
        except Company.DoesNotExist:
            raise serializers.ValidationError({'account': {'company': 'La compañía especificada no existe.'}})
        
        user_instance = User.objects.create(**validated_data)
        if user_instance and user_instance.id:
            Account.objects.create(user=user_instance, company=company_instance, **account_data)
            return user_instance
        else:
            raise serializers.ValidationError({'account': {'user': 'Error al intentar crear el usuario.'}})
    
    #serializar de Objeto a un JSON
    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        account = Account.objects.get(user=obj.id)
        return {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'account': {
                        'id': account.id,
                        'company': {
                            'id': account.company.id,
                            'name': account.company.name
                        },
                        'last_change_date': account.last_change_date,
                        'is_active': account.is_active
                    }
                }