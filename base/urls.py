from django.urls import path
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from .views_formulario import FormularioTestView

urlpatterns = [
    path('', views.Home.as_view(template_name='base/inicio.html'), name='inicio'),

    #Auntenticacion
    path('login/', auth_view.LoginView.as_view(template_name='base/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'base:login'), name='logout'),
    path('disc/', views.DiscTotal.as_view(template_name='base/disctotal.html'), name='disctotal'),
    path('informedisc/<slug:val>', views.ResultadoDisc.as_view(template_name='base/informedisc.html'), name='informe_disc'),
    path('informediscCare/<slug:val>', views.ViewGraficoCare.as_view(template_name='base/informediscCare.html'), name='grafico_care'),
    path('informediscword/<slug:val>', views.DescargarWord.as_view(), name='informe_dcl'),
    path('informediscpdfalt/<slug:name><slug:val>', views.DescargarPdfAlt.as_view(), name='informepdfalt_dcl'),
    path('enviomail/', views.enviarMail, name='enviomail'),
    path('testdcl/', views.TestDcl.as_view(), name='testdcl'),
    path('testdcl_in/', views.TestDclInterno.as_view(), name='testdcl_in'),
    path('formulario-test/', FormularioTestView.as_view(), name='formulario_test'),
    path('registro-test/', views.RegistroTest.as_view(), name='registro_test'),
    path('test-completos/', views.TestCompletoList.as_view(), name='test_completos_list'),
    path('resultado-test/<slug:val>', views.ResultadoTest.as_view(), name='resultado_test'),
    path('informediscwordbd/<slug:val>', views.DescargarWordDB.as_view(), name='informe_dcl_word'),
    path('datos-personales/', views.DatosPersonalesListView.as_view(), name='datos_personales_list'),
    path('datos-personales/editar/<int:pk>/', views.DatosPersonalesUpdateView.as_view(), name='datos_personales_update'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)