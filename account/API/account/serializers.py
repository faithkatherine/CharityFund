from rest_framework import serializers
from account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):

	class Meta:
		confirm_password = serializers.CharField(style = {'input_type': 'password'}, read_only=True)

		model = Account
		fields = {"email", "username", "password", "confirm_password", "organization", "registration_code"}

		extra_kwargs = {
		'password' : {'write_only' : True}
		}


	def save(self):
		account = Account(

			email = self.validated_data['email'],
			username = self.validated_data['username'],

			)
		password = self.validated_data['password']
		confirm_password = self.validated_data['confirm_password']

		if password != confirm_password:
			raise serializers.ValidationError({'password': 'Passwords must match'})

		account.set_password(password)
		account.save()
		return account

