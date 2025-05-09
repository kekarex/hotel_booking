from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        choices=[(i, f"{i} звёзд{'ы' if i>1 else ''}") for i in range(1,6)],
        default=5
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.user.username} ({self.rating}/5 – {self.created_at:%Y-%m-%d})"
