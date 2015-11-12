url(r'^create/barcode/(?P<order_pk>\d+)/$', 'barcode_create', name="staff_barcode"),
url(r'^barcode/$', 'order_status_bar_code', name="staff_order_status_bar_code"),
