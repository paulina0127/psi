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
    commodities = graphene.List(CommodityType)
    clients = graphene.List(ClientType)
    orders = graphene.List(OrderType)
    baskets = graphene.List(BasketType)
    pay = graphene.List(PayType)
    commodity = graphene.Field(CommodityType, id=graphene.ID())
    client = graphene.Field(ClientType, id=graphene.ID())
    order = graphene.Field(OrderType, id=graphene.ID())
    basket = graphene.Field(BasketType, id=graphene.ID())
    pay = graphene.Field(PayType, id=graphene.ID())

    def resolve_commodities(root, info, **kwargs):
        return Commodity.objects.all()

    def resolve_clients(root, info, **kwargs):
        return Client.objects.all()

    def resolve_orders(root, info, **kwargs):
        return Order.objects.all()

    def resolve_baskets(root, info, **kwargs):
        return Basket.objects.all()

    def resolve_pay(root, info, **kwargs):
        return Pay.objects.all()

    def resolve_commodity(root, info, id):
        return Commodity.objects.get(pk=id)

    def resolve_client(root, info, id):
        return Client.objects.get(pk=id)

    def resolve_order(root, info, id):
        return Order.objects.get(pk=id)

    def resolve_basket(root, info, id):
        return Basket.objects.get(pk=id)

    def resolve_pay(root, info, id):
        return Pay.objects.get(pk=id)


class CommodityInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    price = graphene.Decimal()
    quantity = graphene.Int()


class CreateCommodity(graphene.Mutation):
    class Arguments:
        input = CommodityInput(required=True)

    commodity = graphene.Field(CommodityType)

    @classmethod
    def mutate(cls, root, info, input):
        commodity = Commodity()
        commodity.name = input.name
        commodity.description = input.description
        commodity.price = input.price
        commodity.quantity = input.quantity
        commodity.save()
        return CreateCommodity(commodity=commodity)


class UpdateCommodity(graphene.Mutation):
    class Arguments:
        input = CommodityInput(required=True)
        id = graphene.ID()

    commodity = graphene.Field(CommodityType)

    @classmethod
    def mutate(cls, root, info, input, id):
        commodity = Commodity.objects.get(pk=id)
        commodity.name = input.name
        commodity.description = input.description
        commodity.price = input.price
        commodity.quantity = input.quantity
        commodity.save()
        return UpdateCommodity(commodity=commodity)


class DeleteCommodity(graphene.Mutation):
    response = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        commodity = Commodity.objects.get(pk=id)
        commodity.delete()
        return cls(response=True)


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


class DeleteClient(graphene.Mutation):
    response = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        client = Client.objects.get(pk=id)
        client.delete()
        return cls(response=True)


class CreateOrder(graphene.Mutation):
    class Arguments:
        client = graphene.ID()

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, client):
        order = Order()
        order.client = Client.objects.get(pk=client)
        order.save()
        return CreateOrder(order=order)


class UpdateOrder(graphene.Mutation):
    class Arguments:
        client = graphene.ID()
        id = graphene.ID()

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, client, id):
        order = Order.objects.get(pk=id)
        order.client = Client.objects.get(pk=client)
        order.save()
        return CreateOrder(order=order)


class DeleteOrder(graphene.Mutation):
    response = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        order = Order.objects.get(pk=id)
        order.delete()
        return cls(response=True)


class BasketInput(graphene.InputObjectType):
    commodity = graphene.ID()
    order = graphene.ID()


class CreateBasket(graphene.Mutation):
    class Arguments:
        input = BasketInput(required=True)

    basket = graphene.Field(BasketType)

    @classmethod
    def mutate(cls, root, info, input):
        basket = Basket()
        basket.commodity = Commodity.objects.get(pk=input.commodity)
        basket.order = Order.objects.get(pk=input.order)
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
        basket.commodity = Commodity.objects.get(pk=input.commodity)
        basket.order = Order.objects.get(pk=input.order)
        basket.save()
        return UpdateBasket(basket=basket)


class DeleteBasket(graphene.Mutation):
    response = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        basket = Basket.objects.get(pk=id)
        basket.delete()
        return cls(response=True)


class PayInput(graphene.InputObjectType):
    order = graphene.ID()
    price = graphene.Decimal()


class CreatePay(graphene.Mutation):
    class Arguments:
        input = PayInput(required=True)

    pay = graphene.Field(PayType)

    @classmethod
    def mutate(cls, root, info, input):
        pay = Pay()
        pay.order = Order.objects.get(pk=input.order)
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
        pay.order = Order.objects.get(pk=input.order)
        pay.price = input.price
        pay.save()
        return UpdatePay(pay=pay)


class DeletePay(graphene.Mutation):
    response = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        pay = Pay.objects.get(pk=id)
        pay.delete()
        return cls(response=True)


class Mutation(graphene.ObjectType):
    create_commodity = CreateCommodity.Field()
    create_client = CreateClient.Field()
    create_order = CreateOrder.Field()
    create_basket = CreateBasket.Field()
    create_pay = CreatePay.Field()
    update_commodity = UpdateCommodity.Field()
    update_client = UpdateClient.Field()
    update_order = UpdateOrder.Field()
    update_basket = UpdateBasket.Field()
    update_pay = UpdatePay.Field()
    delete_commodity = DeleteCommodity.Field()
    delete_client = DeleteClient.Field()
    delete_order = DeleteOrder.Field()
    delete_basket = DeleteBasket.Field()
    delete_pay = DeletePay.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
