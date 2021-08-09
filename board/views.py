from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from board.models import para


def hello(request, var):
    return HttpResponse('Hello {}'.format(var))

class paraListView(LoginRequiredMixin, TemplateView):
    template_name = 'para_list.html'
    queryset = para.objects.all()
    login_url = settings.LOGIN_URL
    # queryset = None

    def get(self, request, *args, **kwargs):
        #print(request.GET)
        ctx = {
            'paras': self.queryset
        }
        return self.render_to_response(ctx)

    # def get_queryset(self):
    #     if not self.queryset:
    #         self.queryset = para.objects.all()
    #     return self.queryset

class paraDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'para_detail.html'
    queryset = para.objects.all()
    pk_name = 'para_id'
    login_url = settings.LOGIN_URL

    def get_object(self, queryset = None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_name)
        article = queryset.filter(pk=pk).first()
        
        if not article:
            raise Http404('error Detial')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        # if not article:
        #     raise Http404('invalid para_id at Detail')
        ctx = {
            'para': article
        }
        return self.render_to_response(ctx)


class paraCUView(LoginRequiredMixin, TemplateView):
    template_name = 'para_update.html'
    queryset = para.objects.all()
    pk_name = 'para_id'
    success_msg = '저장되었습니다.'
    login_url = settings.LOGIN_URL

    def get_object(self, queryset = None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_name)
        article = queryset.filter(pk=pk).first()

        if pk and not article:
            raise Http404('error CU_get_object')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        # if not article:
        #     raise Http404('error at CU_get')
        ctx = {
            'para': article
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        # if action == '':
        #     messages.error(self.request, 'test?', extra_tags='danger')
        post_data = {key: request.POST.get(key) for key in ('title', 'content', 'author')}
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger')

        if len(messages.get_messages(request)) == 0:
            if action == 'create':
                article = para.objects.create(**post_data)
                # article = para.objects.create(title=title, content=content, author=author)
                messages.success(self.request, self.success_msg)
            elif action == 'update':
                article = self.get_object()
                # if not article:
                #     raise Http404('error CU update')

                for key, value in post_data.items():
                    setattr(article, key, value)
                article.save()
                messages.success(self.request, self.success_msg)
            # elif action == '':
            #     messages.error(self.request, '왜 없니?', extra_tags='danger')
            else:
                #print(action)
                messages.error(self.request, 'POST - 404 Not Found', extra_tags='danger')

            return HttpResponseRedirect('/para/')

        ctx = {
            'para': self.get_object() if action == 'update' else None ,
        }

        return self.render_to_response(ctx)