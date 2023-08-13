from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
import requests
from bs4 import BeautifulSoup
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def get_token(self, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        return token


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            serializer = UserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
    
            response_data = {
                "user": data,
            }

            response = Response(response_data, status=status.HTTP_200_OK)

            response.set_cookie(
                "token", token.access_token, httponly=True
            )  
            return response
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        response = Response({"msg": "User logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie("token")  
        return response

class ScrapeProductView(APIView):
        
	def get(self, request, *args, **kwargs):
		user = request.user
		if not user.is_authenticated:
			return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
		products = Product.objects.filter(user=user)
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request, *args, **kwargs):
		user = request.user
		if not user.is_authenticated:
			return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
		url = request.data.get('url')
		if Product.objects.filter(url=url,user=user).exists():
			det=Product.objects.filter(url=url,user=user)
			serializer=ProductSerializer(det,many=True)
			return Response({'message': 'This URL is already scraped.','Details':serializer.data}, status=status.HTTP_400_BAD_REQUEST)
		try:
			response = requests.get(url)
			soup = BeautifulSoup(response.content, 'html.parser')
			title = soup.find('span', {'class': 'B_NuCI'}).text.strip()
			price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.replace('₹', '').replace(',', '').strip()
			description_elem = soup.find('div', {'class': '_2o-xpa'})
			description=''
			if description_elem and description_elem.div.p is not None:
				description = description_elem.div.p.text.strip() if description_elem else ''
			elif description_elem:
				description = description_elem.text.strip() if description_elem else ''
			rating_count_elem = soup.find('span', {'class': '_2_R_DZ'})
			if len(rating_count_elem.span.find_all('span'))==2:
				rating_count = int(rating_count_elem.span.span.text.split()[0].replace(',','')) if rating_count_elem else 0
				review_count=int(rating_count_elem.span.find_all('span')[2].text.split()[0])
			else:
				rating_count=int(rating_count_elem.span.text.split()[0].replace(',','')) if rating_count_elem else 0
				review_count=int(rating_count_elem.span.text.split()[-2].replace(',','')) if rating_count_elem else 0
			ratings_elem = soup.find('div', {'class': '_3LWZlK'})
			rating = float(ratings_elem.text) if ratings_elem else 0.0
			media_count = (soup.find('ul', {'class': '_3GnUWp'}))
			media_count = len(media_count) if media_count else 0
			details = {
				'title': title,
				'price': price,
				'description': description,
				'rating': rating,
				'rating_count': rating_count,
				'review_count': review_count,
				'media_count': media_count
			}
			product = Product(
				user=user,
				url=url,
				title=title,
				price=price,
				description=description,
				reviews_count=review_count,
				ratings_count=rating_count,
				ratings=rating,
				media_count=media_count
			)
			product.save()
			return Response({'message': 'Product data scraped and saved successfully.','details':details}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'detail':"Enter the correct url"+str(e)}, status=status.HTTP_400_BAD_REQUEST)
