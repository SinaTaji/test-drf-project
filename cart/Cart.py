from cart.serializers import ProductSerializer
from product.models import Product

Cart_Session_Id = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(Cart_Session_Id)
        if not cart:
            cart = self.session[Cart_Session_Id] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            product_data = ProductSerializer(product).data
            cart[str(product.id)]['product'] = product_data
        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += int(quantity)

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
