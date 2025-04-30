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
print(f"Największym odsetkiem znamion choroby psychicznej podczas interwencji charakteryzuje się rasa {most_mental_ill_race}")

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

print(report2)

