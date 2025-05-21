from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page

class WordleGame(Page):

    guesses_per_level = models.PositiveIntegerField(
        default=6,
        help_text="The number of guesses this game can have"
    )

    active = models.BooleanField(
        default=True,
        help_text="Whether this game is active"
    )

    date = models.DateField(
        unique=True,
        help_text="The date this game was created"
    )


    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('guesses_per_level'),
        FieldPanel('active'),
        InlinePanel('levels', heading='Levels/Articles'),
    ]



class Article(models.Model):
    article_id = models.CharField(
        max_length=300,
        unique=True,
    )
    date_processed = models.DateField()
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    des_facet = models.TextField()
    org_facet = models.TextField()
    per_facet = models.TextField()
    geo_facet = models.TextField()
    url = models.URLField()


class GameLevel(models.Model):
    daily_game = models.ForeignKey(WordleGame,
                                   on_delete=models.CASCADE,
                                   related_name='levels',
    )
    level_number = models.PositiveIntegerField()
    target_word = models.CharField(max_length=10)

    class Meta:
        unique_together = ('daily_game', 'level_number')