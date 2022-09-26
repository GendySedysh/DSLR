# DSLR
Классификация с помощью логической регрессии

# Использование
python.exe .\describe.py .\datasets\dataset_train.csv - покажет статистику по датасету и создаст папку describe с датасетами по разным параметрам

python.exe .\histogram.py - создаст папку с гистограммами для анализа данных

python.exe .\scatter_plot.py - создаст папку с точечными графиками для анализа данных

python.exe .\pair_plot.py- создаст большой график с данными из предыдущих двух команд

python.exe .\logreg_train.py .\datasets\dataset_train.csv - обучит модель и сохранит данные в weights.csv. Данные будут разбиты на обучающие и тестовые для валидации точности модели.

python.exe .\logreg_predict.py .\datasets\dataset_test.csv .\weights.csv - создаст файл houses.csv в котором будут сохранены предсказанные классы из тестовых данных.
