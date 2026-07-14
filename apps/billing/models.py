from django.db import models

class LOCRate(models.Model):
    loc_level = models.CharField(max_length=50, unique=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.loc_level}: ${self.daily_rate}"
