from flask import request

class RegistrationForm:
	users = []
	def get_registration_details(self):
		self.f_name = request.form.get("first_name")
		self.l_name = request.form.get("last_name")
		self.email = request.form.get("email")
		self.address1 = request.form.get("Address1")
		self.address2 = request.form.get("Address2")
		self.city = request.form.get("City")
		self.state = request.form.get("State")
		self.zipcode = request.form.get("Postal")
		self.phone = request.form.get("phone")
		self.birth_date = request.form.get("bday")

class LoginForm:
	def get_login_details(self):
		self.email_id = request.form.get("email")
		self.password = request.form.get("password")

