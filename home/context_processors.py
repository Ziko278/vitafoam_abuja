from site_setup.models import SiteSetupModel
from catalog.models import CategoryModel


def layout_variable(request):
    site_info = SiteSetupModel.objects.first()
    category_list = CategoryModel.objects.all()
    return {'site_info': site_info,
            'five_cate_list': category_list[:5],
            'full_cate_list': category_list
        }



