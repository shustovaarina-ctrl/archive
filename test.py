import pet
import pandas as pd
# Это наш первый простой тест, проверим самые важные шаги выполнения кода
def test_build_table_basic():
    # Выполняем
    df = pet.build_table(2026, ["Грузия"])

    # Проверяем, что создан DataFrame
    assert isinstance(df, pd.DataFrame)

    # Проверяем наличие базовых колонок
    assert "Country" in df.columns
    assert "MPID" in df.columns

    # Проверяем, что есть хотя бы одна строка
    assert len(df) > 0


