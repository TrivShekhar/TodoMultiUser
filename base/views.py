from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, base
from django.views.generic.edit import DeleteView, FormView
from base.models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
# Create your views here.
class UserLoginView(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user = True
    def get_success_url(self) -> str:
        return reverse_lazy('tasklist')

class UserRegisterView(FormView):
    template_name = "base/user_register.html"
    form_class = UserCreationForm 
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        if(user is not None):
            login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(UserRegisterView, self).get(*args,**kwargs)

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
        context['search_input']=search_input
        return context
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task" 
    template_name = "base//task.html"

class TaskCreateView(LoginRequiredMixin ,CreateView):
    model = Task 
    fields = ['title','description','completed']
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasklist')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')

