import subprocess

from pydantic import BaseModel
from pathlib import Path

from watchdog.events import FileSystemEvent, PatternMatchingEventHandler, FileOpenedEvent

class GenerateInterfaceConfig(BaseModel):
    frontend_dir: Path
    frontend_output_dir: Path
    node_modules_dir: Path
    openapi_endpoint: str
    
    @property
    def cmd_openapi_ts(self)->Path:
        cmd_openapi_ts = self.node_modules_dir / '.bin/' / 'openapi-ts'
        return cmd_openapi_ts.resolve()

async def generate_client_interface(dev_config: GenerateInterfaceConfig):
    cmd = f'cd {dev_config.frontend_dir}'
    cmd += f'&& {dev_config.cmd_openapi_ts} --input {dev_config.openapi_endpoint} --output {dev_config.frontend_output_dir} --client axios -d'
    print(cmd)
    subprocess.run(cmd, shell=True)


class InterfaceHandler(PatternMatchingEventHandler):
    def __init__(self,*, callback_func, target_events: list,  patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.target_events = target_events
        self.callback_func = callback_func

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.__class__ in self.target_events:
            self.callback_func()
