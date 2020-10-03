from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    flavour = None
    if 'product_flavour' in request.POST:
        flavour = request.POST['product_flavour']
    bag = request.session.get('bag', {})

    if flavour:
        if item_id in list(bag.keys()):
            if flavour in bag[item_id]['items_by_flavour'].keys():
                bag[item_id]['items_by_flavour'][flavour] += quantity
                messages.success(request, f'Updated flavour {flavour.upper()} {product.name} quantity to {bag[item_id]["items_by_flavour"][flavour]}')
            else:
                bag[item_id]['items_by_flavour'][flavour] = quantity
                messages.success(request, f'Added flavour {flavour.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_flavour': {flavour: quantity}}
            messages.success(request, f'Added flavour {flavour.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adujusts the quantity of the specified products in the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    flavour = None
    if 'product_flavour' in request.POST:
        flavour = request.POST['product_flavour']
    bag = request.session.get('bag', {})

    if flavour:
        if quantity > 0:
            bag[item_id]['items_by_flavour'][flavour] = quantity
            messages.success(request, f'Updated flavour {flavour.upper()} {product.name} quantity to {bag[item_id]["items_by_flavour"][flavour]}')
        else:
            del bag[item_id]['items_by_flavour'][flavour]
            if not bag[item_id]['items_by_flavour']:
                bag.pop(item_id)
            messages.success(request, f'Removed flavour {flavour.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Removes the item from the shopping cart """

    try:
        product = get_object_or_404(Product, pk=item_id)
        flavour = None
        if 'product_flavour' in request.POST:
            flavour = request.POST['product_flavour']
        bag = request.session.get('bag', {})


        if flavour:

            del bag[item_id]['items_by_flavour'][flavour]
            if not bag[item_id]['items_by_flavour']:
                bag.pop(item_id)
            messages.success(request, f'Removed flavour {flavour.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)