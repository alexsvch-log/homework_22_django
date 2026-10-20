from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов из Технического Задания 1
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        # Указываем поля, которые будут отображаться в форме на сайте
        fields = ['name', 'description', 'price', 'category', 'image']

        # ДОБАВЛЯЕМ ПЕРЕВОД ОШИБОК:
        error_messages = {
            'image': {
                'invalid_image': "Загружаемый файл не является изображением или поврежден!",
            }
        }

    # ЗАДАНИЕ 3: Стилизация всех полей под дизайн Bootstrap через метод __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Проходим циклом по всем полям нашей формы
        for field_name, field in self.fields.items():
            # Если это обычное текстовое поле, выпадающий список или число — добавляем класс формы Bootstrap
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control'})
            # Если это чекбокс (если будем использовать)
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            # Для поля загрузки файлов (картинок)
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})

    def _validate_forbidden_words(self, text):
        """Вспомогательный метод для проверки текста на наличие запрещенных слов (в любом регистре)"""
        if not text:
            return

        # Переводим весь текст в нижний регистр для проверки без учета регистра
        text_lower = text.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in text_lower:
                raise forms.ValidationError(f'В тексте обнаружено запрещенное слово: "{word}"!')

    # Задание 1: Валидация названия
    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        self._validate_forbidden_words(cleaned_data)
        return cleaned_data

    # Задание 1: Валидация описания
    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        self._validate_forbidden_words(cleaned_data)
        return cleaned_data

    # Задание 2: Кастомная валидация поля price через метод clean_price
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной!')

        return price

        # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Валидация формата и размера изображения

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # ЗАЩИТА: Если файл вообще не загружен, равен False/None, или если это строка/кортеж с ошибкой
        if not image or isinstance(image, (str, tuple, list)):
            return image

        # Проверяем только вновь загруженные файлы (InMemoryUploadedFile)
        from django.core.files.uploadedfile import UploadedFile
        if not isinstance(image, UploadedFile):
            return image

        # 1. Проверяем РАЗМЕР файла (не более 5 МБ)
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise forms.ValidationError('Размер загружаемого файла не должен превышать 5 МБ!')

        # 2. Проверяем ФОРМАТ файла (Сначала разделяем, а потом вызываем .lower() у расширения!)
        import os
        _, ext_raw = os.path.splitext(image.name)
        ext = ext_raw.lower()  # Теперь PyCharm на 100% уверен, что это строка, и не ругается!

        valid_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in valid_extensions:
            raise forms.ValidationError('Неверный формат файла! Допускаются только изображения JPEG и PNG.')

        return image

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Имя")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, label="Телефон")
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Сообщение")

    # Стилизация всех полей формы контактов под Bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.EmailInput)):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label