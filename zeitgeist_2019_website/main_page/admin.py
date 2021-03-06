from django.contrib import admin
from .models import *

# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Category._meta.get_fields()]

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in SubCategory._meta.get_fields()]

# class EventAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Event._meta.get_fields()]


class Our_SponsorAdmin(admin.ModelAdmin):

    list_display = ['name_of_photo_in_static_files', 'link_to_sponsor']


class Prev_SponsorAdmin(admin.ModelAdmin):

    list_display = ['name_of_photo_in_static_files', 'link_to_sponsor']


class AccomodationAdmin(admin.ModelAdmin):

    list_per_page = 1000

    list_display = ['id', 'get_participant_participant_code', 'get_participant_name', 'get_participant_participating_user_email', 'get_participant_college_name', 'get_participant_contact_mobile_number', 'get_participant_whatsapp_mobile_number', 'gender', 'acco_for_day_one', 'acco_for_day_two', 'acco_for_day_three', 'include_meals', 'transaction_id', 'payment_request_id']

    def get_participant_participant_code(self, obj):
        return obj.participant.participant_code

    get_participant_participant_code.short_description = 'Participant Code'
    get_participant_participant_code.admin_order_field = 'participant__participant_code'

    def get_participant_name(self, obj):
        return obj.participant.name

    get_participant_name.short_description = 'Participant Name'
    get_participant_name.admin_order_field = 'participant__name'

    def get_participant_participating_user_email(self, obj):
        return obj.participant.participating_user.email

    get_participant_participating_user_email.short_description = 'Participant Email'
    get_participant_participating_user_email.admin_order_field = 'participant__participating_user__email'

    def get_participant_college_name(self, obj):
        return obj.participant.college_name

    get_participant_college_name.short_description = 'Participant College Name'
    get_participant_college_name.admin_order_field = 'participant__college_name'

    def get_participant_contact_mobile_number(self, obj):
        return obj.participant.contact_mobile_number

    get_participant_contact_mobile_number.short_description = 'Participant Contact Mobile Number'
    get_participant_contact_mobile_number.admin_order_field = 'participant__contact_mobile_number'

    def get_participant_whatsapp_mobile_number(self, obj):
        return obj.participant.whatsapp_mobile_number

    get_participant_whatsapp_mobile_number.short_description = 'Participant WhatsApp Mobile Number'
    get_participant_whatsapp_mobile_number.admin_order_field = 'participant__whatsapp_mobile_number'


class ParticipantAdmin(admin.ModelAdmin):

    list_per_page = 3000

    list_display = ['get_participating_user_id', 'participant_code', 'name', 'get_participating_user_email',
                    'college_name', 'contact_mobile_number', 'whatsapp_mobile_number', 'referring_ca']

    def get_participating_user_id(self, obj):
        return obj.participating_user.id

    get_participating_user_id.short_description = 'ID'
    get_participating_user_id.admin_order_field = 'participating_user__id'

    def get_participating_user_email(self, obj):
        return obj.participating_user.email

    get_participating_user_email.short_description = 'Participant Email'
    get_participating_user_email.admin_order_field = 'participating_user__email'


class ParticipantHasPaidAdmin(admin.ModelAdmin):

    list_per_page = 1000

    list_display = ['id', 'paid_subcategory', 'transaction_id',
                    'payment_request_id', 'get_participant_code', 'get_participant_name', 'get_participant_participating_user_email', 'get_participant_contact_mobile_number', 'get_participant_whatsapp_mobile_number', 'get_participant_college_name']

    def get_participant_code(self, obj):
        return obj.participant.participant_code

    get_participant_code.short_description = 'Participant Code'
    get_participant_code.admin_order_field = 'participant__participant_code'

    def get_participant_name(self, obj):
        return obj.participant.name

    get_participant_name.short_description = 'Participant Name'
    get_participant_name.admin_order_field = 'participant__name'

    def get_participant_participating_user_email(self, obj):
        return obj.participant.participating_user.email

    get_participant_participating_user_email.short_description = 'Participant Email'
    get_participant_participating_user_email.admin_order_field = 'participant__participating_user__email'

    def get_participant_contact_mobile_number(self, obj):
        return obj.participant.contact_mobile_number

    get_participant_contact_mobile_number.short_description = 'Contact Mobile Number'
    get_participant_contact_mobile_number.admin_order_field = 'participant__contact_mobile_number'

    def get_participant_whatsapp_mobile_number(self, obj):
        return obj.participant.whatsapp_mobile_number

    get_participant_whatsapp_mobile_number.short_description = 'WhatsApp Mobile Number'
    get_participant_whatsapp_mobile_number.admin_order_field = 'participant__whatsapp_mobile_number'

    def get_participant_college_name(self, obj):
        return obj.participant.college_name

    get_participant_college_name.short_description = 'Participant College'
    get_participant_college_name.admin_order_field = 'participant__college_name'


class ParticipantHasParticipatedAdmin(admin.ModelAdmin):

    list_per_page = 1000

    list_display = ['id', 'event', 'get_participant_code', 'get_participant_name', 'get_participant_participating_user_email',
                    'get_participant_contact_mobile_number', 'get_participant_whatsapp_mobile_number', 'get_participant_college_name']

    def get_participant_code(self, obj):
        return obj.participant.participant_code

    get_participant_code.short_description = 'Participant Code'
    get_participant_code.admin_order_field = 'participant__participant_code'


    def get_participant_name(self, obj):
        return obj.participant.name

    get_participant_name.short_description = 'Participant Name'
    get_participant_name.admin_order_field = 'participant__name'

    def get_participant_participating_user_email(self, obj):
        return obj.participant.participating_user.email

    get_participant_participating_user_email.short_description = 'Participant Email'
    get_participant_participating_user_email.admin_order_field = 'participant__participating_user__email'

    def get_participant_contact_mobile_number(self, obj):
        return obj.participant.contact_mobile_number

    get_participant_contact_mobile_number.short_description = 'Contact Mobile Number'
    get_participant_contact_mobile_number.admin_order_field = 'participant__contact_mobile_number'

    def get_participant_whatsapp_mobile_number(self, obj):
        return obj.participant.whatsapp_mobile_number

    get_participant_whatsapp_mobile_number.short_description = 'WhatsApp Mobile Number'
    get_participant_whatsapp_mobile_number.admin_order_field = 'participant__whatsapp_mobile_number'

    def get_participant_college_name(self, obj):
        return obj.participant.college_name

    get_participant_college_name.short_description = 'Participant College'
    get_participant_college_name.admin_order_field = 'participant__college_name'


class TeamAdmin(admin.ModelAdmin):

    list_per_page = 1000

    list_display = ['id', 'name', 'team_code', 'event', 'get_captain_participant_code', 'get_captain_name', 'get_captain_participating_user_email',
                    'get_captain_college_name', 'get_captain_contact_mobile_number', 'get_captain_whatsapp_mobile_number']

    def get_captain_participant_code(self, obj):
        return obj.captain.participant_code

    get_captain_participant_code.short_description = 'Captain Participant Code'
    get_captain_participant_code.admin_order_field = 'captain__participant_code'

    def get_captain_name(self, obj):
        return obj.captain.name

    get_captain_name.short_description = 'Captain Name'
    get_captain_name.admin_order_field = 'captain__name'

    def get_captain_participating_user_email(self, obj):
        return obj.captain.participating_user.email

    get_captain_participating_user_email.short_description = 'Captain Email'
    get_captain_participating_user_email.admin_order_field = 'captain__participating_user__email'

    def get_captain_college_name(self, obj):
        return obj.captain.college_name

    get_captain_college_name.short_description = 'Captain College'
    get_captain_college_name.admin_order_field = 'captain__college_name'

    def get_captain_contact_mobile_number(self, obj):
        return obj.captain.contact_mobile_number

    get_captain_contact_mobile_number.short_description = 'Captain Contact Mobile Number'
    get_captain_contact_mobile_number.admin_order_field = 'captain__contact_mobile_number'

    def get_captain_whatsapp_mobile_number(self, obj):
        return obj.captain.whatsapp_mobile_number

    get_captain_whatsapp_mobile_number.short_description = 'Captain WhatsApp Mobile Number'
    get_captain_whatsapp_mobile_number.admin_order_field = 'captain__whatsapp_mobile_number'


class TeamHasMemberAdmin(admin.ModelAdmin):

    list_per_page = 1000

    list_display = ['id', 'get_member_participant_code', 'get_member_name', 'get_member_college_name', 'get_member_contact_mobile_number', 'get_member_whatsapp_mobile_number', 'get_member_participating_user_email', 'get_team_team_code', 'get_team_name',
                    'get_team_event', 'get_team_captain_participant_code', 'get_team_captain_name', 'get_team_captain_college_name', 'get_team_captain_contact_mobile_number', 'get_team_captain_whatsapp_mobile_number', 'get_team_captain_participating_user_email']

    def get_member_participant_code(self, obj):
        return obj.member.participant_code

    get_member_participant_code.short_description = 'Member Participant Code'
    get_member_participant_code.admin_order_field = 'member__participant_code'

    def get_member_name(self, obj):
        return obj.member.name

    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__name'

    def get_member_college_name(self, obj):
        return obj.member.college_name

    get_member_college_name.short_description = 'Member College Name'
    get_member_college_name.admin_order_field = 'member__college_name'

    def get_member_contact_mobile_number(self, obj):
        return obj.member.contact_mobile_number

    get_member_contact_mobile_number.short_description = 'Member Contact Mobile Number'
    get_member_contact_mobile_number.admin_order_field = 'member__contact_mobile_number'

    def get_member_whatsapp_mobile_number(self, obj):
        return obj.member.whatsapp_mobile_number

    get_member_whatsapp_mobile_number.short_description = 'Member WhatsApp Mobile Number'
    get_member_whatsapp_mobile_number.admin_order_field = 'member__whatsapp_mobile_number'

    def get_member_participating_user_email(self, obj):
        return obj.member.participating_user.email

    get_member_participating_user_email.short_description = 'Member Email'
    get_member_participating_user_email.admin_order_field = 'member__participating_user__email'

    def get_team_team_code(self, obj):
        return obj.team.team_code

    get_team_team_code.short_description = 'Team Code'
    get_team_team_code.admin_order_field = 'team__team_code'

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = 'Team Name'
    get_team_name.admin_order_field = 'team__name'

    def get_team_event(self, obj):
        return obj.team.event

    get_team_event.short_description = 'Event'
    get_team_event.admin_order_field = 'team__event'

    def get_team_captain_participant_code(self, obj):
        return obj.team.captain.participant_code

    get_team_captain_participant_code.short_description = 'Team Captain Participant Code'
    get_team_captain_participant_code.admin_order_field = 'team__captain__participant_code'

    def get_team_captain_name(self, obj):
        return obj.team.captain.name

    get_team_captain_name.short_description = 'Team Captain Name'
    get_team_captain_name.admin_order_field = 'team__captain__name'

    def get_team_captain_college_name(self, obj):
        return obj.team.captain.college_name

    get_team_captain_college_name.short_description = 'Team Captain College Name'
    get_team_captain_college_name.admin_order_field = 'team__captain__college_name'

    def get_team_captain_contact_mobile_number(self, obj):
        return obj.team.captain.contact_mobile_number

    get_team_captain_contact_mobile_number.short_description = 'Team Captain Contact Mobile Number'
    get_team_captain_contact_mobile_number.admin_order_field = 'team__captain__contact_mobile_number'

    def get_team_captain_whatsapp_mobile_number(self, obj):
        return obj.team.captain.whatsapp_mobile_number

    get_team_captain_whatsapp_mobile_number.short_description = 'Team Captain WhatsApp Mobile Number'
    get_team_captain_whatsapp_mobile_number.admin_order_field = 'team__captain__whatsapp_mobile_number'

    def get_team_captain_participating_user_email(self, obj):
        return obj.team.captain.participating_user.email

    get_team_captain_participating_user_email.short_description = 'Team Captain Email'
    get_team_captain_participating_user_email.admin_order_field = 'team__captain__participating_user__email'


# class SupportAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Category._meta.get_fields()]

class NotificationAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Notification._meta.get_fields()]


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)
# admin.site.register(Event, EventAdmin)
admin.site.register(Our_Sponsor, Our_SponsorAdmin)
admin.site.register(Prev_Sponsor, Prev_SponsorAdmin)
admin.site.register(Accomodation, AccomodationAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ParticipantHasPaid, ParticipantHasPaidAdmin)
admin.site.register(ParticipantHasParticipated, ParticipantHasParticipatedAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamHasMember, TeamHasMemberAdmin)
# admin.site.register(Support, SupportAdmin)
admin.site.register(Notification, NotificationAdmin)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Event)
# admin.site.register(Our_Sponsor)
# admin.site.register(Prev_Sponsor)
# admin.site.register(Accomodation)
# admin.site.register(Participant)
# admin.site.register(ParticipantHasPaid)
# admin.site.register(ParticipantHasParticipated)
# admin.site.register(Team)
# admin.site.register(TeamHasMember)
admin.site.register(Support)
# admin.site.register(Notification)
