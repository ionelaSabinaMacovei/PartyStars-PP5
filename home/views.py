from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.


def index(request):
    """ A view to return the index page """

    template = 'home/index.html'
    return render(request, template)


def contact_page(request):
    """ contact page view"""

    if request.method == 'POST':
        email_host = settings.DEFAULT_FROM_EMAIL
        cust_email = request.POST.get('message-email')
        cust_name = request.POST.get('message-name')
        cust_message = request.POST.get('message')
        message = render_to_string(
            'home/confirmation_emails/confirmation_email_body_admin.txt',
            {
                'cust_email': cust_email,
                'cust_name': cust_name,
                'cust_message': cust_message})
        messages.success(
            request,
            f'Thank you {cust_name}, your email has been sent.
            We will contact you shortly.')
        # Send email to store
        send_mail(
            'ALERT! New customer message from ' + cust_name,  # subject line
            message,  # message
            email_host,  # from email
            [email_host],  # to email
        )

        # Send confirmation email to customer
        message = render_to_string(
            'home/confirmation_emails/confirmation_email_body.txt',
            {
                'cust_email': cust_email,
                'cust_name': cust_name,
                'cust_message': cust_message})
        send_mail(
            'Party Stars Message Received Confirmation!',
            message,  # message
            email_host,
            [cust_email],  # from email
        )
        return redirect(reverse('contact'))
    context = {
        'on_page': True,
    }

    return render(request, 'home/contact.html', context)
