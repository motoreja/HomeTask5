# Создать класс с полями, в котором реализовать инициализатор и метод обработки данных.
# Спроектировать иерархию классов от изначально написаного класса, используя наследование.
# Дописать как минимум одно уникальное поле для каждого подкласса.
# В классах-наследниках реализовать метод обработки данных.
#
# Класс и его поля: Станок - производительность (изделий в час), стоимость станка, средняя цена детали
#
# Метод 1: количество деталей для окупаемости
# Иерархия: фрезерный станок, станок с ЧПУ
# Метод 2: время окупаемости станка при фиксированной цене детали
#
# Перегрузите оператор сложения add, который будет складывать производительность двух станков


class Machine:
    """Станок"""
    __slots__ = ['__dict__', 'name', 'product', 'cost']

    def __init__(self, name, product=1, cost=0):
        self.name = name
        self.product = product
        self.cost = cost
        self._detail_price = 100

    def __add__(self, other):
        """Создать новый объект как сумму полей 'self' и 'other'."""
        if isinstance(other, Machine) and isinstance(self, Machine):
            newins = self.__class__(self.name + "+" + other.name, self.product + other.product, self.cost + other.cost)
            newins.detail_price = self.detail_price
            return newins
        else:
            raise TypeError(
                f'Не могу сложить {self.__class__} и {type(other)}'
            )

    def __str__(self):
        return f"""Станок "{self.name}".\n\tПроизводительность: {self.product} шт/час. \n\tЦена станка: {self.cost} руб.
        \r\tСредняя цена детали: {self.detail_price} руб."""

    def _details_to_payback(self):
        return int(self.cost/self.detail_price)

    def _time_to_payback(self):
        return self.cost/(self.product*self.detail_price)

    def get_payback_details(self):
        return self._details_to_payback()

    def get_payback_time(self):
        return self._time_to_payback()

    def print_payback(self):
        print(self)
        print(f'\tДеталей до окупаемости: {self.get_payback_details()};\n\tВремя до окупаемости: {self.get_payback_time()}')

    @property
    def detail_price(self):
        return self._detail_price

    @detail_price.setter
    def detail_price(self, newprice):
        assert newprice > 0, 'Цена деали должна быть больше 0!'
        self._detail_price = newprice


class MillingMachine(Machine):
    """Фрезенрный станок"""
    __slots__ = ['efficiency']

    def __init__(self, name, product=1, cost=0, efficiency=0.95):
        self.name = name
        self.product = product
        self.cost = cost
        self.efficiency = efficiency
        self._detail_price = 100

    def __str__(self):
        return f"""Фрезерный станок "{self.name}".\n\tПроизводительность: {self.product} шт/час. \n\tЦена станка: {self.cost} руб.
           \r\tСредняя цена детали: {self.detail_price} руб.
           \r\tЭффективность работы: {self.efficiency} %."""

    def get_payback_details(self):
        # при расчетах используется показатель "Эффективность"
        return int(self._details_to_payback()/self.efficiency)

    def get_payback_time(self):
        # при расчетах используется показатель "Эффективность"
        return self._time_to_payback()/self.efficiency


class CNCMachine(Machine):
    """Фрезенрный станок"""
    __slots__ = ['UsageCost']

    def __init__(self, name, product=1, cost=0, usage=1):
        self.name = name
        self.product = product
        self.cost = cost
        self.usage_cost = usage
        self._detail_price = 100

    def __str__(self):
        return f"""ЧПУ станок "{self.name}".\n\tПроизводительность: {self.product} шт/час. \n\tЦена станка: {self.cost} руб.
           \r\tСредняя цена детали: {self.detail_price} руб.
           \r\tСтоимость обслуживания: {self.usage_cost} руб./час"""

    def get_payback_details(self):
        # при расчетах используется показатель "Стоимость обслуживания"
        ttp = self.get_payback_time()
        cost_bonus = ttp*self.usage_cost
        dtp = self._details_to_payback()
        return dtp + int(cost_bonus/self.product)

    def get_payback_time(self):
        # при расчетах используется показатель "Стоимость обслуживания"
        ttp = self._time_to_payback()
        cost_bonus = ttp*self.usage_cost
        return ttp + cost_bonus/(self.product*self.detail_price)


if __name__ == '__main__':
    # Cоздаем станки
    m1 = MillingMachine("Советский", product=1, cost=100000)
    m1.detail_price = 1000
    m2 = CNCMachine("Стахановец", product=10, cost=500000)
    m2.detail_price = 200
    m3 = m1 + m2

    # рассчитываем окупаемость
    m1.print_payback()
    m2.print_payback()
    m3.print_payback()
