#!/usr/bin/env python
import os
import sys

def main():
    """Запуск командной строки Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен "
            "и доступен в виртуальном окружении."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
