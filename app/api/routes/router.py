from fastapi import APIRouter
import pkgutil
import importlib
import sys
import pathlib

# Добавляем корневую директорию в sys.path (на случай запуска без пакета)
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))


class MainRouter:
    def __init__(self, prefix: str = "/api"):
        """Инициализация главного роутера с автоподключением маршрутов"""
        self.router = APIRouter(prefix=prefix)
        self._load_routes()

    def _load_routes(self):
        """Автоматически находит и подключает все модули с роутами"""
        package_name = "app.api.routes"

        # Перебираем все файлы в папке routes (кроме __init__.py и router.py)
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            if module_name not in ["router"]:  # Исключаем сам `router.py`
                module = importlib.import_module(f"{package_name}.{module_name}")

                # Если в модуле есть `router`, подключаем его
                if hasattr(module, "router"):
                    # Если у роутера нет тегов, добавляем автоматически
                    router_tags = getattr(module.router, 'tags', None) or [module_name.capitalize()]
                    self.router.include_router(
                        module.router, 
                        prefix=f"/{module_name}", 
                        tags=router_tags
                    )


# Создаем главный роутер
main_router = MainRouter().router