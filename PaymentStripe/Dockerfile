FROM python
ENV STRIPE_KEY_BACKEND='sk_test_4eC39HqLyjWDarjtT1zdp7dc'
ENV DJANGO_SECRET_KEY='django-insecure-y6k)iqgimr%kmoo&la&$9kr53tb!-s!6b#!)1h^o-*ri5rim=g'
WORKDIR /PaymentApp
COPY .. .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]