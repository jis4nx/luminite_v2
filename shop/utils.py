from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import uuid
from weasyprint import HTML


def gen_pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html_content = template.render(context_dict)
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    return response
