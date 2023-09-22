from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import (
	User,
	Event,
 PeopleGroup,
 Comment,
 CommentImages, 
 InterestedEvent
)


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm

	model = User

	list_display = ('name', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login',)
	list_filter = ('is_active', 'is_staff', 'is_superuser')

	fieldsets = (
		(None, {'fields' : ('name', 'email', 'password', 'avatar')}),
		('Permissions', {'fields' : ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')})
		# ('Dates', {'fields' : ('last_login', 'date_joined')})
	)
	add_fieldsets = (
		(None,{

			'classes' : ('wide',),
			'fields' : ('name', 'email', 'password1', 'password2', 'is_staff', 'is_active')
		}

		),
	)

	ordering = ('email',)

class CommentImageInline(admin.TabularInline):
    model = CommentImages
    
class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentImageInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(PeopleGroup)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentImages)
admin.site.register(InterestedEvent)
