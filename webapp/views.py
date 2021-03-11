from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View

from webapp.models import List
from webapp.forms import ListForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = List.objects.all()
        return context


class DetailView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = get_object_or_404(List, id=kwargs.get('id'))
        return context


class IndexRedirectView(View):

    def get(self, request, **kwargs):
        form = ListForm()
        return render(request, 'task_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ListForm(data=request.POST)
        if form.is_valid():
            task = List.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                status=form.cleaned_data.get('status'),
                type=form.cleaned_data.get('type'),
            )
            return redirect('index_view')
        return render(request, 'task_create.html', context={'form': form})


class UpdateView(View):

    def get(self, request, **kwargs):
        task = get_object_or_404(List, id=kwargs.get('id'))
        form = ListForm(initial={
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'type': task.type,
        })
        return render(request, 'task_update.html', context={'form': form, 'list': task})

    def post(self, request, **kwargs):
        task = get_object_or_404(List, id=kwargs.get('id'))
        form = ListForm(data=request.POST)
        if form.is_valid():
            List.name = form.cleaned_data.get("name")
            List.description = form.cleaned_data.get("description")
            List.status = form.cleaned_data.get("status")
            List.type = form.cleaned_data.get("type")
            List.save()
            return redirect('index_view')
        return render(request, 'task_update.html', context={'form': form, 'list': task})


class DeleteView(View):

    def get(self, request, **kwargs):
        task = get_object_or_404(List, id=kwargs.get('id'))
        form = ListForm()
        return render(request, 'task_delete.html', context={'list': task, 'form': form})

    def post(self, request, **kwargs):
        task = get_object_or_404(List, id=kwargs.get('id'))
        form = ListForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['name'] != List.name:
                form.errors['name'] = ['Названия статей не совпадают']
                return render(request, 'task_delete.html', context={'list': task, 'form': form})

            List.delete()
            return redirect('index_view')
        return render(request, 'task_delete.html', context={'list': task, 'form': form})