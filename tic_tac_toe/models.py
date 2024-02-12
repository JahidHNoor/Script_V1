from django.db import models
from core.models import core_model


class Tic_tac_toe_room(models.Model):
    player1 = models.CharField(max_length=100 , null=True , blank=True)
    player2 = models.CharField(max_length=100 , null=True , blank=True)
    
    def __str__(self) -> str:
        return f"{self.id}"
