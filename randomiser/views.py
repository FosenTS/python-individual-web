from django.shortcuts import render
from .models import Domain
from django.db.models import Q

def search_domains_by_name(text):
    domains = Domain.objects.filter(domain_name__icontains=text)
    return domains

def input_view(request):
    query = request.GET.get('q', '')

    results = []
    if query:
        results = search_domains_by_name(query)

    return render(request, 'randomiser/search.html', {'results': results, 'query': query})