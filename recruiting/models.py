from django.db import models


class Planet(models.Model):
    planet_name = models.CharField('название планеты', max_length=50)

    def __str__(self):
        return self.planet_name

    class Meta:
        verbose_name = 'планета'
        verbose_name_plural = 'планеты'


class Recruit(models.Model):
    recruit_name = models.CharField('имя рекрута', max_length=50)
    living_planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    recruit_age = models.IntegerField('возраст рекрута')
    recruit_email = models.EmailField('email рекрута')
    teacher = models.ForeignKey('Sith', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.recruit_name

    class Meta:
        verbose_name = 'рекрут'
        verbose_name_plural = 'рекруты'


class Sith(models.Model):
    sith_name = models.CharField('имя ситха', max_length=50)
    teaching_planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    student = models.ManyToManyField(Recruit, blank=True)
    max_number_of_recruits = 3

    def __str__(self):
        return self.sith_name

    class Meta:
        verbose_name = 'ситх'
        verbose_name_plural = 'ситхи'

    def can_take_student(self):
        return self.student.count() < self.max_number_of_recruits


class ShadowHandTest(models.Model):
    order_id = models.CharField('уникальный код ордена', max_length=50)
    question = models.CharField('вопрос', max_length=200)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'тестовое испытание'
        verbose_name_plural = 'тестовые испытания'


class Answer(models.Model):
    test = models.ForeignKey(ShadowHandTest, on_delete=models.CASCADE)
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    answer = models.BooleanField('ответ на вопрос')

    def __str__(self):
        return f'Ответ {self.recruit} на вопрос {self.test}'

    class Meta:
        verbose_name = 'ответы на тестовое испытание'
        verbose_name_plural = 'ответы на тестовые испытания'
