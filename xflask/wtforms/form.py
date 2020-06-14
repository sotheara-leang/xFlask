from wtforms import Form

from xflask.dto import Dto
from xflask.wtforms import StringField, IntegerField, FieldList, FormField, SelectField


class Form(Form):
    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exclude = kwargs.get('exclude') or []
        self.exclude = exclude

    def get_dto(self):
        return Dto(**self.data)


class SortForm(Form):
    field = StringField()
    order = SelectField(choices=[('asc', ''), ('desc', '')])


class PageForm(Form):
    page = IntegerField(default=1)
    per_page = IntegerField(default=30)
    sort = FieldList(FormField(SortForm), default=[])

    def get_page(self):
        return self.page.data

    def get_per_page(self):
        return self.per_page.data

    def get_sort(self):
        ret_data = []
        for sort in self.sort:
            ret_data.append(Dto(field=sort.field.data, order=sort.order.data))
        return ret_data

    def get_filter(self):
        filter = {}
        for field in self:
            field_name = field.id or field.name

            if field_name not in ['page', 'per_page', 'sort']:
                filter[field_name] = field.data

        return Dto(**filter)

