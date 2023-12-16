from django.contrib import admin
from .models import (Game,Player,Turn,Card)
# Register your models here.


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Turn)
admin.site.register(Card)