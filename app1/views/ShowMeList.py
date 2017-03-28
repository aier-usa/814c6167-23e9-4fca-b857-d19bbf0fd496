from django.views.generic.list import ListView
from app1.models import Password


# for ShowMeList, NEVER use LoginRequiredMixin because
# login is NOT required at all.
class ShowMeList(ListView):
    model = Password
    template_name = "app1/show_me_list.html"
    fields = ['id', 'website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']

    def get_queryset(self):
        name_ap = self.kwargs['nameAP']
        print('nameAP is: ' + name_ap)
        temp_variable= Password.objects.filter(
            access_points__name__iexact=name_ap)

        return temp_variable
