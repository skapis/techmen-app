import json
from datetime import datetime as dt
from .models import Record, ProductionLine, MachineWorks, MachineIssues, Components, Variables, PriceOffer, RecordSum
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from app_settings.models import WorkList, WorkItemDescription
from decimal import Decimal
from django.utils.timezone import make_aware
import xlwt
from PIL import Image
from io import BytesIO
from django.contrib.staticfiles import finders
from .utils import is_valid_uuid


@login_required(login_url='/auth/login')
def index(request):
    product_lines = ProductionLine.objects.all()
    records = Record.objects.filter(user=request.user)

    context = {
        'records': records,
        'lines': product_lines
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='/auth/login')
def add_record(request):
    lines = ProductionLine.objects.all()
    work_list = WorkList.objects.filter(valid=True)
    work_desc = WorkItemDescription.objects.filter(valid=True)

    context = {
        'lines': lines,
        'works': work_list,
        'workDesc': work_desc,
        'workPrice': Variables.objects.get(variableName='workPrice'),
        'transportPrice': Variables.objects.get(variableName='transportPrice'),
        'values': request.POST,
    }

    if request.method == 'GET':
        return render(request, 'records/newRecord.html', context=context)

    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        line_category = ProductionLine.objects.get(lineId=data.get('line'))
        date = data.get('date')
        description = data.get('description')
        internal_id = data.get('internalId')
        distance = data.get('distance')
        transport_price = data.get('transportPrice')
        work_price = data.get('workPrice')
        works_list = data.get('works', [])
        issues_list = data.get('issues', [])
        components_list = data.get('components', [])
        offers_list = data.get('offers', [])

        if name and line_category and date and description and internal_id and distance and transport_price:
            new_record = Record.objects.create(name=name, date=date, lineCategory=line_category, user=request.user,
                                               description=description, internalId=internal_id, distance=distance,
                                               transportPrice=transport_price, workPrice=work_price)

            for item in works_list:
                work_item_desc = WorkItemDescription.objects.get(workItemDescId=item['itemDescription'])
                work_item = WorkList.objects.get(itemId=item['workId'])
                MachineWorks.objects.create(recordId=new_record, workListItemName=work_item.name,
                                            workListItem=work_item, workDone=item['workDone'],
                                            itemDescName=work_item_desc.name, itemDesc=work_item_desc)

            if len(issues_list) != 0:
                for issue in issues_list:
                    MachineIssues.objects.create(recordId=new_record, issueName=issue['issueName'],
                                                 fixed=True, fixTime=issue['fixTime'], resolution=issue['resolution'])
            # TODO: if fixTime is not filled or zero then fixed=False
            if len(components_list) != 0:
                for component in components_list:
                    Components.objects.create(recordId=new_record,
                                              componentSerialNumber=component['componentSerialNumber'],
                                              componentName=component['componentName'],
                                              ordered=component['componentOrdered'],
                                              componentChange=component['componentChange'],
                                              componentPrice=component['componentPrice'])

            if len(offers_list) != 0:
                for offer in offers_list:
                    PriceOffer.objects.create(recordId=new_record, offerDate=offer['offerDate'],
                                              componentSerialNumber=offer['componentSerialNumber'],
                                              workTime=offer['workTime'], componentPrice=offer['offerPrice'])

            messages.success(request, 'Záznam byl vytvořen')
            return redirect('home')

    messages.error(request, 'Něco není v pořádku, zkontrolujte formulář')
    return redirect(add_record, context=context)


@login_required(login_url='/auth/login')
def record_detail(request, record_id):
    if request.method == 'GET':
        record = Record.objects.get(recordId=record_id)
        lines = ProductionLine.objects.all()
        work_desc = WorkItemDescription.objects.all()
        work_done = MachineWorks.objects.filter(recordId=record)
        issues = MachineIssues.objects.filter(recordId=record)
        components = Components.objects.filter(recordId=record)
        offers = PriceOffer.objects.filter(recordId=record)
        record_sum = RecordSum.objects.filter(recordId=record)

        context = {
            'record': record,
            'lines': lines,
            'workDesc': work_desc,
            'workDone': work_done,
            'issues': issues,
            'components': components,
            'offers': offers,
            'recordSum': record_sum
        }

        if record.confirmed:
            messages.info(request, 'Záznam byl již potvrzen, můžete pouze exportovat')

        return render(request, 'records/recordDetail.html', context=context)


@login_required(login_url='/auth/login')
def confirm_record(request, record_id):
    record = Record.objects.get(recordId=record_id)
    components = Components.objects.filter(recordId=record_id)
    issues = MachineIssues.objects.filter(recordId=record_id)

    issues_work = issues.aggregate(work_sum=Sum('fixTime'))['work_sum']
    components_price = components.aggregate(components_price=Sum('componentPrice'))['components_price']
    margin = Decimal(str(1.35))
    components_total = components_price * margin
    transport = record.distance * record.transportPrice
    total_work = issues_work * record.workPrice

    RecordSum.objects.create(recordId=record, workPriceSum=total_work, componentPriceSum=components_total,
                             transportPriceSum=transport, total=(total_work + components_total + transport))

    record.confirmed = True
    record.confirmed_at = make_aware(dt.now())
    record.confirmed_by = f"{request.user.first_name} {request.user.last_name}"
    record.save()

    messages.success(request, 'Záznam byl potvrzen')
    return redirect('record', record_id)


def export_record(request, record_id):
    record = Record.objects.get(recordId=record_id)
    works = MachineWorks.objects.filter(recordId=record_id)
    issues = MachineIssues.objects.filter(recordId=record_id)
    components = Components.objects.filter(recordId=record_id)
    offers = PriceOffer.objects.filter(recordId=record_id)
    record_sum = RecordSum.objects.get(recordId=record_id)

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Record')

    img_path = finders.find('media/techmen_logo.png')
    img = Image.open(img_path)
    desired_width_cm = 9
    desired_height_cm = 1.5

    resized_img = img.resize((int(desired_width_cm * 28.3465), int(desired_height_cm * 28.3465)))

    image_parts = resized_img.split()
    r = image_parts[0]
    g = image_parts[1]
    b = image_parts[2]

    resized_img = Image.merge("RGB", (r, g, b))
    fo = BytesIO()
    resized_img.save(fo, format='bmp')

    # insert techmen logo
    worksheet.insert_bitmap_data(fo.getvalue(), 1, 0)
    worksheet.insert_bitmap_data(fo.getvalue(), 45, 0)
    worksheet.insert_bitmap_data(fo.getvalue(), 86, 0)
    worksheet.insert_bitmap_data(fo.getvalue(), 124, 0)

    company_slogan_rows = [2, 46, 87, 125]
    for slogan_row in company_slogan_rows:
        worksheet.write_merge(slogan_row, slogan_row, 4, 8, 'marking coding automation vision',
                              xlwt.easyxf('font: height 220, name Calibri; align: horiz center'))

    worksheet.col(3).width = 256 * 10
    worksheet.col(4).width = 256 * 17

    worksheet.write_merge(4, 4, 2, 7, f'Záznam o provedení preventivní údržby na lince {record.lineCategory.lineName}',
                          xlwt.easyxf('font: bold 1, height 280, name Calibri; align: horiz center'))

    head_table_dict = {
        "typ stroje": record.lineCategory.lineName,
        "datum výroby": record.lineCategory.lineDate.strftime('%d.%m.%Y'),
        "výrobní číslo": record.lineCategory.lineSerialNumber,
        "provedeno dne": record.date.strftime('%d.%m.%Y'),
        "umístění stroje": record.lineCategory.lineLocation,
        "interní číslo zakázky": record.internalId,
    }

    normal_style_bold = xlwt.easyxf('font: bold 1; borders: left thick, right thin, top thin, bottom thin;')
    normal_val_style = xlwt.easyxf('borders: left thin, right thick, top thin, bottom thin;')
    norm_first = xlwt.easyxf('font: bold 1; borders: left thick, right thin, top thick, bottom thin;')
    norm_last = xlwt.easyxf('font: bold 1; borders: left thick, right thin, top thin, bottom thick;')
    norm_val_first = xlwt.easyxf('borders: left thin, right thick, top thick, bottom thin;')
    norm_val_last = xlwt.easyxf('borders: left thin, right thick, top thin, bottom thick;')

    for row_num, (key, value) in enumerate(head_table_dict.items(), start=7):
        if row_num == 7:
            worksheet.write_merge(row_num, row_num, 0, 1, key, style=norm_first)
            worksheet.write_merge(row_num, row_num, 2, 5, value, style=norm_val_first)
        elif row_num == 12:
            worksheet.write_merge(row_num, row_num, 0, 1, key, style=norm_last)
            worksheet.write_merge(row_num, row_num, 2, 5, value, style=norm_val_last)
        else:
            worksheet.write_merge(row_num, row_num, 0, 1, key, style=normal_style_bold)
            worksheet.write_merge(row_num, row_num, 2, 5, value, style=normal_val_style)

    # works on machine
    worksheet.write_merge(15, 15, 3, 6, 'Provedené práce na stroji',
                          xlwt.easyxf('font: bold 1, height 280, name Calibri; align: horiz center'))

    worksheet.write_merge(18, 19, 0, 4, 'provedené práce',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(18, 18, 5, 6, 'provedeno',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                      'borders: left thick, right thick, top thick, bottom thin;'))

    worksheet.write(19, 5, 'ano',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write(19, 6, 'ne',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write_merge(18, 19, 7, 8, 'záznam',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    for row_num, work in enumerate(works, start=21):
        worksheet.row(row_num).height_mismatch = True
        worksheet.row(row_num).height = 25 * 20
        worksheet.write_merge(row_num, row_num, 0, 4, work.workListItemName,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))
        if work.workDone:
            worksheet.write(row_num, 5, 'x',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center;'))
            worksheet.write(row_num, 6, '',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center;'))
        else:
            worksheet.write(row_num, 5, '',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center;'))
            worksheet.write(row_num, 6, 'x',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center;'))

        worksheet.write_merge(row_num, row_num, 7, 8, work.itemDescName,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

    # issues
    worksheet.write_merge(48, 48, 3, 6, 'Nalezené závady při kontrole stroje',
                          xlwt.easyxf('font: bold 1, height 280, name Calibri; align: horiz center'))

    worksheet.write_merge(50, 51, 0, 4, 'záznam o závadě',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(50, 50, 5, 6, 'oprava',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                      'borders: left thick, right thick, top thick, bottom thin;'))

    worksheet.write(51, 5, 'ano',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write(51, 6, 'čas',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write_merge(50, 51, 7, 8, 'odstranění závady',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    for row_num, issue in enumerate(issues, start=53):
        worksheet.row(row_num).height_mismatch = True
        worksheet.row(row_num).height = 25 * 20

        worksheet.write_merge(row_num, row_num, 0, 4, issue.issueName,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))
        if issue.fixed:
            worksheet.write(row_num, 5, 'x',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center, vert center;'))
        else:
            worksheet.write(row_num, 5, '',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: horiz center, vert center;'))

        worksheet.write(row_num, 6, issue.fixTime,
                        xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                    'font: height 220, name Calibri; align: horiz center, vert center;'))

        worksheet.write_merge(row_num, row_num, 7, 8, issue.resolution,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

    # components
    worksheet.write_merge(89, 89, 3, 6, f'Seznam komponent na výměnu {record.internalId}',
                          xlwt.easyxf('font: bold 1, height 280, name Calibri; align: horiz center'))

    worksheet.write_merge(91, 92, 0, 4, 'poškozený díl ; číslo dílu',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(91, 91, 5, 6, 'objednáno',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                      'borders: left thick, right thick, top thick, bottom thin;'))

    worksheet.write(92, 5, 'ano',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write(92, 6, 'ne',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                'borders: left thick, right thick, top thin, bottom thick;'))

    worksheet.write_merge(91, 92, 7, 8, 'výměna dílu',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    for row_num, component in enumerate(components, start=94):
        worksheet.row(row_num).height_mismatch = True
        worksheet.row(row_num).height = 25 * 20
        worksheet.write_merge(row_num, row_num, 0, 4, f'{component.componentName} ; {component.componentSerialNumber}',
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))
        if component.ordered:
            worksheet.write(row_num, 5, 'x',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: vert center, horiz center;'))
            worksheet.write(row_num, 6, '',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: vert center, horiz center;'))
        else:
            worksheet.write(row_num, 5, '',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: vert center, horiz center;'))
            worksheet.write(row_num, 6, 'x',
                            xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                        'font: height 220, name Calibri; align: vert center, horiz center;'))

        worksheet.write_merge(row_num, row_num, 7, 8, component.componentChange,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

    # price offers
    worksheet.write_merge(127, 127, 3, 6, f'Cenová nabídka {record.internalId}',
                          xlwt.easyxf('font: bold 1, height 280, name Calibri; align: horiz center'))

    worksheet.write(130, 0, 'datum',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(130, 130, 1, 3, 'číslo dílu',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(130, 130, 4, 5, 'čas výměny',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(130, 130, 6, 9, 'cena',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    for row_num, offer in enumerate(offers, start=132):
        worksheet.row(row_num).height_mismatch = True
        worksheet.row(row_num).height = 25 * 20

        worksheet.write(row_num, 0, offer.offerDate.strftime('%d.%m.%Y'),
                        xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                    'font: height 220, name Calibri; align: vert center;'))

        worksheet.write_merge(row_num, row_num, 1, 3, offer.componentSerialNumber,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

        worksheet.write_merge(row_num, row_num, 4, 5, offer.workTime,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

        worksheet.write_merge(row_num, row_num, 6, 9, offer.componentPrice,
                              xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;'
                                          'font: height 220, name Calibri; align: vert center;'))

    # summary
    worksheet.write(151, 0, 'datum',
                    xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'
                                'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(151, 151, 1, 5, 'počet km doprava',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write_merge(151, 151, 6, 9, 'cena dopravného',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center;'
                                      'borders: left thick, right thick, top thick, bottom thick;'))

    worksheet.write(153, 0, '',
                    xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center;'
                                'borders: left thin, right thin, top thin, bottom thin;'))

    worksheet.write_merge(153, 153, 1, 5, record.distance,
                          xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thin, right thin, top thin, bottom thin;'))

    worksheet.write_merge(153, 153, 6, 9, record_sum.transportPriceSum,
                          xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thin, right thin, top thin, bottom thin;',
                                      num_format_str="#,##0.00 Kč"))

    worksheet.write(154, 0, '',
                    xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center;'
                                'borders: left thin, right thin, top thin, bottom thin;'))

    worksheet.write_merge(154, 154, 1, 5, 'cena dopravného bude jedna za předpokladu opravy všech závad na lince ….. '
                                          'v jednom dni.',
                          xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center, wrap on;'
                                      'borders: left thin, right thin, top thin, bottom thin;'))

    worksheet.write_merge(154, 154, 6, 9, '',
                          xlwt.easyxf('font: height 220, name Calibri; align: horiz center, vert center;'
                                      'borders: left thin, right thin, top thin, bottom thin;'))

    worksheet.write_merge(158, 158, 0, 3, f'Celková cena za opravu dle {record.internalId}',
                          xlwt.easyxf('font: bold 1, height 220, name Calibri; align: horiz center, vert center;'))

    worksheet.write_merge(158, 158, 6, 9, record_sum.total,
                          xlwt.easyxf(strg_to_parse='font: bold 1, height 220, name Calibri; align: horiz center, '
                                                    'vert center;',
                                      num_format_str="#,##0.00 Kč"))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={record.internalId}.xls'

    workbook.save(response)

    return response


@login_required(login_url='/auth/login')
def edit_record(request, record_id):
    if request.method == 'POST':
        record = Record.objects.get(recordId=record_id)
        data = json.loads(request.body)

        record.name = data['name']
        record.date = data['date']
        record.lineCategory = ProductionLine.objects.get(lineId=data['line'])
        record.description = data['description']
        record.internalId = data['internalId']
        record.distance = data['distance']
        record.transportPrice = data['transportPrice']
        record.workPrice = data['workPrice']

        record.save()

        works = data['works']
        issues = data['issues']
        components = data['components']
        offers = data['offers']

        for item in works:
            work = MachineWorks.objects.get(workId=item['workId'])
            work_item_desc = WorkItemDescription.objects.get(workItemDescId=item['itemDescription'])
            work_item = WorkList.objects.get(itemId=item['workItemId'])
            work.workDone = item['workDone']
            work.workListItem = work_item
            work.workListItemName = work_item.name
            work.itemDesc = work_item_desc
            work.itemDescName = work_item_desc.name
            work.save()

        if len(issues) != 0:
            for issue_obj in issues:
                if is_valid_uuid(str(issue_obj['issueId'])):
                    issue = MachineIssues.objects.get(issueId=issue_obj['issueId'])
                    issue.issueName = issue_obj['issueName']
                    issue.fixTime = issue_obj['fixTime']
                    issue.resolution = issue_obj['resolution']
                    issue.save()
                else:
                    MachineIssues.objects.create(recordId=record, issueName=issue_obj['issueName'],
                                                 fixed=True, fixTime=issue_obj['fixTime'],
                                                 resolution=issue_obj['resolution'])

        if len(components) != 0:
            for component_obj in components:
                if is_valid_uuid(str(component_obj['componentId'])):
                    component = Components.objects.get(componentId=component_obj['componentId'])
                    component.componentName = component_obj['componentName']
                    component.componentSerialNumber = component_obj['componentSerialNumber']
                    component.componentChange = component_obj['componentChange']
                    component.ordered = component_obj['componentOrdered']
                    component.componentPrice = component_obj['componentPrice']
                    component.save()

                else:
                    Components.objects.create(recordId=record,
                                              componentSerialNumber=component_obj['componentSerialNumber'],
                                              componentName=component_obj['componentName'],
                                              ordered=component_obj['componentOrdered'],
                                              componentChange=component_obj['componentChange'],
                                              componentPrice=component_obj['componentPrice'])

        if len(offers) != 0:
            for offer_obj in offers:
                if is_valid_uuid(str(offer_obj['offerId'])):
                    offer = PriceOffer.objects.get(offerId=offer_obj['offerId'])
                    offer.offerDate = offer_obj['offerDate']
                    offer.componentSerialNumber = offer_obj['componentSerialNumber']
                    offer.workTime = offer_obj['workTime']
                    offer.componentPrice = offer_obj['offerPrice']
                    offer.save()
                else:
                    PriceOffer.objects.create(recordId=record, offerDate=offer_obj['offerDate'],
                                              componentSerialNumber=offer_obj['componentSerialNumber'],
                                              workTime=offer_obj['workTime'], componentPrice=offer_obj['offerPrice'])

        response = {
            'message': 'success'
        }

        messages.success(request, 'Změny byly uloženy')
        return JsonResponse(response, status=200)


@login_required(login_url='/auth/login')
def delete_record(request, record_id):
    record = Record.objects.get(recordId=record_id)
    record.delete()

    messages.success(request, f'Záznam {record.name} byl smazán')
    return redirect('home')


@login_required(login_url='/auth/login')
def production_lines(request):
    if request.method == 'GET':
        lines = ProductionLine.objects.all()

        context = {
            'lines': lines
        }

        return render(request, 'lines/linesIndex.html', context=context)

    if request.method == 'POST':
        data = request.POST
        new_line = ProductionLine.objects.create(
            lineName=data['name'], lineSerialNumber=data['serialNumber'], lineLocation=data['location'],
            lineDate=data['date']
        )

        messages.success(request, f'Nová kategorie linky s názvem {new_line.lineName} byla vytvořena')
        return redirect('lines')


@login_required(login_url='/auth/login')
def line_detail(request, line_id):
    if request.method == 'GET':
        line = ProductionLine.objects.get(lineId=line_id)
        records = Record.objects.filter(lineCategory=line, user=request.user)

        context = {
            'line': line,
            'records': records
        }

        return render(request, 'lines/lineDetail.html', context=context)


@login_required(login_url='/auth/login')
def edit_line(request, line_id):
    if request.method == 'POST':
        line = ProductionLine.objects.get(lineId=line_id)
        data = request.POST

        line.lineName = data['name']
        line.lineSerialNumber = data['serialNumber']
        line.lineLocation = data['location']
        line.lineDate = data['date']
        line.save()

        messages.success(request, 'Linka byla úspěšně změněna')
        return redirect('lines')


@login_required(login_url='/auth/login')
def change_line(request, line_id):
    if request.method == 'GET':
        line = ProductionLine.objects.get(lineId=line_id)
        if line.valid:
            line.valid = False
            line.save()
            messages.error(request, f'Položka {line.lineName} byla deaktivována')
        else:
            line.valid = True
            line.save()
            messages.success(request, f'Položka {line.lineName} byla aktivována')
        return redirect('lines')


@login_required(login_url='/auth/login')
def check_line_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if ProductionLine.objects.filter(lineName=data['name']).exists():
            return JsonResponse({'duplicate_check': 'Linka s tímto názvem již existuje'}, status=409)
        return JsonResponse({'duplicate_check': True})

