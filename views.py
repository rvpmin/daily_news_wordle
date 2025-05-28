from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

from wagtail.admin.models import get_object_usage

from .utils import fetch_nyt_api
from .utils import WordleGameEngine
from .utils import process_articles
from .models import Article
from .models import GameArticle
from .models import GameLevel
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import DailyGame
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from wagtail.models import Page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def homepage(request):
    today = timezone.now().date()

    try:
        # Obtener el juego de hoy
        game = DailyGame.objects.get(date=today, is_active=True)
        game_articles = game.game_articles.order_by('level_number')

        # Preparar datos para el template
        articles = []
        for ga in game_articles:
            articles.append({
                'id': ga.article.id,
                'title': ga.article.title,
                'abstract': ga.article.abstract,
                'url': ga.article.url,
                'target_word': ga.article.target_word
            })

        context = {
            'articles_json': json.dumps(articles),
            'articles': articles
        }
        return render(request, "wordle/home.html", context)

    except DailyGame.DoesNotExist:

        return render(request, "wordle/no_game.html")


def home(request):
    today = timezone.now().date()

    try:

        game = DailyGame.objects.get(date=today, is_active=True)
        articles = game.game_articles.order_by('level_number')
        return render(request, 'wordle/home.html', {
            'game': game,
            'articles': articles
        })

    except DailyGame.DoesNotExist:

        data = fetch_nyt_api()
        if data:
            articles = process_articles(data)
            print(articles)
            if articles:

                parent = Page.objects.get(slug='games')

                game = DailyGame(
                    title=f"Wordle {today}",
                    date=today,
                    is_active=True,
                    slug=f"wordle-{today}"
                )

                parent.add_child(instance=game)
                game.save_revision().publish()

                for i, article in enumerate(articles[:5], start=1):
                    GameArticle.objects.create(
                        game=game,
                        article=article,
                        level_number=i
                    )
                    print(f"Creado GameArticle: game={ga.game.id}, article={ga.article.id}, level={ga.level_number}")
                return redirect('home')


        return render(request, 'wordle/no_game.html', status=404)


@user_passes_test(lambda u: u.is_staff)
def force_create_game(request):
    if request.method == 'POST':
        today = timezone.now().date()

    try:

        game = DailyGame.objects.get(date=today, is_active=True)
        articles = game.game_articles.order_by('level_number')
        return render(request, 'wordle/home.html', {
            'game': game,
            'articles': articles
        })

    except DailyGame.DoesNotExist:

        data = fetch_nyt_api()
        if data:
            articles = process_articles(data)
            if articles:

                parent = Page.objects.get(slug='games')

                game = DailyGame(
                    title=f"Wordle {today}",
                    date=today,
                    is_active=True,
                    slug=f"wordle-{today}"
                )

                parent.add_child(instance=game)
                game.save_revision().publish()

                for i, article in enumerate(articles[:5], start=1):
                    GameArticle.objects.create(
                        game=game,
                        article=article,
                        level_number=i
                    )
                    print(f"Creado GameArticle: game={ga.game.id}, article={ga.article.id}, level={ga.level_number}")
        messages.success(request, "Juego creado exitosamente")
        return redirect('home')

    return redirect('home')


class LoadArticlesView(LoginRequiredMixin, View):
    def get(self, request):
        data = fetch_nyt_api()
        if data:
            processed = process_articles(data)
            return JsonResponse({'status': 'success', 'count': len(processed)})
        return JsonResponse({'status': 'error'}, status=500)


def game_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if 'wordle_game' not in request.session:
        request.session['wordle_game'] = {
            'article_id': article_id,
            'engine': None,
            'guesses': []
        }

    game_state = request.session['wordle_game']

    if game_state['engine'] is None:
        game_state['engine'] = {
            'target_word': article.target_word,
            'max_guesses': 6,
            'current_guesses': []
        }
        request.session.modified = True

    guesses = game_state['engine']['current_guesses']
    zipped_guesses = [
        zip(g['guess'], g['result']) for g in guesses
    ]

    context = {
        'article': article,
        'title': article.title,
        'abstract': article.abstract,
        'guesses': zipped_guesses
    }

    return render(request, 'wordle/game.html', context)


@require_POST
@csrf_exempt
def check_guess(request, article_id):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            guess = data.get('guess', '')
        else:
            guess = request.POST.get('guess', '')

        if not guess or len(guess) != 5 or not guess.isalpha():
            return JsonResponse(
                {'error': 'La palabra debe tener exactamente 5 letras'},
                status=400
            )

        article = get_object_or_404(Article, pk=article_id)

        # Inicializar o recuperar estado del juego
        session_key = f'wordle_game_{article_id}'
        game_state = request.session.get(session_key, {
            'target_word': article.target_word,
            'max_guesses': 6,
            'guesses': []
        })

        engine = WordleGameEngine(
            word=game_state['target_word'],
            max_guesses=game_state['max_guesses']
        )

        for prev_guess in game_state['guesses']:
            engine.guesses.append(prev_guess)

        result = engine.evaluate_guess(guess.lower())

        game_state['guesses'] = engine.guesses
        request.session[session_key] = game_state

        response_data = {
            'status': result['status'],
            'result': result.get('result'),
            'current_attempt': len(engine.guesses),
            'guesses': engine.guesses,
        }

        if result['status'] in ['won', 'lost']:
            response_data['target_word'] = article.target_word
            del request.session[session_key]

            response_data['article_info'] = {
                'title': article.title,
                'abstract': article.abstract,
                'url': article.url
            }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse(
            {'error': f'Error interno del servidor: {str(e)}'},
            status=500
        )


