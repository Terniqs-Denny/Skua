from datetime import timezone
import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User 
from userauth.models import BlacklistedToken, UserSession

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for Django REST Framework
    """
    
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = self.get_token_from_header(request)
        if jwt_token is None:
            return None

        try:
            # Decode the JWT
            payload = self.decode_token(jwt_token)
            
            # Check if token has been blacklisted
            self.check_blacklist(jwt_token)
            
            # Get the user from the payload
            user = self.get_user(payload)
            
            # Validate token type is 'access'
            self.validate_token_type(payload)
            
            # Update last activity in user session
            self.update_user_session(user)
            
            return (user, jwt_token)
            
        except Exception as e:
            raise AuthenticationFailed(f'Invalid authentication: {str(e)}')
    
    def get_token_from_header(self, request):
        """Extract token from the request header"""
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
            
        return parts[1]
        
    def decode_token(self, token, allow_expired=False):
        """Decode and validate the token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SETTINGS['SECRET_KEY'],
                algorithms=[settings.JWT_SETTINGS['ALGORITHM']],
                options={"verify_exp": not allow_expired}
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
    
    def check_blacklist(self, token):
        """Check if the token is blacklisted"""
        is_blacklisted = BlacklistedToken.objects.filter(token=token).exists()
        if is_blacklisted:
            raise AuthenticationFailed('Token is blacklisted')
    
    def get_user(self, payload):
        """Get the user from the payload"""
        user_id = payload.get(settings.JWT_SETTINGS['USER_ID_CLAIM'])
        if not user_id:
            raise AuthenticationFailed('User identifier not found in token')
            
        try:
            user = User.objects.get(id=user_id, is_active=True)
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found or inactive')
    
    def validate_token_type(self, payload):
        """Ensure the token is an access token"""
        token_type = payload.get(settings.JWT_SETTINGS['TOKEN_TYPE_CLAIM'])
        if token_type != settings.JWT_SETTINGS['TOKEN_TYPE_ACCESS']:
            raise AuthenticationFailed('Token is not an access token')
    
    def update_user_session(self, user):
        """Update the last activity timestamp in the user session"""
        try:
            session = UserSession.objects.filter(user_id=user, is_active=True).first()
            if session:
                session.last_activity = timezone.now()
                session.save(update_fields=['last_activity'])
        except Exception:
            # Don't fail authentication if session update fails
            pass
            
