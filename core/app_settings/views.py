from .models import WorkList, WorkItemDescription
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .utils import WORK_LIST_ITEMS, ITEM_DESC_LIST


@login_required(login_url='/auth/login')
def app_settings(request):
    work_list = WorkList.objects.all()
    work_description = WorkItemDescription.objects.exclude(name='Výchozí')

    context = {
        'workList': work_list,
        'workItemDescription': work_description
    }

    return render(request, 'settings/index.html', context=context)


@login_required(login_url='/auth/login')
def add_work_list_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            if WorkList.objects.filter(name=name).exists():
                messages.error(request, 'Položka s tímto názvem již existuje')
                return redirect('settings')
            WorkList.objects.create(name=name)
            messages.success(request, f'Položka {name} byla vytvořena')
            return redirect('settings')
        messages.error(request, 'Něco se nepovedlo, zkuste to znovu')
        return redirect('settings')


def edit_work_list_item(request, item_id):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            work_list_item = WorkList.objects.get(itemId=item_id)
            work_list_item.name = name
            work_list_item.save()
            messages.success(request, f'Položka {name} byla změněna')
            return redirect('settings')
        messages.error(request, 'Něco se nepovedlo, zkuste to znovu')
        return redirect('settings')


@login_required(login_url='/auth/login')
def add_work_item_desc(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            if WorkItemDescription.objects.filter(name=name).exists():
                messages.error(request, 'Položka s tímto názvem již existuje')
                return redirect('settings')

            WorkItemDescription.objects.create(name=name)
            messages.success(request, f'Položka {name} byla vytvořena')
            return redirect('settings')

        messages.error(request, 'Něco se nepovedlo, zkuste to znovu')
        return redirect('settings')


@login_required(login_url='/auth/login')
def edit_work_item_desc(request, item_id):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            item_desc = WorkItemDescription.objects.get(workItemDescId=item_id)
            item_desc.name = name
            item_desc.save()
            messages.success(request, f'Položka {name} byla změněna')
            return redirect('settings')
        messages.error(request, 'Něco se nepovedlo, zkuste to znovu')
        return redirect('settings')


@login_required(login_url='/auth/login')
def change_validity_work_list_item(request, item_id):
    if request.method == 'GET':
        work_list_item = WorkList.objects.get(itemId=item_id)
        if work_list_item.valid:
            work_list_item.valid = False
            work_list_item.save()
            messages.error(request, f'Položka {work_list_item.name} byla deaktivována')
        else:
            work_list_item.valid = True
            work_list_item.save()
            messages.success(request, f'Položka {work_list_item.name} byla aktivována')
        return redirect('settings')


@login_required(login_url='/auth/login')
def change_validity_work_item_desc(request, item_desc_id):
    if request.method == 'GET':
        item_desc = WorkItemDescription.objects.get(workItemDescId=item_desc_id)
        if item_desc.valid:
            item_desc.valid = False
            item_desc.save()
            messages.error(request, f'Položka {item_desc.name} byla deaktivována')
        else:
            item_desc.valid = True
            item_desc.save()
            messages.success(request, f'Položka {item_desc.name} byla aktivována')
        return redirect('settings')


@login_required(login_url='auth/login')
def create_enums(request):
    work_list_count = WorkList.objects.all().count()
    item_desc_count = WorkItemDescription.objects.all().count()

    if work_list_count == 0:
        for work_item in WORK_LIST_ITEMS:
            WorkList.objects.create(name=work_item)

    if item_desc_count == 0:
        for item_desc in ITEM_DESC_LIST:
            WorkItemDescription.objects.create(name=item_desc)

    messages.success(request, 'Hodnoty do číselníků byly úspěšně vloženy')
    return redirect('settings')


