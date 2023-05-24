from django.db import models
from django_mysql.models import SizedTextField

class JobOffer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    Entreprise = models.CharField(max_length=150)
    Titre =  models.CharField(max_length=150)
    Date = models.DateField()
    Description = SizedTextField(size_class=3)
    Lieu  = models.CharField(max_length=150)
    Salaire = models.CharField(max_length=45)
    url = models.CharField(max_length=150)
    img = models.CharField(max_length=150)
    type_poste = models.CharField(max_length=45)
    diplome = models.CharField(max_length=100)
    Experience = models.CharField(max_length=100)
    SalaireMin = models.CharField(max_length=10)
    SalaireMax = models.CharField(max_length=10)
    def to_dict(self):
        return {
            'objectID': str(self.pk),
            'Entreprise': self.Entreprise,
            'Titre': self.Titre,
            'Date': self.Date.isoformat(),
            'Description': self.Description,
            'Lieu': self.Lieu,
            'Salaire': self.Salaire,
            'url': self.url,
            'img': self.img,
            'type_poste': self.type_poste,
            'diplome': self.diplome,
            'Experience': self.Experience
        }
# Create your models here.
