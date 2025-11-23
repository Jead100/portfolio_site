from django.http import FileResponse, Http404
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from .models import Bio, Skill, Project, Resume


class PortfolioView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bio'] = Bio.objects.first()
        context['projects'] = Project.objects.all().order_by('created_at')
        context['resume'] = Resume.objects.filter(is_active=True).first()
        context['skills'] = Skill.objects.filter(pinned=True).order_by('priority', 'name')
        return context


@require_safe
def download_resume(request):
    resume = Resume.objects.filter(is_active=True).first()
    if not resume:
        raise Http404('No active resume.')
    
    resp = FileResponse(
        resume.file.open('rb'),
        as_attachment=True,
        filename="Jordan-Ascanoa-Resume.pdf",
        content_type='application/pdf',
    )

    resp['Cache-Control'] = 'no-cache, must-revalidate'
    return resp
