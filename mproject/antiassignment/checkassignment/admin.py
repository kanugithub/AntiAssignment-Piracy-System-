from django.contrib import admin

# Register your models here.
from checkassignment.models import Student,Assignment,DWMAssignment,CGMAssignment,MLAssignment,TOCAssignment,BIGDATAAssignment

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(DWMAssignment)
admin.site.register(CGMAssignment)
admin.site.register(MLAssignment)
admin.site.register(TOCAssignment)
admin.site.register(BIGDATAAssignment)
