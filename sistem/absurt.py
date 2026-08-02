from django.contrib.auth.models import User
from sistem.models import Profile

user = User.objects.create_user('tekniker1', password='123456')
profile = Profile.objects.get(user=user)
profile.role = 'tekniker'
profile.save()
