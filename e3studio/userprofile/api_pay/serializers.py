from rest_framework import serializers
from sguser.models import ChargeAccount, ClientUser, SGStaff, SGTool
from django.utils.translation import ugettext_lazy as _


class SGToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGTool
        fields = '__all__'


class SGStaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGStaff
        fields = '__all__'


class ChargeAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeAccount
        fields = ('id', 'charge_account')


class ChargeAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeAccount
        fields = '__all__'


class ClientUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = '__all__'


class ClientUserUpdateSerializer(serializers.ModelSerializer):
    cu_id = serializers.CharField(max_length=None)
    first_name = serializers.CharField(max_length=None)
    middle_name = serializers.CharField(max_length=None)
    last_name = serializers.CharField(max_length=None)
    email = serializers.CharField(max_length=None)
    company = serializers.CharField(max_length=None)
    password = serializers.CharField(
        max_length=None, style={'input_type': 'password'})
    is_mnger = serializers.BooleanField()
    custom = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.cu_id = validated_data.get(
            'cu_id', instance.cu_id)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.company = validated_data.get(
            'company', instance.company)
        instance.password = validated_data.get(
            'password', instance.password)
        instance.is_mnger = validated_data.get(
            'is_mnger', instance.is_mnger)
        instance.custom = validated_data.get(
            'custom', instance.custom)
        instance.save()
        return instance


class ClientUserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=None)
    middle_name = serializers.CharField(max_length=None)
    last_name = serializers.CharField(max_length=None)
    email = serializers.CharField(max_length=None)
    company_id = serializers.CharField(max_length=None)
    password = serializers.CharField(
        max_length=None, style={'input_type': 'password'})
    is_mnger = serializers.BooleanField()
    custom = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.company_id = validated_data.get(
            'company_id', instance.company_id)
        instance.password = validated_data.get(
            'password', instance.password)
        instance.is_mnger = validated_data.get(
            'is_mnger', instance.is_mnger)
        instance.custom = validated_data.get(
            'custom', instance.custom)
        instance.save()
        return instance


class SSUpdateSerializer(serializers.Serializer):
    ca_id = serializers.CharField(max_length=None)
    ca_input = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.ca_id = validated_data.get(
            'ca_id', instance.ca_id)
        instance.ca_input = validated_data.get(
            'ca_input', instance.ca_input)
        instance.save()
        return instance


class ClientUserRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=None)
    company = serializers.CharField(max_length=None)
    email = serializers.EmailField(max_length=None)
    phone = serializers.CharField(max_length=None)
    message = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.company = validated_data.get(
            'company', instance.company)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.phone = validated_data.get(
            'phone', instance.phone)
        instance.message = validated_data.get(
            'message', instance.message)
        instance.save()
        return instance


class ClientUserSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=None)
    last_name = serializers.CharField(max_length=None)
    company = serializers.CharField(max_length=None)
    role = serializers.CharField(max_length=None)
    email = serializers.EmailField(max_length=None)
    phone = serializers.CharField(max_length=None)
    address1 = serializers.CharField(max_length=None)
    address2 = serializers.CharField(max_length=None)
    city = serializers.CharField(max_length=None)
    province = serializers.CharField(max_length=None)
    postal = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.company = validated_data.get(
            'company', instance.company)
        instance.role = validated_data.get(
            'role', instance.role)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.phone = validated_data.get(
            'phone', instance.phone)
        instance.address1 = validated_data.get(
            'address1', instance.address1)
        instance.address2 = validated_data.get(
            'address2', instance.address2)
        instance.city = validated_data.get(
            'city', instance.city)
        instance.province = validated_data.get(
            'province', instance.province)
        instance.postal = validated_data.get(
            'postal', instance.postal)
        instance.save()
        return instance


class CorpoSubmitListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=None)
    street = serializers.CharField(max_length=None)
    city = serializers.CharField(max_length=None)
    province = serializers.CharField(max_length=None)
    postal = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.street = validated_data.get(
            'street', instance.street)
        instance.city = validated_data.get(
            'city', instance.city)
        instance.province = validated_data.get(
            'province', instance.province)
        instance.postal = validated_data.get(
            'postal', instance.postal)
        instance.save()
        return instance


class CorpoSubmitUpdateSerializer(serializers.Serializer):
    charge = serializers.CharField(max_length=None)
    street = serializers.CharField(max_length=None)
    city = serializers.CharField(max_length=None)
    province = serializers.CharField(max_length=None)
    postal = serializers.CharField(max_length=None)
    names = serializers.CharField(max_length=None)
    emails = serializers.CharField(max_length=None)

    def update(self, instance, validated_data):
        instance.charge = validated_data.get(
            'charge', instance.charge)
        instance.street = validated_data.get(
            'street', instance.street)
        instance.city = validated_data.get(
            'city', instance.city)
        instance.province = validated_data.get(
            'province', instance.province)
        instance.postal = validated_data.get(
            'postal', instance.postal)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.save()
        return instance


class OrderStatusFilterSerializer(serializers.Serializer):
    # number = serializers.CharField(max_length=None, required=False)
    name = serializers.CharField(max_length=None, required=False)
    year = serializers.CharField(max_length=None, required=False)
    month = serializers.CharField(max_length=None, required=False)

    # charge_account = serializers.CharField(max_length=None, required=False)
    # priority = serializers.CharField(max_length=None, required=False)
    # order_status = serializers.CharField(max_length=None, required=False)
    # order_type = serializers.CharField(max_length=None, required=False)
    # status = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        # instance.number = validated_data.get(
        #     'number', instance.number)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.year = validated_data.get(
            'year', instance.year)
        instance.month = validated_data.get(
            'month', instance.month)
        instance.save()
        return instance


class OrderStatusListSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=None, required=False)
    middle_name = serializers.CharField(max_length=None, required=False)
    last_name = serializers.CharField(max_length=None, required=False)
    received_date = serializers.CharField(max_length=None, required=False)
    kit_number = serializers.CharField(max_length=None, required=False)
    order_type = serializers.CharField(max_length=None, required=False)
    status = serializers.CharField(max_length=None, required=False)
    tracking_number = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.received_date = validated_data.get(
            'received_date', instance.received_date)
        instance.kit_number = validated_data.get(
            'kit_number', instance.kit_number)
        instance.order_type = validated_data.get(
            'order_type', instance.order_type)
        instance.status = validated_data.get(
            'status', instance.status)
        instance.tracking_number = validated_data.get(
            'tracking_number', instance.tracking_number)
        instance.save()
        return instance


class InvoiceStatusListSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=None, required=False)
    middle_name = serializers.CharField(max_length=None, required=False)
    last_name = serializers.CharField(max_length=None, required=False)
    gfront_order_id = serializers.CharField(max_length=None, required=False)
    received_date = serializers.CharField(max_length=None, required=False)
    order_type = serializers.CharField(max_length=None, required=False)
    price = serializers.FloatField(required=False)
    paid = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.gfront_order_id = validated_data.get(
            'gfront_order_id', instance.gfront_order_id)
        instance.received_date = validated_data.get(
            'received_date', instance.received_date)
        instance.kit_number = validated_data.get(
            'kit_number', instance.kit_number)
        instance.order_type = validated_data.get(
            'order_type', instance.order_type)
        instance.price = validated_data.get(
            'price', instance.price)
        instance.paid = validated_data.get(
            'paid', instance.paid)
        instance.save()
        return instance


class InvoiceStatusUpdateSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=None, required=False)
    intent_id = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.session_id = validated_data.get(
            "session_id", instance.session_id)
        instance.intent_id = validated_data.get(
            "intent_id", instance.intent_id)
        instance.save()
        return instance


class HistoryStatusListSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=None, required=False)
    middle_name = serializers.CharField(max_length=None, required=False)
    last_name = serializers.CharField(max_length=None, required=False)
    received_date = serializers.CharField(max_length=None, required=False)
    order_type = serializers.CharField(max_length=None, required=False)
    owe = serializers.FloatField(required=False)
    pay_date = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.received_date = validated_data.get(
            'received_date', instance.received_date)
        instance.order_type = validated_data.get(
            'order_type', instance.order_type)
        instance.owe = validated_data.get(
            'owe', instance.owe)
        instance.pay_date = validated_data.get(
            'pay_date', instance.pay_date)
        instance.save()
        return instance


class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=None, required=False)
    currency = serializers.CharField(max_length=None, required=False)
    customer = serializers.CharField(max_length=None, required=False)
    receipt_email = serializers.CharField(max_length=None, required=False)
    description = serializers.CharField(max_length=None, required=False)
    shipping = serializers.CharField(max_length=None, required=False)
    nam = serializers.CharField(max_length=None, required=False)
    address_line1 = serializers.CharField(max_length=None, required=False)
    address_line2 = serializers.CharField(max_length=None, required=False)
    city = serializers.CharField(max_length=None, required=False)
    province = serializers.CharField(max_length=None, required=False)
    postal_code = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get(
            "amount", instance.amount)
        instance.currency = validated_data.get(
            "currency", instance.currency)
        instance.customer = validated_data.get(
            "customer", instance.customer)
        instance.receipt_email = validated_data.get(
            "receipt_email", instance.receipt_email)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.shipping = validated_data.get(
            "shipping", instance.shipping)
        instance.name = validated_data.get(
            "name", instance.name)
        instance.address_line1 = validated_data.get(
            "address_line1", instance.address_line1)
        instance.address_line2 = validated_data.get(
            "address_line2", instance.address_line2)
        instance.city = validated_data.get(
            "city", instance.city)
        instance.province = validated_data.get(
            "province", instance.province)
        instance.postal_code = validated_data.get(
            "postal_code", instance.postal_code)
        instance.save()
        return instance


class PaymentRetrieveSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.session_id = validated_data.get(
            "session_id", instance.session_id)
        instance.save()
        return instance


class PaymentReadySerializer(serializers.Serializer):
    payment_method = serializers.CharField(max_length=None, required=False)
    save_card = serializers.BooleanField(required=False)
    session_id = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.payment_method = validated_data.get(
            "payment_method", instance.payment_method)
        instance.save_card = validated_data.get(
            "save_card", instance.save_card)
        instance.session_id = validated_data.get(
            "session_id", instance.session_id)
        instance.save()
        return instance


class PaymentFinalSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=None, required=False)
    payment_id = serializers.CharField(max_length=None, required=False)
    intent_id = serializers.CharField(max_length=None, required=False)

    def update(self, instance, validated_data):
        instance.session_id = validated_data.get(
            "session_id", instance.session_id)
        instance.payment_id = validated_data.get(
            "payment_id", instance.payment_id)
        instance.intent_id = validated_data.get(
            "intent_id", instance.intent_id)
        instance.save()
        return instance
