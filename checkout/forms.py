

from userApp.models import address
from django import forms


class add_address(forms.ModelForm):
    class Meta:
        model = address
        exclude = ('user_id',)

    def clean(self):
        cleaned_data = super(add_address, self).clean()
        full_name = cleaned_data.get("full_name")
        city = cleaned_data.get("city")
        mobile_number = cleaned_data.get("mobile_number")
        zipcode = cleaned_data.get("zipcode")
        address = cleaned_data.get("address")

        # if mobile_number !=None and mobile_number.isdecimal():
        #     self.add_error('mobile_number', "mobile number should only contain numbers")
        if mobile_number !=None and len(mobile_number) < 10:
            self.add_error('mobile_number', "minmum length is 10") 

        if zipcode !=None and len(zipcode) < 6:
            self.add_error('zipcode', "minmum length is 6") 

        return cleaned_data
