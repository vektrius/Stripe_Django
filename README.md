# Integration with Stripe

## Overview

Integration with Stripe was done with Django.
<br> Test task for the Ришат.

## Stack

* Python
* Django
* Stripe
* Docker
## How to run  

1. Clone the repository from GitHub:

    $ git clone https://github.com/vektrius/Stripe_Django.git

2. Navigate into the project directory:

    $ cd Stripe_Django/PaymentStripe/

3. Create image:

    $ docker build -t paymentdjango .
4. Run container:

    $ docker run -p 8000:8000 paymentdjango
5. Open site:

    http://127.0.0.1:8000/

