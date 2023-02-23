from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.views import View

from .models import Category, Customer, Order, Product


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}   
         
    products = None
    categories = Category.get_all_categories()
    
    categoryID = request.GET.get('category')
    
    if categoryID:
        products = Product.get_products_by_category_id(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['cats'] = categories

    # print('you are : ', request.session.get('email'))
    return render(request, 'itshop/index.html', data)


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        return render(request, 'itshop/cart.html',{'products':products})


class CheckOut(View):
    # def get(self, request):
    def  post(self, request):
        name = request.POST.get('name')
        address = request.POST.get('address')
        cell = request.POST.get('cell')
        # customer = Customer.objects.get(id=1)
        customer = customer.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))

        for product in products:
            order = Order(
                product = product,
                customer = customer,
                quantity = 1,
                delevery_address = address,
                price = product.sell_price - (product.sell_price * product.discount) / 100,
                phone = cell,
            
            )
            order.placeOrder()

            orders = Order.get_orders_by_customer(customer)
        
        request.session['cart'] = {}
        return render(request, 'itshop/orders.html', {'orders':orders})
        

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'itshop/login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        # print (email, password)
        return render (request, 'itshop/login.html', {'error': error_message})



class Signup (View):
    def get(self, request):
        return render(request, 'itshop/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        cell = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'cell': cell,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            cell=cell,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, cell, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'itshop/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.cell:
            error_message = 'Enter your Phone Number'
        elif len(customer.cell) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
    

def logout(request):
    request.session.clear()
    return redirect('login')















# ================================

    
# class Cart(View):
#     def get(self , request):
#         ids = list(request.session.get('cart').keys())
#         products = Product.get_product_by_id(ids)
#         return render(request , 'itshop/cart.html' , {'products' : products} )



# class Signup(View):
#     pass

# class Login(View):
#     pass


# class CheckOut(View):
#     def post(self, request):
#         address = request.POST.get('address')
        
#         phone = request.POST.get('phone')
#         # print('++++++++++++++++++++'+ phone + '++++++++++++++++')
#         # customer = request.session.get('customer')
#         # customer=Customer.objects.get(1)
       
        
#         cart = request.session.get('cart')
#         products = Product.get_product_by_id(list(cart.keys()))
        
#         for product in products:
#             print(cart.get(str(product.id)))
#             order = Order(
#                           customer=Customer(id=1),
#                         #   customer=Customer.objects.get(1),
#                           product=product,
#                           price=product.sell_price,
#                           delevery_address=address,
#                           phone=phone,
#                           quantity=cart.get(str(product.id)))
#             order.save()
#         request.session['cart'] = {}

#         return redirect('cart')


# class OrderView(View):
#     def get(self , request ):
#         customer = request.session.get('customer')
#         orders = Order.get_orders_by_customer(customer)
#         print(orders)
#         return render(request , 'orders.html'  , {'orders' : orders})


# def logout(request):
#     request.session.clear()
#     return redirect('login')
