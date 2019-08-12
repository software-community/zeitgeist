from django.contrib import admin
from .models import *

# Register your models here.

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in SubCategory._meta.get_fields()]

# class EventAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Event._meta.get_fields()]

# class ParticipantAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Participant._meta.get_fields()]

# class ParticipantHasPaidAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ParticipantHasPaid._meta.get_fields()]

# class ParticipantHasParticipatedAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ParticipantHasParticipated._meta.get_fields()]

# class TeamAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Team._meta.get_fields()]

# class TeamHasMemberAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in TeamHasMember._meta.get_fields()]

# admin.site.register(SubCategory, SubCategoryAdmin)
# admin.site.register(Event, EventAdmin)
# admin.site.register(Participant, ParticipantAdmin)
# admin.site.register(ParticipantHasPaid, ParticipantHasPaidAdmin)
# admin.site.register(ParticipantHasParticipated, ParticipantHasParticipatedAdmin)
# admin.site.register(Team, TeamAdmin)
# admin.site.register(TeamHasMember, TeamHasMemberAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(ParticipantHasPaid)
admin.site.register(ParticipantHasParticipated)
admin.site.register(Team)
admin.site.register(TeamHasMember)
