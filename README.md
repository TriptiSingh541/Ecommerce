**E-Commerce Backend API**
This project is a RESTful API built using Django, Django REST Framework (DRF), and Django Channels. It powers a simple e-commerce platform with user authentication, product management, cart functionality, and real-time order updates.
**Features**
1.User registration and login using JWT authentication
2.User profile retrieval and update
3.Admin-managed categories and products
4.Cart functionality for authenticated users
5.Order placement from cart
6.Real-time order status updates using WebSockets
7.Admin can update order statuses

**Technologies Used**
- Django: Backend web framework
- Django REST Framework: API handling
- Django Channels: Real-time WebSocket communication
- Djangorestframework Simplejwt: JWT-based authentication
- PostgreSQL: Database

##  API Endpoints Overview
Authentication:
- `POST /register/` - Register a new user
- `POST /token/` → Obtain JWT access and refresh tokens
- `POST /token_refresh/` → Refresh JWT access token

User Profile:
- `GET /profile/` → Retrieve authenticated user's profile
- `PUT /profile/` → Update profile

Products and Categories:
- `GET /categories/` → List all categories
- `GET /products/` → List all products
  (Admins can perform full CRUD through DRF's admin interface or using viewsets.)

Cart and Orders:
- `POST /cart_add/` → Add product to cart
- `POST /order_place/` → Place order from cart
- `POST /create/` → Manually create an order
- `POST /order/<order_id>/status/` → Admin updates order status
- `POST /update_order/<order_id>/` → Alternate view to update order (used with @login_required)

**Setup Instructions**

1.Clone the repository
  Use the following command to clone the repository:
  `git clone https://github.com/TriptiSingh541/Ecommerce.git`
2.Navigate to the project directory
  Move into the cloned project folder:
   e.g `cd ecommerce-backend` 
3.Create a virtual environment
4.Install project dependencies
   `pip install -r requirements.txt`
5.Apply database migrations
  Run the following to create necessary tables:
  `python manage.py migrate` 
6.Create a superuser
  To access the admin panel, run:
  `python manage.py createsuperuser`
  Enter a username, email, and password when prompted.  
7.Run the development server
  Start the backend server locally:
  `python manage.py runserver`
  Visit http://127.0.0.1:8000/ in your browser. 
8.Access the admin panel
  Open your browser and go to:
  http://127.0.0.1:8000/admin/
  Log in with the superuser credentials.  
9.Run ASGI server for WebSocket support
  If using Django Channels for real-time features:
  `daphne ecommerce.asgi:application` 

