# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Game

# @receiver(post_save, sender=Game)
# def add_deck_to_game(sender, instance, created, **kwargs):
#     if created:
#         instance.save_deck_to_database()
