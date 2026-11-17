# Урок 3. Блок 2×4

<img class="preview" src="block2x4-00.jpg" alt="Готовий блок LEGO 2×4 зверху і знизу">

**Завдання.** Спроєктуйте у FreeCAD деталь LEGO 2×4.

**Що навчимося:** будувати центральний прямокутник, прив'язувати ескіз до країв грані через <img class="ic" src="icons/external.svg" alt="" data-no-zoom>**зовнішню геометрію**, ставити обмеження <img class="ic" src="icons/equal.svg" alt="" data-no-zoom>**рівності** і <img class="ic" src="icons/symmetric.svg" alt="" data-no-zoom>**симетрії**, робити <img class="ic" src="icons/linear-pattern.svg" alt="" data-no-zoom>**лінійний масив** і <img class="ic" src="icons/pocket.svg" alt="" data-no-zoom>**виріз**, налаштовувати матеріал і колір.

## Відео

<div class="video">
  <iframe src="https://www.youtube.com/embed/t6yTvfP7Ums" allowfullscreen></iframe>
</div>

## Хід роботи

### 1. Основа

1. Відкрийте FreeCAD і під час створення нового файлу виберіть <img class="ic" src="icons/body.svg" alt="" data-no-zoom>**Parametric Body**.
2. Натисніть <img class="ic" src="icons/new-sketch.svg" alt="" data-no-zoom>**Новий ескіз** (New Sketch) і виберіть площину **XY**. Ескіз відкриється в режимі редагування, і ви дивитиметеся на нього згори.
3. Виберіть інструмент <img class="ic" src="icons/rect-center.svg" alt="" data-no-zoom>**Центральний прямокутник** (Centered Rectangle) і клацніть у точці початку координат.
4. Введіть з клавіатури розміри: ширина **47,7 мм**, довжина **23,7 мм**.

   ![Ескіз основи 47,7 × 23,7 мм](block2x4-01.jpg)

5. Вийдіть з ескізу кнопкою <img class="ic" src="icons/leave-sketch.svg" alt="" data-no-zoom>**Leave Sketch**.
6. Видавіть ескіз інструментом <img class="ic" src="icons/pad.svg" alt="" data-no-zoom>**Видавлювання** (Pad) на **14,4 мм**. Інші параметри залишіть як є й натисніть **ОК**.

   ![Видавлювання основи на 14,4 мм](block2x4-02.jpg)

### 2. Шипи зверху

7. Виділіть **верхню грань** блока й натисніть <img class="ic" src="icons/new-sketch.svg" alt="" data-no-zoom>**Новий ескіз**.
8. Намалюйте одне коло інструментом <img class="ic" src="icons/circle.svg" alt="" data-no-zoom>**Circle** у будь-якому місці.
9. Кола треба розташувати відносно країв грані, тому скористаємося інструментом <img class="ic" src="icons/external.svg" alt="" data-no-zoom>**Зовнішня геометрія** (External geometry). Він дає змогу посилатися на ребра грані й точно прив'язувати до них кола:
   - спочатку клацніть кнопку <img class="ic" src="icons/construction.svg" alt="" data-no-zoom>**Режим допоміжних ліній** (Toggle construction geometry), щоб лінії стали пунктирними;
   - виберіть інструмент <img class="ic" src="icons/external.svg" alt="" data-no-zoom>**Зовнішня геометрія** і клацніть по прямокутнику (краях грані);
   - знову клацніть кнопку <img class="ic" src="icons/construction.svg" alt="" data-no-zoom>**Режим допоміжних ліній**, щоб вимкнути його.
10. Інструментом <img class="ic" src="icons/dimension.svg" alt="" data-no-zoom>**Розмірність** задайте відстань **6 мм** від центра кола до лівого ребра. Так само задайте 6 мм до верхнього ребра.
11. Задайте **діаметр кола 7,2 мм**.
12. Намалюйте друге коло.
13. Затисніть **Ctrl**, виберіть обидва кола і застосуйте обмеження <img class="ic" src="icons/equal.svg" alt="" data-no-zoom>**рівності**.
14. Затисніть **Ctrl**, виберіть центри обох кіл і вісь X (червону лінію), потім застосуйте обмеження <img class="ic" src="icons/symmetric.svg" alt="" data-no-zoom>**симетрії**.

    ![Два кола: 6 мм від країв, діаметр 7,2 мм, симетричні відносно осі X](block2x4-03.jpg)

15. Вийдіть з ескізу (<img class="ic" src="icons/leave-sketch.svg" alt="" data-no-zoom>**Leave Sketch**) і видавіть його (<img class="ic" src="icons/pad.svg" alt="" data-no-zoom>**Pad**) на **2,7 мм**.

    ![Видавлювання двох шипів на 2,7 мм](block2x4-04.jpg)

16. Виділіть щойно створене видавлювання (**Pad001**) і натисніть <img class="ic" src="icons/linear-pattern.svg" alt="" data-no-zoom>**Лінійний масив**. Напрямок: **горизонтальна вісь ескізу**, довжина **36 мм** (проміжок, у який мають уміститися копії), кількість **4**. Натисніть **ОК**.

    ![Лінійний масив: 36 мм, 4 копії](block2x4-05.jpg)

### 3. Виріз знизу з трубками

17. Поверніть модель, виділіть **нижню грань** блока й натисніть <img class="ic" src="icons/new-sketch.svg" alt="" data-no-zoom>**Новий ескіз**.
18. Прив'яжіть ескіз до країв грані так само, як у кроці 9:
    - клацніть кнопку <img class="ic" src="icons/construction.svg" alt="" data-no-zoom>**Режим допоміжних ліній**;
    - виберіть <img class="ic" src="icons/external.svg" alt="" data-no-zoom>**Зовнішня геометрія** і клацніть по прямокутнику;
    - знову клацніть кнопку <img class="ic" src="icons/construction.svg" alt="" data-no-zoom>**Режим допоміжних ліній**.
19. Намалюйте довільний <img class="ic" src="icons/rect.svg" alt="" data-no-zoom>**прямокутник**. Інструментом <img class="ic" src="icons/dimension.svg" alt="" data-no-zoom>**Розмірність** задайте відстань **1,8 мм** від верхнього лівого кута прямокутника до лівого ребра і так само до верхнього ребра.
20. Затисніть **Ctrl**, виберіть верхній лівий кут прямокутника, нижній правий кут і точку початку координат, потім застосуйте <img class="ic" src="icons/symmetric.svg" alt="" data-no-zoom>**симетрію**.
21. Намалюйте коло з центром **на осі X** (червона лінія) і діаметром **9,765 мм**. Задайте відстань від його центра до лівого ребра прямокутника: **10,2 мм**.
22. Намалюйте ще два кола: одне з центром у початку координат, друге з центром на осі X. Діаметри можуть бути довільні.
23. Затисніть **Ctrl**, виберіть усі три кола й застосуйте <img class="ic" src="icons/equal.svg" alt="" data-no-zoom>**рівність**.
24. Задайте відстань від центра правого кола до правого ребра прямокутника: **10,2 мм**.
25. Намалюйте ще три кола **діаметром 7,2 мм** зі спільними центрами з трьома попередніми колами.

    ![Ескіз знизу: стінки 1,8 мм і три трубки](block2x4-06.jpg)

26. Вийдіть з ескізу, виберіть його й застосуйте <img class="ic" src="icons/pocket.svg" alt="" data-no-zoom>**Виріз** (Pocket) глибиною **12 мм**. Натисніть **ОК**.

    ![Виріз глибиною 12 мм](block2x4-07.jpg)

    ![Результат: вигляд знизу](block2x4-08.jpg)

### 4. Матеріал і колір

27. Виберіть <img class="ic" src="icons/body.svg" alt="" data-no-zoom>**Тіло** в лівій панелі, перейдіть на вкладку **Перегляд** і натисніть <img class="ic" src="icons/appearance.svg" alt="" data-no-zoom>**Appearance**.
28. Виберіть матеріал **Plastic**.
29. Ще раз натисніть <img class="ic" src="icons/appearance.svg" alt="" data-no-zoom>**Appearance**, виберіть **Колір дифузії** і задайте колір на свій смак. Натисніть **ОК**.

    ![Вибір кольору](block2x4-09.jpg)

30. Закрийте меню. Модель готова!

    ![Готовий блок 2×4](block2x4-10.jpg)

<div class="task">

**Здача.** Збережіть файл з назвою<br>
`Блок 2x4 Прізвище Клас.FCStd`

</div>
