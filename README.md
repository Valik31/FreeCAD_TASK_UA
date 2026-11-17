# FreeCAD: завдання та відеоуроки

Сайт з уроками FreeCAD (аналог GitBook) на **GitHub Pages** + **Docsify**.
Нічого встановлювати не треба: все редагується прямо в браузері на GitHub.

## Структура

| Файл / папка | Що це |
|---|---|
| `home.md` | Головна сторінка сайту |
| `_sidebar.md` | Меню зліва (список уроків) |
| `lessons/` | Сторінки уроків |
| `assets/` | Картинки |
| `templates/lesson-template.md` | Шаблон для нового уроку |
| `index.html` | Налаштування сайту (зазвичай не чіпати) |

## Як додати відео до уроку

1. Відкрийте файл уроку, наприклад `lessons/01-lego-head.md`, і натисніть ✏️ (Edit).
2. Візьміть код відео з посилання YouTube: у `https://www.youtube.com/watch?v=abc123XYZ` це `abc123XYZ`
   (у `https://youtu.be/abc123XYZ` теж `abc123XYZ`).
3. Вставте такий блок, замінивши `VIDEO_ID`:
   ```html
   <div class="video">
     <iframe src="https://www.youtube.com/embed/VIDEO_ID" allowfullscreen></iframe>
   </div>
   ```
4. Натисніть **Commit changes**. Через 1–2 хвилини сайт оновиться.

> Видимість відео на YouTube має бути «Відкритий доступ» або «За посиланням». Приватні відео не покажуться.

## Як додати новий урок

1. Відкрийте папку `lessons` → **Add file → Create new file**.
2. Назвіть файл, наприклад `02-nazva.md` (латиницею, без пробілів).
3. Скопіюйте вміст з `templates/lesson-template.md` і заповніть.
4. У файлі `_sidebar.md` додайте рядок:
   ```
     - [2. Назва уроку](lessons/02-nazva.md)
   ```
5. За бажанням додайте картку на головну (`home.md`), скопіювавши блок `<a>…</a>`.

## Як додати картинку

Відкрийте папку `assets` → **Add file → Upload files** і перетягніть картинку.
У тексті уроку: `<img class="preview" src="assets/назва.jpg">`

## Як увімкнути сайт (один раз)

**Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, папка `/ (root)` → Save.**
Через хвилину сайт буде за адресою `https://<ваш-логін>.github.io/<назва-репозиторію>/`.

## Перегляд на своєму комп'ютері (необов'язково)

```
python -m http.server 3000
```
і відкрити `http://localhost:3000`.
