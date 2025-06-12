# Установка кодировки UTF-8 для корректного отображения кириллицы
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

Clear-Host

# Включаем строгую обработку ошибок
$ErrorActionPreference = "Stop"

# Путь к виртуальному окружению
$venvPath = ".\venv"

# Проверка: существует ли виртуальное окружение
if (!(Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Создание виртуального окружения..."
    python -m venv venv
}

# Активация виртуального окружения
Write-Host "Активация виртуального окружения..."
. "$venvPath\Scripts\Activate.ps1"

# Установка зависимостей
Write-Host "Установка необходимых библиотек..."
pip install Flask Flask-SQLAlchemy Flask-Login

# Создание базы данных (если файл init_db.py существует)
if (Test-Path ".\init_db.py") {
    Write-Host "Создание базы данных..."
    python init_db.py
}

# Запуск Flask-приложения (браузер откроется из app.py)
Write-Host "Запуск Flask-приложения..."
python app.py
