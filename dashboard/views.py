from django.shortcuts import get_object_or_404, render
from .models import Report, Associate, Refund
from django.utils import timezone
from datetime import timedelta
from dashboard.forms import ReportForm, AssociateForm, RefundForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.db.models import Sum, Avg

@login_required
def mainboard(request):
    processing_reports = Report.objects.filter(completed=False).order_by('-created_date')
    not_completed_total = Report.objects.filter(completed=False).aggregate(Sum('total_amount')).get('total_amount__sum')
    recent_completed_reports = Report.objects.filter(completed=True).filter(completed_date__gte=timezone.now()-timedelta(days=7)).order_by('-created_date')  #최근 일주일간 완료된 목록을 시간 역순으로 전달
    return render(request, 'dashboard/dashboard.html', {'processing_reports':processing_reports, 'recent_completed_reports':recent_completed_reports, 'not_completed_total':not_completed_total})

@login_required
def report_list(request):
    reports = Report.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    associates = Associate.objects.all()
    return render(request, 'dashboard/report_list.html', {'reports_list':reports})

@login_required
def associate_list(request):
    associates = Associate.objects.all().order_by('name')
    return render(request, 'dashboard/associate_list.html', {'associate_list':associates})

@login_required
def report_detail(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render(request, 'dashboard/report_detail.html', {'eachReport':report})

@login_required
def associate_detail(request, associate_id):
    return render(request, 'dashboard/associate_detail.html', {'eachAssociate':Associate.objects.get(pk=associate_id)})

@login_required
def new_report(request):
    if request.method == 'POST':  #폼에서 "save" 버튼을 클릭하면,
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)   # 여기서 report 는 그냥 아무 변수. 어떤 것으로 설정해도 상관없고, redirect  에 넘겨주기 위해서 만든 것임.
            report.last_edited_date = timezone.now()
            report.writer = request.user
            report.save() # 여기서 자료를 저장하면, 기존 불러온 자료에 대한 수정이 아니라, 신규로 저장된다.
            #mail_admins('새 품의서 등록 알림','새 품의서가 등록되었습니다.')
            '''
            send_mail(
                '새 품의서 등록 알림',
                '새 품의서가 등록되었습니다.',
                'emailnotification@pythonanywhere.com',
                ['kpetinter@gmail.com'],
                fail_silently=False,
            )
            '''
            return redirect('dashboard:report_detail', report.pk)
    else:
        form = ReportForm()
    return render(request, 'dashboard/new_report.html', {'form':form}) # 입력 폼을 불러온 페이지에 넘겨준다.

@login_required
def edit_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    if request.method == 'POST':  #폼에서 "save" 버튼을 클릭하면,
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)   # 여기서 report 는 그냥 아무 변수. 어떤 것으로 설정해도 상관없고, redirect  에 넘겨주기 위해서 만든 것임.
            report.last_edited_date = timezone.now()
            report.completed_date = timezone.now()
            report.save()
            return redirect('dashboard:report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'dashboard/edit_report.html', {'form':form})  # 입력 폼을 불러온 페이지에 넘겨준다.

@login_required
def new_associate(request):
    if request.method == 'POST':
        form = AssociateForm(request.POST)
        if form.is_valid():
            associate = form.save(commit=False)
            associate.save()
            return redirect('dashboard:associate_detail', associate.pk)
    else:
        form = AssociateForm()
    return render(request, 'dashboard/new_associate.html', {'form':form})

@login_required
def edit_associate(request, associate_id):
    associate = Associate.objects.get(pk=associate_id)
    if request.method == 'POST':
        form = AssociateForm(request.POST, instance=associate)
        if form.is_valid():
            associate = form.save(commit=False)
            associate.save()
            return redirect('dashboard:associate_list')
    else:
        form = AssociateForm(instance=associate)
    return render(request, 'dashboard/edit_associate.html', {'form':form})

@login_required
def edit_refund(request, refund_id):
    refund = Refund.objects.get(pk=refund_id)
    if request.method == 'POST':
        form = RefundForm(request.POST, instance=refund)
        if form.is_valid():
            refund = form.save(commit=False)
            refund.last_edited_date = timezone.now()
            refund.completed_date = timezone.now()
            refund.save()
            return redirect('dashboard:refund_list')
    else:
        form = RefundForm(instance=refund)
    return render(request, 'dashboard/edit_refund.html', {'form':form})

@login_required
def new_refund(request):
    if request.method == 'POST':  #폼에서 "save" 버튼을 클릭하면,
        form = RefundForm(request.POST)
        if form.is_valid():
            refund = form.save(commit=False)   # 여기서 report 는 그냥 아무 변수. 어떤 것으로 설정해도 상관없고, redirect  에 넘겨주기 위해서 만든 것임.
            refund.last_edited_date = timezone.now()
            refund.completed_date = timezone.now()
            refund.writer = request.user
            refund.save() # 여기서 자료를 저장하면, 기존 불러온 자료에 대한 수정이 아니라, 신규로 저장된다.
            return redirect('dashboard:refund_detail', refund.pk)
    else:
        form = RefundForm()
    return render(request, 'dashboard/new_refund.html', {'form':form}) # 입력 폼을 불러온 페이지에 넘겨준다.


@login_required
def refund_list(request):
    refunds = Refund.objects.all().order_by('-created_date')
    return render(request, 'dashboard/refund_list.html', {'refunds_list':refunds})

@login_required
def refund_detail(request, refund_id):
    refund = Refund.objects.get(pk=refund_id)
    return render(request, 'dashboard/refund_detail.html', {'eachRefund':refund})
