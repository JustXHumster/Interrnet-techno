(function($) {
    $.fn.trackCoords = function(options) {
        // Настройки по умолчанию
        var settings = $.extend({
            checkInterval: 30,
            sendInterval: 3000,
            url: '/save.php'
        }, options);

        return this.each(function() {
            var $element = $(this);
            var mouseData = [];
            var lastX = null;
            var lastY = null;
            var timeInPosition = 0;
            var tracking = true;
            
            // Функция отслеживания мыши
            function onMouseMove(e) {
                if (!tracking) return;
                
                // Получаем координаты относительно элемента
                var offset = $element.offset();
                var x = Math.round(e.pageX - offset.left);
                var y = Math.round(e.pageY - offset.top);
                
                // Проверяем, что курсор внутри элемента
                if (x >= 0 && x <= $element.width() && y >= 0 && y <= $element.height()) {
                    
                    // Если позиция изменилась
                    if (lastX !== x || lastY !== y) {
                        // Сохраняем предыдущую позицию
                        if (lastX !== null && timeInPosition > 0) {
                            mouseData.push({
                                x: lastX,
                                y: lastY,
                                time: timeInPosition
                            });
                            console.log('Сохранена позиция:', lastX, lastY, 'время:', timeInPosition);
                        }
                        
                        // Новая позиция
                        lastX = x;
                        lastY = y;
                        timeInPosition = settings.checkInterval;
                    } else {
                        // Та же позиция - увеличиваем время
                        timeInPosition += settings.checkInterval;
                    }
                } else {
                    // Курсор вне элемента
                    if (lastX !== null && timeInPosition > 0) {
                        mouseData.push({
                            x: lastX,
                            y: lastY,
                            time: timeInPosition
                        });
                        console.log('Курсор вышел, сохранено:', lastX, lastY, 'время:', timeInPosition);
                        
                        lastX = null;
                        lastY = null;
                        timeInPosition = 0;
                    }
                }
            }
            
            // Функция отправки данных
            function sendDataToServer() {
                if (!tracking) return;
                
                // Добавляем текущую позицию если есть
                if (lastX !== null && timeInPosition > 0) {
                    mouseData.push({
                        x: lastX,
                        y: lastY,
                        time: timeInPosition
                    });
                    timeInPosition = 0;
                }
                
                // Отправляем если есть данные
                if (mouseData.length > 0) {
                    var dataToSend = mouseData.slice();
                    
                    console.log('📤 Отправка данных:', dataToSend);
                    
                    $.ajax({
                        url: settings.url,
                        type: 'POST',
                        data: JSON.stringify(dataToSend),
                        contentType: 'application/json',
                        success: function(response) {
                            console.log('✅ Данные отправлены успешно');
                        },
                        error: function(xhr, status, error) {
                            console.log('⚠️ Данные не отправлены (эмуляция):', dataToSend);
                            console.log('   URL:', settings.url);
                        }
                    });
                    
                    // Очищаем отправленные данные
                    mouseData = [];
                }
            }
            
            // Навешиваем обработчики
            $element.on('mousemove', onMouseMove);
            
            // Запускаем интервал отправки
            var intervalId = setInterval(sendDataToServer, settings.sendInterval);
            
            // Сохраняем данные для внешнего доступа
            $element.data('trackCoords', {
                mouseData: mouseData,
                stop: function() {
                    tracking = false;
                    $element.off('mousemove', onMouseMove);
                    clearInterval(intervalId);
                    console.log('🛑 Отслеживание остановлено');
                },
                getData: function() {
                    return mouseData;
                }
            });
            
            console.log('✅ Плагин запущен на элементе', $element);
        });
    };
})(jQuery);