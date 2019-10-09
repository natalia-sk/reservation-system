from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField()


class Reservation(models.Model):
    reservation_date = models.DateField()
    comment = models.TextField(null=True)
    rooms = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ("reservation_date", "rooms")
