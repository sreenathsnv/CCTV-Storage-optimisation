from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import FootagesSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# @api_view(['POST'])
# def loginUser(request):
#     if request.method == 'POST':
#         user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
#         if user:
          
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def loginUser(request):
    if request.method == 'POST':
        # Accessing data using request.data instead of request.POST
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user:
            # If user is authenticated, create or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            # If authentication fails, return error response
            return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fileUpload(request):
    data = request.data
    print(data)
    # Add the user instance to the data dictionary
    data['user'] = request.user.id

    # Serialize the request data
    footage = FootagesSerializer(data=request.data, context={'request': request})

    # Validate and save the serialized data
    if footage.is_valid():
        footage.save()
        return Response(footage.data, status=status.HTTP_201_CREATED)
    return Response(footage.errors, status=status.HTTP_400_BAD_REQUEST)
