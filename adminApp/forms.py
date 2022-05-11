from django import forms
from django.db.models import fields
from .models import *
from PIL import Image
from django.core.files import File
from django.core.validators import MinValueValidator
import re

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category"]


class SubCategoriesForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control mt-2 mb-2'}), label='')

    class Meta:
        model = SubCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SubCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].widget.attrs['hidden'] = True


class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        exclude = ('date', 'offer',)
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['img1'].widget.attrs['class'] = "image"
        self.fields['brand_id'].label = "brand name"
        self.fields['front_camera'].label = "front camera(px)"
        self.fields['back_camera'].label = "back camera(px)"

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        battery = cleaned_data.get("battery")
        rom = cleaned_data.get("rom")
        front_camera = cleaned_data.get("front_camera")
        back_camera = cleaned_data.get("back_camera")


        if battery != None and  int(battery) > 30000:
            self.add_error('battery', "value must less that 30000") 
    
        if rom != None and  int(rom) > 500:
            self.add_error('rom', "value must less that 500") 

        if rom != None and  int(rom) > 500:
            self.add_error('rom', "value must less that 500") 

        if front_camera != None and  int(front_camera) > 500:
            self.add_error('front_camera', "value must less that 500") 

        if back_camera != None and  int(back_camera) > 500:
            self.add_error('back_camera', "value must less that 500")

        return cleaned_data




class VariantForm(forms.ModelForm):
    class Meta:
        model = VariantAndPrice
        exclude = ("product_id", 'final_price')
    def __init__(self, *args, **kwargs):
        super(VariantForm, self).__init__(*args, **kwargs)
        self.fields['variant'].label = "varaint 1(ram)"
        self.fields['price'].label = "varaint 1(price)"
        self.fields['quantity'].label = "varaint 1(quantity)"

    def clean(self):
        cleaned_data = super(VariantForm, self).clean()
        variant = cleaned_data.get("variant")

        if variant != None and  int(variant) > 1000:
            self.add_error('variant', "value must greater that 1000") 


        return cleaned_data


class VariantForm2(forms.Form):
    nameOfVariant = forms.CharField(label='varaint 2(ram)')
    priceOfVariant = forms.IntegerField(label="varaint 2(price)")
    quantity_2 = forms.IntegerField(label="varaint 2(quantity)" )

    def clean(self):
        cleaned_data = super(VariantForm2, self).clean()
        nameOfVariant = cleaned_data.get("nameOfVariant")
        priceOfVariant = cleaned_data.get("priceOfVariant")
        quantity_2 = cleaned_data.get("quantity_2")


        if str(nameOfVariant).isdigit() == False:
            self.add_error('nameOfVariant', "only numbers are allowded") 
        elif nameOfVariant != None and  int(nameOfVariant) < 1:
            self.add_error('nameOfVariant', "value must greater that 0") 
        elif nameOfVariant != None and  int(nameOfVariant) > 1000:
            self.add_error('nameOfVariant', "value must less that 1000") 

        if priceOfVariant != None and  int(priceOfVariant) < 1:
            self.add_error('priceOfVariant', "value must greater that 0") 
        elif str(priceOfVariant).isdigit() == False:
            self.add_error('priceOfVariant', "only numbers are allowded") 

        if quantity_2 != None and  int(quantity_2) < 1:
            self.add_error('quantity_2', "value must greater that 0") 

        elif str(quantity_2).isdigit() == False:
            self.add_error('quantity_2', "only numbers are allowded") 



        return cleaned_data





class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

class CoupenForm(forms.ModelForm):
    class Meta:
        model = Coupen
        fields = "__all__"

    def clean(self):
        cleaned_data = super(CoupenForm, self).clean()
        coupen_offer = cleaned_data.get("coupen_offer")
        if coupen_offer != None and  coupen_offer < 1:
            self.add_error('coupen_offer', "coupen offer must greater that 0") 
        elif coupen_offer != None and coupen_offer > 90:
            self.add_error('coupen_offer', "coupen offer must less that 90") 
        return cleaned_data

