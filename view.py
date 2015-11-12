###bar code function###
@login_required(login_url='/staff/login/')
@user_passes_test(lambda u: u.is_staff)
def order_status_bar_code(request):
    form = BarCodeForm()
    if request.method == 'POST':
        form = BarCodeForm(data=request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            #split the - than can get the order pk number to change the order status when scan the barcode
            pk, status = code.split("- ")
            order = Order.objects.get(pk=pk)
            if order.delivery_method == "Delivery" and order.status == ORDER_IN_PROGRESS:
                order.status = [8][0]
                order.save()
                messages.success(request, ('The order bar code scan has been successfully change to Attempt Delivery.'), fail_silently=True)
                return redirect('staff_order_status_bar_code')
            elif order.delivery_method == "Self Collect" and order.status == ORDER_IN_PROGRESS:
                order.status = [10][0]
                order.save()
                messages.success(request, ('The order bar code scan has been successfully change to Ready To Pick Up.'), fail_silently=True)
                return redirect('staff_order_status_bar_code')
            else:
                #only when order status is printing in process, the barcode just have function.
                messages.error(request, ('This barcode have some error please contact our admin.'), fail_silently=True)
                return redirect('staff_order_status_bar_code')
    context = {
        'form': form,
    }
    return render_to_response('staff/bar_code_form.html', context, context_instance=RequestContext(request))


@login_required(login_url='/staff/login/')
@user_passes_test(lambda u: u.is_staff)
def barcode_create(request, order_pk):
    #get the order pk
    order = get_object_or_404(Order, pk=order_pk)
    #save the barcode format as code39
    EAN = barcode.get_barcode_class('code39')
    #if order is self collect and printing in process create bar code
    if order.delivery_method == "Self Collect" and order.status == ORDER_IN_PROGRESS:
        ean = EAN(u"%s- rdy-pick-up" % (order.pk))
        barcode_name = (u"%s- rdy-pick-up" % (order.pk))
        fullname = ean.save(u"media/barcode_svg/%s- rdy-pick-up" % (order.pk))
    #if order is delivery and printing in process create bar code
    elif order.delivery_method == "Delivery" and order.status == ORDER_IN_PROGRESS:
        ean = EAN(u"%s- attempt-d" % (order.pk))
        barcode_name = (u"%s- attempt-d" % (order.pk))
        fullname = ean.save(u"media/barcode_svg/%s- attempt-d" % (order.pk))
        # return HttpResponse(ean)
    else:
        #if order status not in printing in process cannot create barcode
        messages.error(request, ('This order status will not generate barcode.'), fail_silently=True)
        print order.get_status_display
        return redirect("%s?fo=1" % reverse('staff_user_order_detail', kwargs={'username': order.user, 'order_pk': order_pk}))

    # return redirect("{{ STATIC_URL }}barcode_svg/{{ barcode_name }}.svg")
    # return HttpResponse(fullname)
    context = {
        'fullname': fullname,
        'barcode_name': barcode_name,
    }
    return render_to_response('staff/bar_code.html', context, context_instance=RequestContext(request))
