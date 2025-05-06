## Podstawa dla projektu PZ2

Ten projekt jest podstawą, od której należy wyjść przy realizacji projektu PZ2.

Aby zainstalować wymagane biblioteki, stwórz nowe środowisko wirtualne, 
poprzez uruchomienie wewnątrz katalogu projektu:

```bash
python -m venv .venv
```

Następnie aktywuj to środowisko
```bash
./venv/Scripts/activate.bat
```

I zainstaluj wymagane do poprawnego działania paczki:
```bash
pip install -r ./requirements.txt
```

Możesz sprawdzić czy wszystko działa poprzez uruchomienie testów automatycznych:
```bash
python -m pytest
```

W razie wystąpienia problemów proszę o kontakt mailowy.