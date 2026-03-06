Установка
Подключите jQuery:

html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
Подключите плагин:

html
<script src="js/jquery.trackcoords.js"></script>
Быстрый старт
javascript
// Базовая инициализация
$("#trackBox").trackCoords({
    url: '/save.php'
});

// С пользовательскими настройками
$("#trackBox").trackCoords({
    checkInterval: 50,    // проверка каждые 50мс
    sendInterval: 2000,   // отправка каждые 2 секунды
    url: '/api/track'
});
Настройки
Параметр	Тип	По умолчанию	Описание
checkInterval	number	30	Период сбора данных (мс)
sendInterval	number	3000	Период отправки данных (мс)
url	string	'/save.php'	URL для отправки данных
Формат данных
json
[
  {
    "x": 150,
    "y": 75,
    "time": 120
  },
  {
    "x": 151,
    "y": 76,
    "time": 90
  }
]
x, y - координаты относительно элемента

time - время в миллисекундах

API методы
После инициализации плагин доступен через data():

javascript
var plugin = $("#element").data('trackCoords');

// Остановить отслеживание
plugin.stop();

// Получить собранные данные
var data = plugin.getData();

// Получить настройки
var settings = plugin.settings;

// Доступ к массиву данных
var mouseData = plugin.mouseData;