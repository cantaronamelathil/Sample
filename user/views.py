from django.shortcuts import render
from rest_framework import generics,permissions,status
from .models import UserModel
from .serializers import UserSerializer,LoginSerializer,BlockUserSerializer
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
# Create your views here.
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class LoginView(generics.GenericAPIView):
        serializer_class = LoginSerializer
        permission_classes = [permissions.AllowAny]
        
        def post(self,request,*args,**kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            #if valid the serializer returns a user object
            user = serializer.validated_data
            print(user)
            #create or retrieve the token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)  
            return Response({"token":token.key},status=status.HTTP_200_OK)
 
 
class StaffListView(generics.ListAPIView):
    queryset = UserModel.objects.filter(role =UserModel.STAFF)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]   
    
    def get(self,request,*args, **kwargs):
        if  not request.user.is_admin():
            return Response({"detail": "You do not have permisssion to perform this action."}, status = status.HTTP_403_FORBIDDEN)
        return super().get(request,*args,**kwargs)


class BlockStaffView(generics.UpdateAPIView):
    queryset = UserModel.objects.filter(role ='staff')
    serializer_class = BlockUserSerializer
    permission_classes = [permissions.IsAuthenticated]
                     
                     
    def update(self,request,*args,**kwargs):
        if not request.user.is_admin():
            return Response({"detail": "Not authorized."},status = status.HTTP_403_FORBIDDEN)
        # return super().update(request, *args,**kwargs)
        
        
        partial = True
        serializer = self.get_serializer(self.get_object(),data = request.data,partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        return Response(serializer.data)
                    
class DeleteStaffView(generics.DestroyAPIView):
    queryset = UserModel.objects.filter(role = 'staff')
    serializer_class = UserSerializer
    permission_classes =  [permissions.IsAuthenticated]
    
    
    def destroy(self,request,*args,**kwargs):
        if not request.user.is_admin():
            return Response({"detail":"Not authorized."},status = status.HTTP_403_FORBIDDEN)
        response = super().destroy(request,*args,**kwargs)                     
        return Response({"detail": "Staff member deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,*args,**kwargs):
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
                return Response({"detail":"Successfully logged out."}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)