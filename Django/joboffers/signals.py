from django.db.models.signals import post_migrate
from django.dispatch import receiver
from algoliasearch_django import AlgoliaIndex
from .models import JobOffer
from algoliasearch.search_client import SearchClient

client = SearchClient.create('ANJZKCTTPT', 'eca59778ff3237f7e961cb2787b74044')
# Index the records in Algolia
index = client.init_index('offre_emploi')

@receiver(post_migrate)
def handle_algolia_update(sender, **kwargs):
    # Define the JobOfferIndex
    class JobOfferIndex(AlgoliaIndex):
        index_name = 'offre_emploi'
        fields = ('Entreprise', 'Titre', 'Date', 'Description', 'Lieu', 'Salaire', 'url', 'img', 'type_poste', 'diplome', 'Experience')
    
    # Convert the JobOffer objects to dictionaries
    # records = [offre.to_dict() for offre in JobOffer.objects.all()] 
    #index.clear_objects() 
    for offre in JobOffer.objects.all():
        index.save_object(offre.to_dict())


