# Название проекта

Проект для теста bff и grpc.

## Задачи: 
 1. Проверить возможность типизации и стандартизации коммуникации между сервисами.

    **Результат**:
    
    типизация между grpc <--> fastapi удобна на основе protobuff.
    
    Типизация для frontend <--> fastapi не удобна на основе protobuff. Также попробовал генерацию из openapi от fastapi для формализации rest контрактов это более удобный и успешный вариант.
 2. Проверить возможность live разработки фронтенд с интеграцией в бекенда.

    **Результат**:

    Такая возможность есть на основе связки ts <--> vite <--> fastapi с написанием кастомного плагина для jira2 и конфигурирование файлов. Работает стабильно.
    
    Возможно доработка в виде добавления перезагрузки fastapi при изменениях файлов `*.py`. Тк в текущей конфигурации перезагружаются только файлы от `.js`.

 3. На сколько удобно разрабатывать grpc и поддерживать в актуальном состоянии архитектуры на grpc сервисах.

    **Результат**:
    
    Было попробаванно много разных систем генерации кода для синхронизации контрактов сервисов. В итоге хорошо себя показал генератор на основе betterproto с опцией pydantic. Как плюс генерируют сразу асинхронные метода для сервисов. Минусы генерять через `<name>/__init__.py`, код ложат в `__init__.py`. 
    
    Тк использованны `dataclass` из pydantic это дало возможность сразу описывать эндпоинты (rest) на основе этих данных. Это дало возможность напрямую формировать контракты для ts и поддерживать их в актульном состоянии.
    
    Также была попытка на реализации на основе ws, но она очень плохо себя показала, тк ws не описываются через openapi что тянет за сабой описание в ручную данных типов и контрактов.

## Установка

make install

## Использование

- Генерация конрактов 
    ```bash
    python cli.py
    ```
### Запуск fullstack
- Запуск ```cd frontend && npn run dev``` запускает dev сервер vite.
- Запуск ```cd backand && python app.py``` запускает dev сервер fastapi.
- Запуск ```cd backand && python echo_grpc.py``` запускает тестовый grpc сервис.
- Запуск ```cd backand && python echo_grpc_with_unix_socket.py``` запускает тестовый grpc сервис через сокет.
- Опционально ```python cli.py --wath ``` запуск программы для автогенерации контрактов при изменении сервиса.  
