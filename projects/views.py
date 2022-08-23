from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    user_agent = request.META['HTTP_USER_AGENT']
    keywords = ['Mobile','Opera Mini','Android']

    if any(word in user_agent for word in keywords):
        device = "Mobile"
    else:
        device = "Desktop"
    context = {'projects':projects,'user_device': user_agent,'device':device}
    
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    print('projectObj;',projectObj)
    return render(request, 'projects/single-projects.html', {'project':projectObj})


def createProject(request):
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {'form':form}
    return render(request, "projects/project_form.html", context)


def updateProject(request, pk):
    project = Project.objects.get(id = pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {'form':form}
    return render(request, "projects/project_form.html", context)


def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, "projects/delete_template.html", context)