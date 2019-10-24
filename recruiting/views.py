from django.shortcuts import render
from .models import Planet, Recruit, ShadowHandTest, Sith, Answer
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail


def choice(request):
    return render(request, 'recruiting/choice.html', {})


def for_sith(request):
    siths = Sith.objects.all()
    return render(request, 'recruiting/for_sith.html', {'siths': siths})


def for_recruit(request):
    planet_list = Planet.objects.all()
    return render(request, 'recruiting/for_recruit.html', {'planet_list': planet_list})


def recruit_data(request, planet_id):
    try:
        planet = Planet.objects.get(id=planet_id)
    except:
        raise Http404('Планета не найдена')
    return render(request, 'recruiting/recruit_data.html', {'planet': planet})


def create_recruit(request, planet_id):
    try:
        planet = Planet.objects.get(id=planet_id)
    except:
        raise Http404('Планета не найдена')
    recruit_name = request.POST['name']
    recruit_age = request.POST['age']
    recruit_email = request.POST['email']
    try:
        Recruit.objects.get(recruit_name=recruit_name, recruit_age=recruit_age, recruit_email=recruit_email)
    except MultipleObjectsReturned:
        raise Http404('Такой рекрут уже есть')
    except ObjectDoesNotExist:
        pass
    planet.recruit_set.create(recruit_name=recruit_name, recruit_age=recruit_age, recruit_email=recruit_email)
    recruit = Recruit.objects.get(recruit_name=recruit_name, recruit_age=recruit_age, recruit_email=recruit_email)
    return HttpResponseRedirect(reverse('recruiting:test', args=(recruit.id,)))


def test(request, recruit_id):
    try:
        recruit = Recruit.objects.get(id=recruit_id)
    except:
        raise Http404('Рекрут не найден')
    questions = ShadowHandTest.objects.all()
    return render(request, 'recruiting/test.html', {'recruit': recruit, 'questions': questions})


def send_test(request, recruit_id):
    try:
        recruit = Recruit.objects.get(id=recruit_id)
    except:
        raise Http404('Рекрут не найден')
    questions = ShadowHandTest.objects.all()
    for question in questions:
        if request.POST.get(question.id) == 'true':
            answer = True
        else:
            answer = False
        recruit.answer_set.create(test=ShadowHandTest.objects.get(id=question.id), answer=answer)
    return HttpResponseRedirect(reverse('recruiting:choice'))


def sith_data(request, sith_id):
    try:
        sith = Sith.objects.get(id=sith_id)
    except:
        raise Http404('Ситх не найден')
    try:
        recruits = Recruit.objects.filter(living_planet=sith.teaching_planet, teacher__isnull=True)
    except ObjectDoesNotExist:
        recruits = []
    questions = ShadowHandTest.objects.all()
    answers = []
    recruit_results = {}
    if recruits:
        for recruit in recruits:
            for question in questions:
                try:
                    answers.append(Answer.objects.get(test=question, recruit=recruit))
                except ObjectDoesNotExist:
                    pass
            recruit_results[recruit] = dict(zip(questions, answers))
    return render(request, 'recruiting/sith_data.html', {'sith': sith, 'recruit_results': recruit_results})


def accept_recruit(request, sith_id):
    try:
        sith = Sith.objects.get(id=sith_id)
    except:
        raise Http404('Ситх не найден')
    recruit = Recruit.objects.get(id=request.POST['recruit'])
    sith.student.add(recruit)
    sith.save()
    recruit.teacher = sith
    recruit.save()
    send_mail(f'{recruit.recruit_name}, ты принят в ряды Руки Тени',
              f'{recruit.recruit_name}, ты принят в ряды Руки Тени, твой мастер {recruit.teacher.sith_name} ждет тебя',
              'from@sw.com', [recruit.recruit_email], fail_silently=False)
    return HttpResponseRedirect(reverse('recruiting:sith_data', args=(sith.id,)))
