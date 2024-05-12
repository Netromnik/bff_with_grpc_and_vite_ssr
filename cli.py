import typer
import asyncio
from watchdog.observers  import Observer 
from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileDeletedEvent

from cli_cmd.frontend_interface_generate import generate_client_interface, GenerateInterfaceConfig, InterfaceHandler
from pathlib import Path

app = typer.Typer()


@app.command(
        name='gents',
        short_help='генерация контрактов для frontend',
        help='Для работы нужен включенный fastapi instance',
)
def _tswath(
        frontend_dir: str = './frontend/',
        backend_dir: str = './backend/',
        frontend_output_dir: str = './frontend/back_interface_endpoint/',
        node_modules_dir: str = './frontend/node_modules/',
        openapi_endpoint: str = 'http://localhost:8000/openapi.json',
        watch: bool = False
        ):
    """
    $: python cli.py tswath --ts-conf "{\"frontend_dir\": \"test\"}"
    """
    ts_conf = GenerateInterfaceConfig(
        frontend_dir=Path(frontend_dir).resolve(),
        frontend_output_dir=Path(frontend_output_dir).resolve(),
        node_modules_dir=Path(node_modules_dir).resolve(),
        openapi_endpoint=openapi_endpoint,
    )

    def _wrap():
        print('runs')
        asyncio.run(generate_client_interface(ts_conf))
    
    if not watch:
        _wrap()
    else:
        event_handler = InterfaceHandler(
            patterns = ['*.py*'],
            ignore_patterns = ['cache/*'],
            ignore_directories = True,
            case_sensitive = False,
            callback_func= _wrap,
            target_events=[FileCreatedEvent, FileModifiedEvent, FileDeletedEvent]
        )
        observer = Observer()
        observer.schedule(event_handler, path=Path(backend_dir).resolve(), recursive=True)
        observer.start()
        print(f"Запушен wathdog {Path(backend_dir).resolve()}/**")
        observer.join()


if __name__ == "__main__":
    app()

