from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shared.models.base_model import BaseModel


class BaseModelAdmin(ModelAdmin):
    readonly_fields = [
        "id",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change) -> None:  # type: ignore
        if obj.pk is None:
            self._do_on_pre_save(request, obj, form, change)

        obj.save()

    def _do_on_pre_save(self, request, obj, form, change) -> None:  # type: ignore
        if isinstance(obj, BaseModel):
            obj.created_by = request.user
            obj.updated_by = request.user

    def save_formset(self, request, form, formset, change):  # type: ignore
        instances = formset.save(commit=False)
        for instance in instances:
            self._do_on_pre_save(request, instance, form, change)
            instance.save()
        formset.save_m2m()


class BaseTabularInline(admin.TabularInline):
    readonly_fields = [
        "id",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    ordering = ["-created_at"]
    extra = 0
