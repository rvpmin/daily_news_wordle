from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page
from modelcluster.fields import ParentalKey


class DailyGame(Page):
    date = models.DateField(unique=True)
    is_active = models.BooleanField(default=True)
    articles = models.ManyToManyField('Article', through='GameArticle')

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('is_active'),
        FieldPanel('articles', heading='Articulos del juego'),
    ]


class GameArticle(models.Model):
    game = models.ForeignKey(DailyGame, on_delete=models.CASCADE, related_name='game_articles')
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    level_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['level_number']


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
    url = models.URLField(unique=True)
    date_processed = models.DateField()
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    target_word = models.CharField(max_length=10)
    '''des_facet = models.TextField(null=True, blank=True)
    org_facet = models.TextField(null=True, blank=True)
    per_facet = models.TextField(null=True, blank=True)
    geo_facet = models.TextField(null=True, blank=True)'''

class GameLevel(models.Model):
    daily_game = models.ForeignKey(WordleGame,
                                   on_delete=models.CASCADE,
                                   related_name='levels',
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    level_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('daily_game', 'level_number')

