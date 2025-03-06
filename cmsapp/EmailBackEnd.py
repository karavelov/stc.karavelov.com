import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"🔍 В authenticate() -> username: {username}")

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            print(f"✅ Потребител открит: {user.email}")
        except UserModel.DoesNotExist:
            print("❌ Потребителят не съществува!")
            return None

        # 🔥 Премахваме `bcrypt$$`, ако съществува
        stored_password = user.password
        if stored_password.startswith("bcrypt$$"):
            stored_password = stored_password.replace("bcrypt$$", "")

        print(f"🔑 Очакван хеш: {stored_password}")

        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("✅ Паролата е правилна!")
            return user
        else:
            print("❌ Грешна парола!")
            return None
