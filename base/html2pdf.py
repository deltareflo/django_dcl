from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')