from django.contrib import admin

from .models import Course, Lesson, Payment

admin.site.register(Course)
admin.site.register(Lesson)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'course__name', 'stripe_session_id')
    readonly_fields = ('created_at', 'updated_at')

