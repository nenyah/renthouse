from workapp.models import Area, HouseInfo
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

class AreaSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(min_length=1)

    class Meta:
        model = Area
        fields = '__all__'
        depth = 1

class HouseSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(min_length=1)

    class Meta:
        model = HouseInfo
        fields = '__all__'
        depth = 1

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def house(request):
    house_list = HouseInfo.objects.all()
    if request.method == 'GET':
        serializer = HouseSerializer(house_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def area(request):
    area_list = Area.objects.all()
    if request.method == 'GET':
        serializer = AreaSerializer(area_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def onehouse(request, id):
    try:
        house = HouseInfo.objects.get(id=id)
        serializer = HouseSerializer(house)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        body = {"msg": "Unsuccessful"}
        return Response(body, status=status.HTTP_403_FORBIDDEN)
