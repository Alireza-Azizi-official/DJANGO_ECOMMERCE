# Django E-Commerce Shop  

This project is a fully functional e-commerce website built using the Django framework. It provides all the features necessary for an online shopping experience, including user authentication, product management, cart functionality, and more.  

---

## Features  

### User Authentication  
- **Sign up**: Users can create accounts to access personalized features.  
- **Login/Logout**: Allows users to securely log in and log out of their accounts.  

### E-Commerce Functionality  
- **Product Management**:  
  - Categories: Products are grouped by categories for easy navigation.  
  - Product Details: Each product has a detailed view with a description, price, and image.  
- **Search Functionality**: Search bar allows users to find products quickly.  
- **Shopping Cart**:  
  - Add, update, and remove items in the cart.  
  - Subtotal calculation for items in the cart.  

### Pages  
- **Home**: Displays featured or latest products.  
- **About**: Provides information about the shop.  
- **Contact**: A contact form to allow users to reach out to the shop's support team.  

### Additional Features  
- **Commenting System**: Users can leave comments on products.  
- **Responsive Design**: The site is mobile-friendly and adapts to different screen sizes.  

---

## Installation  

### Prerequisites  
- Python 3.10 or higher  
- Django 5.1.4 or higher  
- Virtual environment (recommended)  

### Setup  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-repository-url.git  
   ```  

2. Navigate to the project directory:  
   ```bash  
   cd django-ecommerce  
   ```  

3. Create and activate a virtual environment:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```  

4. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

5. Run migrations:  
   ```bash  
   python manage.py makemigrations  
   python manage.py migrate  
   ```  

6. Create a superuser (admin account):  
   ```bash  
   python manage.py createsuperuser  
   ```  

7. Start the development server:  
   ```bash  
   python manage.py runserver  
   ```  

8. Access the website at:  
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

---

## Folder Structure  

- `templates/`: HTML templates for frontend pages.  
- `static/`: Static files such as CSS, JavaScript, and images.  
- `media/`: Uploaded images (e.g., product photos).  
- `site photo/`: Contains a sample screenshot of the project.  
- `store/`: Main app handling core e-commerce functionality.  
- `cart/`: App managing shopping cart logic.  
- `account/`: App for user authentication and account management.  

---

## How It Works  

1. **Users**: Create an account or log in.  
2. **Shopping**: Browse through products by category or search for specific items.  
3. **Cart**: Add desired items to the shopping cart.  
4. **Checkout**: (Future functionality: Payment integration can be added).  
5. **Commenting**: Leave comments or feedback on product pages.  

---

## Future Enhancements  

- Payment gateway integration (e.g., Stripe, PayPal).  
- Product review system with ratings.  
- Wishlist functionality.  
- Admin dashboard for analytics and inventory management.  
- Advanced search with filters (price range, ratings, etc.).  

---

## Screenshot  

A preview of the site can be found in the `site photo/` folder.  

---

## Contributing  

Contributions are welcome! Feel free to fork the repository and submit a pull request.  

---

## License  

This project is licensed under the MIT License.  

---

Let me know if you want to include any additional information or further customization! 😊