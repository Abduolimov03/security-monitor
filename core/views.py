import socket
import ssl
import datetime
from django.shortcuts import render, redirect
from .models import DomainRecord
from .forms import DomainForm

def check_ssl_expiry(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expire_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expire_date - datetime.datetime.utcnow()).days
                return expire_date, days_left
    except:
        return None, None

def check_open_ports(domain, ports=[80, 443, 22, 21, 25]):
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((domain, port), timeout=2):
                open_ports.append(port)
        except:
            continue
    return open_ports

def calculate_security_score(open_ports, ssl_days_left):
    score = 100
    if 22 in open_ports or 21 in open_ports:  # less secure ports
        score -= 20
    if ssl_days_left is not None:
        if ssl_days_left < 30:
            score -= 30
    else:
        score -= 50
    return max(score, 0)

def monitoring_page(request):
    domain = request.GET.get('domain', 'example.com')  # default domain
    ssl_expiry, days_left = check_ssl_expiry(domain)
    open_ports = check_open_ports(domain)
    score = calculate_security_score(open_ports, days_left)

    return render(request, 'core/monitoring.html', {
        'domain': domain,
        'ssl_expiry': ssl_expiry,
        'days_left': days_left,
        'open_ports': open_ports,
        'score': score,
    })

def add_domain(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('domain_list')
    else:
        form = DomainForm()
    return render(request, 'core/add_domain.html', {'form': form})

def domain_list(request):
    records = DomainRecord.objects.all()
    return render(request, 'core/domain_list.html', {'records': records})
