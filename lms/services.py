import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Сервис для работы с Stripe API"""

    @staticmethod
    def create_product(course):
        """Создание продукта в Stripe"""
        try:
            product = stripe.Product.create(
                name=course.name,
                description=course.description or "Онлайн курс",
                metadata={
                    'course_id': str(course.id),
                    'course_name': course.name
                }
            )
            return product.id
        except stripe.error.StripeError as e:
            raise Exception(f"Ошибка создания продукта в Stripe: {str(e)}")

    @staticmethod
    def create_price(product_id, amount):
        """Создание цены в Stripe (сумма в копейках)"""
        try:
            # Конвертируем рубли в копейки
            amount_cents = int(Decimal(str(amount)) * 100)

            price = stripe.Price.create(
                unit_amount=amount_cents,
                currency='rub',
                product=product_id,
                metadata={
                    'currency': 'RUB',
                    'amount_rub': str(amount)
                }
            )
            return price.id
        except stripe.error.StripeError as e:
            raise Exception(f"Ошибка создания цены в Stripe: {str(e)}")

    @staticmethod
    def create_checkout_session(price_id, success_url, cancel_url, metadata=None):
        """Создание сессии для оплаты"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {}
            )
            return session.id, session.url
        except stripe.error.StripeError as e:
            raise Exception(f"Ошибка создания сессии в Stripe: {str(e)}")

    @staticmethod
    def get_session_status(session_id):
        """Получение статуса сессии"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return session.payment_status, session.status
        except stripe.error.StripeError as e:
            raise Exception(f"Ошибка получения статуса сессии: {str(e)}")

    @staticmethod
    def create_payment_for_course(course, user, request):
        """Создание платежа для курса"""
        from .models import Payment

        # Проверяем, есть ли уже активный платеж для этого курса и пользователя
        existing_payment = Payment.objects.filter(
            user=user,
            course=course,
            status__in=['pending', 'processing']
        ).first()

        if existing_payment:
            return existing_payment

        # Создаем платеж в нашей системе
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=course.price
        )

        try:
            # Создаем продукт в Stripe
            product_id = StripeService.create_product(course)
            payment.stripe_product_id = product_id

            # Создаем цену в Stripe
            price_id = StripeService.create_price(product_id, course.price)
            payment.stripe_price_id = price_id

            # Создаем URL для редиректа
            base_url = request.build_absolute_uri('/')
            success_url = f"{base_url}api/payments/success/?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{base_url}api/payments/cancel/"

            # Создаем сессию в Stripe
            metadata = {
                'payment_id': str(payment.id),
                'course_id': str(course.id),
                'user_id': str(user.id)
            }

            session_id, session_url = StripeService.create_checkout_session(
                price_id,
                success_url,
                cancel_url,
                metadata
            )

            payment.stripe_session_id = session_id
            payment.payment_url = session_url
            payment.save()

            return payment

        except Exception as e:
            payment.status = 'failed'
            payment.save()
            raise e