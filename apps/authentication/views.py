from rest_framework import generics, status
from .serializers import UserRegisterEmailPasswordSerializer, NameDOBSerializer
from rest_framework.response import Response


class RegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterEmailPasswordSerializer
    name_dob_serializer = NameDOBSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'email' in kwargs:
            print(kwargs['email'])
            if kwargs['step'] == 1:
                serializer = self.name_dob_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(email=kwargs['email'])
            if kwargs['step'] == 2:
                pass
        else:
            print('Hello there')
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_201_CREATED)


