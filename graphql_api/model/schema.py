from .models import *
from graphene_django import DjangoObjectType
import graphene


class CommodityType(DjangoObjectType):
    class Meta:
        model = Commodity
        fields = (
            'id',
            'name',
            'description',
            'price',
            'quantity',
        )


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = (
            'id',
            'first_name',
            'last_name',
            'address',
        )


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            'id',
            'client',
        )


class BasketType(DjangoObjectType):
    class Meta:
        model = Basket
        fields = (
            'id',
            'commodity',
            'order',
        )


class PayType(DjangoObjectType):
    class Meta:
        model = Pay
        fields = (
            'id',
            'order',
            'price',
        )


class Query(graphene.ObjectType):
    commodites = graphene.List(CommodityType)
    clients = graphene.List(ClientType)
    orders = graphene.List(OrderType)
    baskets = graphene.List(BasketType)
    pay = graphene.List(PayType)

    def resolve_commodites(root, info, **kwargs):
        return Commodity.objects.all()

    def resolve_clients(root, info, **kwargs):
        return Client.objects.all()

    def resolve_orders(root, info, **kwargs):
        return Order.objects.all()

    def resolve_baskets(root, info, **kwargs):
        return Basket.objects.all()

    def resolve_pay(root, info, **kwargs):
        return Pay.object.all()


class CommoditeInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    price = graphene.Decimal()
    quantity = graphene.Int()


class CreateCommodite(graphene.Mutation):
    class Arguments:
        input = CommoditeInput(required=True)

    commodite = graphene.Field(CommodityType)

    @classmethod
    def mutate(cls, root, info, input):
        commodite = Commodity()
        commodite.name = input.name
        commodite.description = input.description
        commodite.price = input.price
        commodite.quantity = input.quantity
        commodite.save()
        return CreateCommodite(commodite=commodite)


class UpdateCommodite(graphene.Mutation):
    class Arguments:
        input = CommoditeInput(required=True)
        id = graphene.ID()

    commodite = graphene.Field(CommodityType)

    @classmethod
    def mutate(cls, root, info, input, id):
        commodite = Commodity.objects.get(pk=id)
        commodite.name = input.name
        commodite.description = input.description
        commodite.price = input.price
        commodite.quantity = input.quantity
        commodite.save()
        return UpdateCommodite(commodite=commodite)


class ClientInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    address = graphene.String()


class CreateClient(graphene.Mutation):
    class Arguments:
        input = ClientInput(required=True)

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, input):
        client = Client()
        client.first_name = input.first_name
        client.last_name = input.last_name
        client.address = input.address
        client.save()
        return CreateClient(client=client)


class UpdateClient(graphene.Mutation):
    class Arguments:
        input = ClientInput(required=True)
        id = graphene.ID()

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, input, id):
        client = Client.objects.get(pk=id)
        client.first_name = input.first_name
        client.last_name = input.last_name
        client.address = input.address
        client.save()
        return CreateClient(client=client)


class CreateOrder(graphene.Mutation):
    class Arguments:
        client = graphene.Int()

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, client):
        order = Order()
        order.client = client
        order.save()
        return CreateOrder(order=order)


class UpdateOrder(graphene.Mutation):
    class Arguments:
        client = graphene.Int()
        id = graphene.ID()

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, client, id):
        order = Order.objects.get(pk=id)
        order.client = client
        order.save()
        return CreateOrder(order=order)


class BasketInput(graphene.InputObjectType):
    commodity = graphene.Int()
    order = graphene.Int()


class CreateBasket(graphene.Mutation):
    class Arguments:
        input = BasketInput(required=True)

    basket = graphene.Field(BasketType)

    @classmethod
    def mutate(cls, root, info, input):
        basket = Basket()
        basket.commodity = input.commodity
        basket.order = input.order
        basket.save()
        return CreateBasket(basket=basket)


class UpdateBasket(graphene.Mutation):
    class Arguments:
        input = BasketInput(required=True)
        id = graphene.ID()

    basket = graphene.Field(BasketType)

    @classmethod
    def mutate(cls, root, info, input, id):
        basket = Basket.objects.get(pk=id)
        basket.commodity = input.commodity
        basket.order = input.order
        basket.save()
        return UpdateBasket(basket=basket)


class PayInput(graphene.InputObjectType):
    order = graphene.Int()
    price = graphene.Decimal()


class CreatePay(graphene.Mutation):
    class Arguments:
        input = PayInput(required=True)

    pay = graphene.Field(PayType)

    @classmethod
    def mutate(cls, root, info, input):
        pay = Pay()
        pay.order = input.order
        pay.price = input.price
        pay.save()
        return CreatePay(pay=pay)


class UpdatePay(graphene.Mutation):
    class Arguments:
        input = PayInput(required=True)
        id = graphene.ID()

    pay = graphene.Field(PayType)

    @classmethod
    def mutate(cls, root, info, input, id):
        pay = Pay.objects.get(pk=id)
        pay.order = input.order
        pay.price = input.price
        pay.save()
        return UpdatePay(pay=pay)


class Mutation(graphene.ObjectType):
    create_commodite = CreateCommodite.Field()
    create_client = CreateClient.Field()
    create_order = CreateOrder.Field()
    create_basket = CreateBasket.Field()
    create_pay = CreatePay.Field()
    update_commodite = UpdateCommodite.Field()
    update_client = UpdateClient.Field()
    update_order = UpdateOrder.Field()
    update_basket = UpdateBasket.Field()
    update_pay = UpdatePay.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
