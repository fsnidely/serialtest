from django.contrib import admin

from .models import Kind, Materiel, Product, Thing


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    model = Kind
    list_display = ['iden', 'rank', 'name', 'desc']


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    model = Thing
    list_display = ['img_name_html', 'rank', 'kind', 'desc']


class MaterielParentInline(admin.TabularInline):
    model = Materiel
    fk_name = 'parent'
    extra = 0
    verbose_name = 'Product Component'
    verbose_name_plural = 'Product Components'

class MaterielComponentInline(admin.TabularInline):
    model = Materiel
    fk_name = 'component'
    extra = 0
    verbose_name = 'Product Used In'
    verbose_name_plural = 'Product Used In'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (MaterielParentInline, MaterielComponentInline)
    list_display = [
        'thing_img_name_html', 'thing_kind', 'prod_secs', 'low_level']

    def thing_kind(self, product):
        return product.thing.kind

    def thing_img_name_html(self, product):
        return product.thing.img_name_html()
    thing_img_name_html.short_description = 'Thing'


@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    model = Materiel
    list_display = [
        'id',
        'parent_img_name_html', 'component_img_name_html', 'quantity']

    def parent_img_name_html(self, materiel):
        return materiel.parent.thing.img_name_html()
    parent_img_name_html.short_description = 'Parent'

    def component_img_name_html(self, materiel):
        return materiel.component.thing.img_name_html()
    component_img_name_html.short_description = 'Component'
