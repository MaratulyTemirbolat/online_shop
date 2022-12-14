from typing import Any

from django.db.models import (
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    UniqueConstraint,
    CASCADE,  # Удаляет все связанные с ним строки после удаления в основе
)

from abstracts.models import AbstractDateTime

MAX_NAME_LENGTH = 180


class Parameter(AbstractDateTime):
    """Parameters database table."""

    name: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        db_index=True,
        unique=True,
        verbose_name="параметр"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Параметр"
        verbose_name_plural: str = "Параметры"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        """Return string representation of instance."""
        return self.name


class Manufacture(AbstractDateTime):
    """Manufactures database table."""

    name: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Наименование производителя"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Производитель"
        verbose_name_plural: str = "Производители"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        """Return string representation of instance."""
        return self.name


class Category(AbstractDateTime):
    """Categories database table."""

    name: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Категория",
        help_text="Категория ваших товаров"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        """Return string representation of instance."""
        return self.name


class Product(AbstractDateTime):
    """Products database table."""

    name: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Наименование продукта",
        help_text="Наименование продукта производителя (Iphone, Flesh card)"
    )
    manufacture: ForeignKey = ForeignKey(
        to=Manufacture,
        on_delete=CASCADE,
        related_name="products",
        verbose_name="Производитель"
    )
    category: ForeignKey = ForeignKey(
        to=Category,
        on_delete=CASCADE,
        related_name="products",
        verbose_name="Категория"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Продукт"
        verbose_name_plural: str = "Продукты"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        """Return string representation of instance."""
        return self.name


class Good(AbstractDateTime):
    """Goods database table."""

    name: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Наименование товара"
    )
    price_rrc: IntegerField = IntegerField(
        verbose_name="Рекомендованая розничная цена"
    )
    product: ForeignKey = ForeignKey(
        to=Product,
        on_delete=CASCADE
    )
    parameters: ManyToManyField = ManyToManyField(
        to=Parameter,
        through="GoodParameter",
        through_fields=("good", "parameter"),
        related_name="goods",
        blank=True,
        verbose_name="Параметры товара"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Товар"
        verbose_name_plural: str = "Товары"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        """Return string representation of instance."""
        return self.name


class GoodParameter(Model):
    """GoodParameter db model."""

    good: ForeignKey = ForeignKey(
        to=Good,
        on_delete=CASCADE,
        verbose_name="Товар"
    )
    parameter: ForeignKey = ForeignKey(
        to=Parameter,
        on_delete=CASCADE,
        verbose_name="Параметр"
    )
    value: CharField = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Значение"
    )

    class Meta:
        """Customization of the model."""

        verbose_name: str = "Параметр товара"
        verbose_name_plural: str = "Параметры товаров"
        ordering: tuple[str] = ("id",)
        constraints: list[Any] = [
            UniqueConstraint(
                fields=["good", "parameter"],
                name="unique_good_parameter"
            ),
        ]
