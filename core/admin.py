from django.contrib import admin

from core.models import Account


class AccountAdmin(admin.ModelAdmin):
	exclude = ('owner', )
	list_display = ('name', 'balance', 'creation_date', 'owner', )
	readonly_fields = ('balance', )
	search_fields = ('name', )

	def save_model(self, request, obj, form, change):
		"""
		Checks if object has no attribute owner (so is a insert operation,
		because it is removed from admin form) to set current 
		user to owner and initial balance to current balance
		"""
		if not hasattr(obj, 'owner'):
			obj.owner = request.user
			obj.balance = obj.init_balance
		obj.save()

	def get_readonly_fields(self, request, obj=None):
		"""
		Verifies if is a update (obj != None) operation to set
		init_balance as readonly
		"""
		if obj:
			return self.readonly_fields + ('init_balance',)
		else:
			return self.readonly_fields

admin.site.register(Account, AccountAdmin)