from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects',
        verbose_name='Автор'
    )
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-адрес', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField(
        'Изображение', upload_to='projects/', blank=True, null=True
    )
    technologies = models.CharField(
        'Технологии', max_length=500,
        help_text='Через запятую: Python, Django, JavaScript'
    )
    demo_url = models.URLField('Ссылка на демо', blank=True)
    github_url = models.URLField('Ссылка на GitHub', blank=True)
    is_featured = models.BooleanField('Избранный проект', default=False)
    created_date = models.DateField('Дата создания', auto_now_add=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order', '-created_date']

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images',
        verbose_name='Проект'
    )
    image = models.ImageField('Изображение', upload_to='projects/gallery/')
    caption = models.CharField('Подпись', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проекта'
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} — Изображение {self.order}'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('design', 'Дизайн'),
        ('devops', 'DevOps'),
        ('mobile', 'Мобильная разработка'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='skills',
        verbose_name='Пользователь'
    )
    name = models.CharField('Название', max_length=100)
    icon_class = models.CharField(
        'CSS класс иконки (Font Awesome)', max_length=100,
        help_text='Например: fa-brands fa-python', default='fa-solid fa-code'
    )
    percentage = models.PositiveIntegerField(
        'Уровень (%)', default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    category = models.CharField(
        'Категория', max_length=20, choices=CATEGORY_CHOICES, default='other'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.percentage}%)'


class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='education',
        verbose_name='Пользователь'
    )
    institution = models.CharField('Учебное заведение', max_length=300)
    degree = models.CharField('Степень/Уровень', max_length=200, blank=True)
    field_of_study = models.CharField('Направление', max_length=300, blank=True)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.institution} — {self.field_of_study}'


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='experience',
        verbose_name='Пользователь'
    )
    company = models.CharField('Компания', max_length=300)
    position = models.CharField('Должность', max_length=300)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.company} — {self.position}'
