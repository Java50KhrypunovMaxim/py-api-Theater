from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from uuid import uuid4
import pathlib


def play_image_path(instance: "Play", filename: str) -> str:
    filename = (f"{slugify(instance.title)}-{uuid4()}"
                + pathlib.Path(filename).suffix)
    return f"upload-image/{filename}"


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", related_name="plays",
                                    blank=True)
    genres = models.ManyToManyField("Genre", related_name="plays",)
    image = models.ImageField(null=True, upload_to=play_image_path)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey("Play", on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey("TheatreHall", on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return str(self.id)

    @property
    def capacity(self):
        return self.theatre_hall.capacity


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey("Performance",
                                    on_delete=models.CASCADE,
                                    related_name="tickets")
    reservation = models.ForeignKey("Reservation",
                                    on_delete=models.CASCADE,
                                    related_name="tickets")

    @staticmethod
    def validate_ticket(row, seat, theatre_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(theatre_hall,
                                  theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in "
                                          f"available range:"
                                          f"(1, {theatre_hall_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.performance.theatre_hall,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]
