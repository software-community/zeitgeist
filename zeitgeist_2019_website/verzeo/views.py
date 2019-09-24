from django.shortcuts import render

# Create your views here.

def verzeo_home(request):
    return render(request, 'verzeo/index.html')


def arts_commerce(request):
    return render(request, 'verzeo/arts&commerce.html')

def advertising(request):
	return render(request, 'verzeo/arts&commerce/advertising.html')

def content(request):
	return render(request, 'verzeo/arts&commerce/content.html')

def digital(request):
	return render(request, 'verzeo/arts&commerce/digital.html')

def journalism(request):
	return render(request, 'verzeo/arts&commerce/journalism.html')

def photo(request):
	return render(request, 'verzeo/arts&commerce/photo.html')

def psychology(request):
	return render(request, 'verzeo/arts&commerce/psychology.html')

def shortfilm(request):
	return render(request, 'verzeo/arts&commerce/shortfilm.html')


def bio(request):
    return render(request, 'verzeo/bio.html')

def nano(request):
    return render(request, 'verzeo/bio/nano.html')


def civil(request):
    return render(request, 'verzeo/civil.html')

def autocad(request):
	return render(request, 'verzeo/civil/autocad.html')

def construction(request):
	return render(request, 'verzeo/civil/construction.html')


def cse(request):
    return render(request, 'verzeo/cse.html')

def ai(request):
	return render(request, 'verzeo/cse/ai.html')

def azure(request):
	return render(request, 'verzeo/cse/azure.html')

def bc(request):
	return render(request, 'verzeo/cse/bc.html')

def ds(request):
	return render(request, 'verzeo/cse/ds.html')

def eh(request):
	return render(request, 'verzeo/cse/eh.html')

def machine(request):
	return render(request, 'verzeo/cse/machine.html')

def web(request):
	return render(request, 'verzeo/cse/web.html')


def ece(request):
    return render(request, 'verzeo/ece.html')

def hybrid(request):
	return render(request, 'verzeo/ece/hybrid.html')

def iot(request):
	return render(request, 'verzeo/ece/iot.html')

def robotics(request):
	return render(request, 'verzeo/ece/robotics.html')


def management(request):
    return render(request, 'verzeo/management.html')

def blockchain(request):
	return render(request, 'verzeo/management/blockchain.html')

def finance_stock(request):
	return render(request, 'verzeo/management/finance&stock.html')

def lean(request):
	return render(request, 'verzeo/management/lean.html')

def marketing(request):
	return render(request, 'verzeo/management/marketing.html')

def hr(request):
	return render(request, 'verzeo/management/hr.html')


def mech(request):
    return render(request, 'verzeo/mech.html')

def autocadmech(request):
	return render(request, 'verzeo/mech/autocadmech.html')

def car(request):
	return render(request, 'verzeo/mech/car.html')

def catia(request):
	return render(request, 'verzeo/mech/catia.html')

def hybridmech(request):
	return render(request, 'verzeo/mech/hybridmech.html')

def icenginee(request):
	return render(request, 'verzeo/mech/icenginee.html')
