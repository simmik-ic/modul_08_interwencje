import pandas as pd
import matplotlib.pyplot as plt

#1
df = pd.read_csv('fatal-police-shootings-data.csv')

#2
report = df.pivot_table(values='id',index='race',columns='signs_of_mental_illness',aggfunc='count')

#3
def percentage(row):
    if row[True] + row[False] == 0:
        perc = 0
    else:
        perc = row[True] / (row[True] + row[False])
    return perc

report['percentage_of_signs_of_mental_illness_for_each_race'] = report.apply(lambda row: percentage(row),axis=1).round(4)

most_mental_ill_race = report['percentage_of_signs_of_mental_illness_for_each_race'].idxmax()
print(report)
print(f"Największym odsetkiem znamion choroby psychicznej podczas interwencji charakteryzuje się rasa {most_mental_ill_race}")   #biała

#4
#stwórz słownik dni tygodnia
weekdays_dict = dict(zip(range(0,7),['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']))

#dodaj kolumnę numeru dnia tygodnia
df['Weekday'] = pd.to_datetime(df['date']).dt.weekday
#stwórz tabelę przestawną
report2 = df.pivot_table(values='id',index='Weekday',aggfunc='count').rename(index=weekdays_dict)

#utwórz wykres kolumnowy
plt.figure(figsize=(10,6))
report2['id'].plot(kind='bar', color='skyblue', edgecolor='black')
ax = report2['id'].plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Liczba ofiar interwencji według dni tygodnia', fontsize=14)
plt.xlabel('Dni tygodnia', fontsize=12)
plt.ylabel('Liczba ofiar', fontsize=12)
ymax = report2['id'].max() * 1.2
plt.ylim(top=ymax)
for i, v in enumerate(report2['id']):
    ax.text(i, v + 10, str(v), ha='center', va='bottom', fontsize=10)
plt.xticks(rotation=45)  
plt.show()
#print(report2)

#5
#zaimportuj dane o populacji ze strony www
path = 'https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population'
df_population = pd.read_html(path, header=0)[0]
#wybierz odpowiednie kolumny i wiersze
report3 = df_population.iloc[:-4, [2,3]]

report3.columns = ['NAZWA STANU', 'LUDNOŚĆ']

#zaimportuj dane o skrótach ze strony www
path = 'https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations'
df_abbreviations = pd.read_html(path, header=0)[1].iloc[:, [0,5]].dropna().replace(r'\[.*?\]', '', regex=True)
#powyższa linia:
#sczytuje z podanej ścieżki drugą tabelę na stronie
#wybiera z niej wszystkie wiersze oraz kolumny 0 i 5
#usuwa wiersze z brakującymi danymi
#zamienia tekst w nawiasach kwadratowych (za pomocą wyrażenia regularnego) na pusty string

#przygotuj słownik skrótów nazw stanów
abbreviations = dict(zip(df_abbreviations.iloc[:, 0], df_abbreviations.iloc[:, 1] ))
#dodaj na drugim miejscu kolumnę z kodem stanu
report3.insert(1, 'KOD', report3['NAZWA STANU'].map(abbreviations))

#na podstawie oryginalnego df przygotuj słownik liczby interwencji według stanu
interventions = df.groupby('state')['id'].count().to_dict()
#dodaj do raportu kolumnę z liczbą interwencji w stanie, brakujące wartości uzupełnij jako 0, zmień typ na int
report3['INTERWENCJE'] = report3['KOD'].map(interventions).fillna(0).astype(int)

#funkcja do liczenia interwencji na 1000 mieszkańców
def int_per_1000_inh(row):
    if row['LUDNOŚĆ'] == 0:
        result = 0
    else:
        result = round(row['INTERWENCJE']*1000 / row['LUDNOŚĆ'], 3)
    return result

#dodaj do raportu kolumnę z liczbą interwencji na 1000 mieszkańców 
report3['NA 1000 MIESZK.'] = report3.apply(lambda row: int_per_1000_inh(row), axis=1)

#posortuj na miejscu po liczbie interwencji na 1000 mieszkańców
report3.sort_values(by='NA 1000 MIESZK.', ascending=False, inplace=True)
report3.reset_index(drop=True, inplace=True)
print(report3)