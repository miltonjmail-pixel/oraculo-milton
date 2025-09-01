import os
import pytest
from utils.validar_json import cargar_json_seguro

def test_json_valido(tmp_path):
    archivo = tmp_path / "valido.json"
    archivo.write_text('{"clave": "valor"}', encoding="utf-8")
    resultado = cargar_json_seguro(str(archivo))
    assert resultado == {"clave": "valor"}

def test_json_malformado(tmp_path):
    archivo = tmp_path / "malformado.json"
    archivo.write_text('{"clave": "valor"', encoding="utf-8")  # Falta cierre
    resultado = cargar_json_seguro(str(archivo))
    assert resultado is None

def test_archivo_inexistente():
    resultado = cargar_json_seguro("ruta/falsa.json")
    assert resultado is None
