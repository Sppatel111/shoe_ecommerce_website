# Shoe E-commerce Website

[![License: Creative Commons](https://img.shields.io/badge/License-CC_BY--NC_4.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/deed.en)

## Description

The Shoe E-commerce Website is a web-based platform built using Django that allows users to browse, search, and purchase various shoes online. This system is designed to provide a seamless shopping experience, complete with user authentication, product categorization, shopping cart functionality, order management, and secure payments via Stripe.

The workflow involves:
1. User registration and login for a personalized experience.
2. Browsing and searching for shoes based on categories and other features.
3. Adding selected shoes to the shopping cart.
4. Managing orders and viewing purchase history.
5. Secure payment processing using Stripe.
6. Admin panel for managing products, categories, and user orders.

## Tech Stack

- **Backend:** Django
- **Database:** MySQL (for storing user data, product information, and order details)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Payment Gateway:** Stripe
- **IDE:** Spyder
- **Python:** 3.11.5
- **Django:** 4.0.0
- **Bootstrap:** 5.1.3

## Demo

![Demo](/store/static/demo.gif)

[Download Demo Video](/store/static/demo.mp4)

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/Sppatel111/shoe-ecommerce-website.git
    ```

2. Set up the MySQL database by creating a database named `shoe_shop` and importing the necessary schema.

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure the Stripe API keys in the project settings. Obtain your API keys from your [Stripe Dashboard](https://dashboard.stripe.com/apikeys) and add them to your Django settings file:

    ```python
    STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
    STRIPE_SECRET_KEY = 'your_stripe_secret_key'
    ```

5. Run the Django application:

    ```bash
    python manage.py runserver
    ```

6. Access the application in your web browser at `http://localhost:8000`.

## Contribution

Contributions to this project are welcome! Here's how you can help:

- Test the application and provide feedback on its functionality and user experience.
- Enhance the search and filtering features for better user experience.
- Improve the frontend design and user interface.
- Report any bugs or issues you encounter while using the application.
- Submit pull requests with new features, optimizations, or bug fixes.

Please note that commercial use of the code or any derived work is not allowed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/deed.en). Contributions should align with the non-commercial nature of the project.

Feel free to fork the repository, make your changes, and submit a pull request. Your contributions are appreciated!

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/deed.en). See the [LICENSE](LICENSE) file for details.
