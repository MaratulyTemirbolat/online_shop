from email.policy import default
from typing import Any

from django.db.models import (
    URLField,
    CharField,
    BooleanField,
    ManyToManyField,
    Model,
    ForeignKey,
    IntegerField,
    CASCADE,
    UniqueConstraint,
)

from abstracts.models import AbstractDateTime

from goods.models import Good
from shops.validators import (
    negative_price_validator,
    negative_quantity_validator,
)


class Shop(AbstractDateTime):
    """Ships database table."""

    MAX_LEN_URL_NAME = 254

    url: URLField = URLField(
        max_length=MAX_LEN_URL_NAME,
        verbose_name="URL"
    )
    name: CharField = CharField(
        max_length=MAX_LEN_URL_NAME,
        verbose_name="Наименование магазина"
    )
    is_active: BooleanField = BooleanField(
        default=True,
        verbose_name="Статус активности"
    )
    goods: ManyToManyField = ManyToManyField(
        to=Good,
        through="ShopGood",
        through_fields=("shop", "good"),
        related_name="shops",
        blank=True,
        verbose_name="Товары магазина"
    )

    def __str__(self) -> str:
        """Override default method."""
        return f"{self.name}"

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Магазин"
        verbose_name_plural: str = "Магазины"
        ordering: tuple[str] = ("pk", "name",)


class ShopGood(Model):
    """Shops database table."""

    shop: ForeignKey = ForeignKey(
        to=Shop,
        on_delete=CASCADE,
        verbose_name="Магазин"
    )
    good: ForeignKey = ForeignKey(
        to=Good,
        on_delete=CASCADE,
        verbose_name="Товар"
    )
    unit_price: IntegerField = IntegerField(
        validators=[negative_price_validator],
        verbose_name="Цена за единицу товара"
    )
    remained_numbee: IntegerField = IntegerField(
        default=0,
        validators=[negative_quantity_validator],
        verbose_name="Остаток товара"
    )

    class Meta:
        """Database table configuration."""

        verbose_name: str = "Товар магазина"
        verbose_name_plural: str = "Товары магазинов"
        ordering: tuple[str] = ("id",)
        constraints: list[Any] = [
            UniqueConstraint(
                fields=["shop", "good"],
                name="unique_shop_good"
            ),
        ]
