"""
Модуль сохранения и загрузки данных коллекции курсов в JSON.
"""
import json
import os
from typing import List, Dict, Any

# Получаем путь к папке, где находится этот файл (lab07/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def save_to_json(data: List[Dict[str, Any]], filepath: str = None) -> None:
    """
    Сохраняет список словарей с данными курсов в JSON-файл.
    
    Args:
        data: список словарей с атрибутами курсов
        filepath: путь к файлу сохранения (по умолчанию в lab07/)
    """
    if filepath is None:
        filepath = os.path.join(BASE_DIR, "courses_data.json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_from_json(filepath: str = None) -> List[Dict[str, Any]]:
    """
    Загружает данные курсов из JSON-файла.
    
    Args:
        filepath: путь к файлу загрузки (по умолчанию из lab07/)
        
    Returns:
        список словарей с атрибутами курсов
    """
    if filepath is None:
        filepath = os.path.join(BASE_DIR, "courses_data.json")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []