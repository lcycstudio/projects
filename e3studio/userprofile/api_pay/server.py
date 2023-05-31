import os
import uuid
import stripe
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from sgback.models import OrderID, OrderInfo
from sguser.models import ClientUser
from .serializers import PaymentCreateSerializer, PaymentRetrieveSerializer, PaymentReadySerializer, PaymentFinalSerializer
from .serializers import InvoiceStatusListSerializer, InvoiceStatusUpdateSerializer

# This is your real test secret API key.
stripe.api_key = settings.STRIPE_SK

# intent = stripe.PaymentIntent.create(
#     amount=1099,
#     currency='cad',
#     # Verify your integration in this guide by including this parameter
#     metadata={'integration_check': 'accept_a_payment'},
# )

# {
#     amount:,
#     currency: 'usd',
#     customer: customer.id,
#     receipt_email:,
#     description:,
#     shipping: {
#         name:
#         address: {
#             line1: ,
#             line2: ,
#             city: ,
#             province: ,
#             postal_code: ,

#         }
#     }
# }
# {idempotency_key}


class PaymentCheckoutView(GenericAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):

        return Response('hi')

    def post(self, request, format=None):
        data = request.data
        return Response('hi')


# stripe.api_key = "sk_test_51IDwSGIFLOg7DfZ4dnJuqPbJSvWlPfqLhnxv4Jgk69NyLEtGr0xF9EL3fOSWw3XCg3WGTFfnpEJkdPNbrMrFmG5S00Hs10QDZo"


class PaymentCreateView(GenericAPIView):
    serializer_class = InvoiceStatusUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make changes.')
            raise ValidationError({'error': msg})
        else:
            return Response('hi')

    def post(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        # the second module must be 1 to see invoice !
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make a payment.')
            raise ValidationError({'error': msg})
        else:
            current_site = Site.objects.get(id=1)
            data = request.data
            gf_list = list(data['gfront_order_id'].split(","))
            id_list = []
            id_list = OrderID.objects.filter(gfront_order_id__in=gf_list)
            paid = False
            for item in id_list:
                if item.price == item.paid:
                    paid = True
            if paid is True:
                msg = _(
                    'Something went wrong. Please refresh your page and try again.')
                raise ValidationError({'error': msg})
            else:
                try:
                    if cu.company.sub_category == "United States" or cu.company.country == "United States":
                        currency = 'usd'
                    elif cu.company.sub_category == "Canada" or cu.company.country == "Canada":
                        currency = 'cad'
                    create_line_items = []
                    for item in id_list:
                        create_line_items.append({
                            'price_data': {
                                'currency': currency,
                                'unit_amount': int(round(item.price - item.paid, 2) * 100),
                                'product_data': {
                                    'name': item.gfront_order_id,
                                },
                            },
                            'quantity': 1,
                            'description': item.gfront_order_id,
                        })
                    checkout_session = stripe.checkout.Session.create(
                        success_url=current_site.domain + '/clientuser/payment/success',
                        cancel_url=current_site.domain + '/clientuser/payment/cancel',
                        payment_method_types=['card'],
                        line_items=create_line_items,
                        client_reference_id=str(token),
                        customer_email=cu.email,
                        mode='payment',
                    )
                    return Response({'id': checkout_session.id})
                except Exception as e:
                    msg = _(
                        'Something went wrong. Please refresh your page and try again.')
                    raise ValidationError({'error': msg})


class PaymentRetrieveView(GenericAPIView):
    serializer_class = PaymentRetrieveSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make changes.')
            raise ValidationError({'error': msg})
        else:
            return Response('hi')

    def post(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        # the second module must be 1 to see invoice !
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make a payment.')
            raise ValidationError({'error': msg})
        else:
            if cu.stripe_customer_id == "":
                customer = None
            else:
                customer = stripe.Customer.retrieve(cu.stripe_customer_id)

            retrieve_session = stripe.checkout.Session.retrieve(
                request.data['session_id'])
            retrieve_line_items = stripe.checkout.Session.list_line_items(
                request.data['session_id'])
            # prevent double charge
            intent_check = stripe.PaymentIntent.retrieve(
                retrieve_session.payment_intent
            )
            payment_complete = False
            if intent_check.canceled_at is None:
                payment_complete = False
            elif intent_check.cancellation_reason == 'abandoned' and intent_check.status == 'canceled':
                payment_complete = True
            gf_list = []
            for item in retrieve_line_items['data']:
                gf_list.append(item['description'])
            id_list = OrderID.objects.filter(gfront_order_id__in=gf_list)
            info_set = []
            for item in id_list:
                if len(OrderInfo.objects.filter(gfront_order_id=item)) > 0:
                    info_set.append(OrderInfo.objects.filter(
                        gfront_order_id=item)[0])
            serializer = InvoiceStatusListSerializer(info_set, many=True)
            serializer_data = serializer.data
            for item in serializer_data:
                this_id = id_list.get(
                    gfront_order_id=item['gfront_order_id'])
                item['owing'] = this_id.price - this_id.paid
            customer = stripe.Customer.create()
            if token == retrieve_session['client_reference_id'] and cu.email == retrieve_session['customer_email']:
                content = {
                    'session': retrieve_session,
                    'items': serializer_data,
                    'customer': customer,
                    'payment': payment_complete,
                }
                return Response(content)
            else:
                msg = _(
                    'You session has expired. Please refresh the invoice page and make another payment.')
            raise ValidationError({'error': msg})


# PaymentReadySerializer
class PaymentReadyView(GenericAPIView):
    serializer_class = PaymentReadySerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make changes.')
            raise ValidationError({'error': msg})
        else:
            return Response('hi')

    def post(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        # the second module must be 1 to see invoice !
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make a payment.')
            raise ValidationError({'error': msg})
        else:
            data = request.data
            if cu.stripe_customer_id == "":
                # create a customer id and attach it to payment
                customer = stripe.Customer.create(
                    payment_method=data['payment_method'],
                    name='{0} {1}'.format(cu.first_name, cu.last_name) if cu.middle_name == "" else '{0} {1} {2}'.format(
                        cu.first_name, cu.middle_name, cu.last_name),
                    email=cu.email,
                    description=cu.company.account_manager,
                )
            else:
                # stripe_id is the customer_id
                customer = stripe.Customer.retrieve(cu.stripe_customer_id)
            if data['save_card'] is True:
                cu.stripe_customer_id = customer.id
                cu.stripe_payment_id = data['payment_method']
                cu.save()
            else:
                cu.stripe_customer_id = ""
                cu.stripe_payment_id = ""
                cu.save()
            retrieve_session = stripe.checkout.Session.retrieve(
                data['session_id'])
            try:
                payment_method = stripe.PaymentMethod.attach(
                    data['payment_method'],
                    customer=customer.id,
                )
                intent = stripe.PaymentIntent.create(
                    amount=retrieve_session.amount_total,
                    currency=retrieve_session.currency,
                    customer=customer.id,
                    payment_method=payment_method.id,
                    # confirm=True,
                )
                return Response({'intent': intent.id})
            except stripe.error.CardError as e:
                err = e.error
                # Error code will be authentication_required if authentication is needed
                payment_intent_id = err.payment_intent['id']
                payment_intent = stripe.PaymentIntent.retrieve(
                    payment_intent_id)
                msg = _("Code is: %s" % err.code)
                # msg = _(
                #     'You session has expired. Please refresh the invoice page and make another payment.')
                raise ValidationError({'error': msg})


class PaymentFinalView(GenericAPIView):
    serializer_class = PaymentFinalSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make changes.')
            raise ValidationError({'error': msg})
        else:
            return Response('hi')

    def post(self, request, format=None):
        token = request.headers['Authorization'].split('Token ')[1]
        cu = ClientUser.objects.get(
            user_id=Token.objects.get(key=token).user)
        is_mnger = cu.is_mnger
        is_allowed = list(cu.custom.split(','))
        # the second module must be 1 to see invoice !
        if not is_mnger and is_allowed[1] != '1':
            msg = _('You are not authorized to make a payment.')
            raise ValidationError({'error': msg})
        else:
            data = request.data
            # serializer data
            retrieve_session = stripe.checkout.Session.retrieve(
                data['session_id'])
            retrieve_line_items = stripe.checkout.Session.list_line_items(
                data['session_id'])
            gf_list = []
            for item in retrieve_line_items['data']:
                gf_list.append(item['description'])
            id_list = OrderID.objects.filter(gfront_order_id__in=gf_list)
            info_set = []
            for item in id_list:
                if len(OrderInfo.objects.filter(gfront_order_id=item)) > 0:
                    info_set.append(OrderInfo.objects.filter(
                        gfront_order_id=item)[0])
            serializer = InvoiceStatusListSerializer(info_set, many=True)
            serializer_data = serializer.data
            for item in serializer_data:
                this_id = id_list.get(
                    gfront_order_id=item['gfront_order_id'])
                item['owing'] = this_id.price - this_id.paid
            # payment object
            payment = stripe.PaymentMethod.retrieve(data['payment_id'])
            # intent object
            intent = stripe.PaymentIntent.retrieve(data['intent_id'])
            content = {
                'intent': intent,
                'items': serializer_data,
                'payment': payment,
            }
            return Response(content)
            # retrieve_session = stripe.checkout.Session.retrieve(
            #     request.data['session_id'])
            # retrieve_line_items = stripe.checkout.Session.list_line_items(
            #     request.data['session_id'])
            # gf_list = []
            # for item in retrieve_line_items['data']:
            #     gf_list.append(item['description'])
            # id_list = OrderID.objects.filter(gfront_order_id__in=gf_list)
            # info_set = []
            # for item in id_list:
            #     if len(OrderInfo.objects.filter(gfront_order_id=item)) > 0:
            #         info_set.append(OrderInfo.objects.filter(
            #             gfront_order_id=item)[0])
            # serializer = InvoiceStatusListSerializer(info_set, many=True)
            # serializer_data = serializer.data
            # for item in serializer_data:
            #     this_id = id_list.get(
            #         gfront_order_id=item['gfront_order_id'])
            #     item['owing'] = this_id.price - this_id.paid
            # customer = stripe.Customer.create()
            # if token == retrieve_session['client_reference_id'] and cu.email == retrieve_session['customer_email']:
            #     content = {
            #         'session': retrieve_session,
            #         'items': serializer_data
            #     }

            # from flask import Flask, render_template, jsonify, request, send_from_directory
            # from dotenv import load_dotenv, find_dotenv

            # # Setup Stripe python client library.
            # load_dotenv(find_dotenv())

            # # Ensure environment variables are set.
            # price = os.getenv('PRICE')
            # if price is None or price == 'price_12345' or price == '':
            #     print('You must set a Price ID in .env. Please see the README.')
            #     exit(0)

            # stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
            # stripe.api_version = os.getenv('STRIPE_API_VERSION')

            # static_dir = str(os.path.abspath(os.path.join(
            #     __file__, "..", os.getenv("STATIC_DIR"))))
            # app = Flask(__name__, static_folder=static_dir,
            #             static_url_path="", template_folder=static_dir)

            # @app.route('/', methods=['GET'])
            # def get_example():
            #     return render_template('index.html')

            # @app.route('/config', methods=['GET'])
            # def get_publishable_key():
            #     price = stripe.Price.retrieve(os.getenv('PRICE'))
            #     return jsonify({
            #       'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
            #       'unitAmount': price['unit_amount'],
            #       'currency': price['currency']
            #     })

            # # Fetch the Checkout Session to display the JSON result on the success page
            # @app.route('/checkout-session', methods=['GET'])
            # def get_checkout_session():
            #     id = request.args.get('sessionId')
            #     checkout_session = stripe.checkout.Session.retrieve(id)
            #     return jsonify(checkout_session)

            # @app.route('/create-checkout-session', methods=['POST'])
            # def create_checkout_session():
            #     data = json.loads(request.data)
            #     domain_url = os.getenv('DOMAIN')

            #     try:
            #         # Create new Checkout Session for the order
            #         # Other optional params include:
            #         # [billing_address_collection] - to display billing address details on the page
            #         # [customer] - if you have an existing Stripe Customer ID
            #         # [payment_intent_data] - lets capture the payment later
            #         # [customer_email] - lets you prefill the email input in the form
            #         # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            #         # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            #         checkout_session = stripe.checkout.Session.create(
            #             success_url=domain_url +
            #             "/success.html?session_id={CHECKOUT_SESSION_ID}",
            #             cancel_url=domain_url + "/canceled.html",
            #             payment_method_types= os.getenv("PAYMENT_METHOD_TYPES").split(','),
            #             mode="payment",
            #             line_items=[
            #                 {
            #                     "price": os.getenv('PRICE'),
            #                     "quantity": data['quantity']
            #                 }
            #             ]
            #         )
            #         return jsonify({'sessionId': checkout_session['id']})
            #     except Exception as e:
            #         return jsonify(error=str(e)), 403

            # @app.route('/webhook', methods=['POST'])
            # def webhook_received():
            #     # You can use webhooks to receive information about asynchronous payment events.
            #     # For more about our webhook events check out https://stripe.com/docs/webhooks.
            #     webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            #     request_data = json.loads(request.data)

            #     if webhook_secret:
            #         # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            #         signature = request.headers.get('stripe-signature')
            #         try:
            #             event = stripe.Webhook.construct_event(
            #                 payload=request.data, sig_header=signature, secret=webhook_secret)
            #             data = event['data']
            #         except Exception as e:
            #             return e
            #         # Get the type of webhook event sent - used to check the status of PaymentIntents.
            #         event_type = event['type']
            #     else:
            #         data = request_data['data']
            #         event_type = request_data['type']
            #     data_object = data['object']

            #     print('event ' + event_type)

            #     if event_type == 'checkout.session.completed':
            #         print('🔔 Payment succeeded!')

            #     return jsonify({'status': 'success'})

            # if __name__ == '__main__':
            #     app.run(port=4242, debug=True)
