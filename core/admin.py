from django.contrib import admin

# Register your models here.
from .models import (
    CakeDepartment,
    CakeShopDetails,
    UserCakeShopRelationship,
    Cakes,
    Flavors,
    OrderCake,
    UserOccasion,
    FlavourRoot,
    OrderProcessing
)


admin.site.register(CakeDepartment)
admin.site.register(CakeShopDetails)
admin.site.register(UserOccasion)
admin.site.register(OrderCake)
admin.site.register(Flavors)
admin.site.register(Cakes)
admin.site.register(UserCakeShopRelationship)
admin.site.register(FlavourRoot)
admin.site.register(OrderProcessing)