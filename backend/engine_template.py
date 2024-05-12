from pathlib import Path
from fastapi.templating import Jinja2Templates as Base
from jinja2 import Environment


class Jinja2Templates(Base):
    def load_assets(self, asset: str, endpoint = 'index.js')->str:
        asset_bundle = f"http://localhost:5173/{asset}"
        if endpoint:
            asset_bundle +=  f"/{endpoint}"
        return asset_bundle 

    def _setup_env_defaults(self, env: Environment) -> None:
        super()._setup_env_defaults(env)
        env.filters['asset'] = self.load_assets

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
