import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tabulate import tabulate

# Налаштування для відображення
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)


class StudentDataAnalyzer:
    """Клас для аналізу даних студентів з використанням Pandas"""

    def __init__(self, group_name="ІПЗ-31"):
        self.group_name = group_name
        self.df = None
        self.subjects = ['Математика', 'Фізика', 'Програмування', 'Англійська', 'Історія']

    def create_from_dicts(self, students_data):
        """
        Створює DataFrame зі списку словників.
        students_data - список словників з ключами 'first_name', 'last_name' та оцінками
        """
        data = []
        for student in students_data:
            row = {
                'Ім\'я': student['first_name'],
                'Прізвище': student['last_name']
            }
            # Додаємо оцінки
            for subject, grade in student['grades'].items():
                row[subject] = grade
            data.append(row)

        self.df = pd.DataFrame(data)
        print(f"DataFrame створено, розмір: {self.df.shape}")
        return self.df

    def create_from_lists(self, names, last_names, grades_matrix):
        """
        Створює DataFrame зі списків імен та матриці оцінок.
        """
        data = {
            'Ім\'я': names,
            'Прізвище': last_names
        }
        for i, subject in enumerate(self.subjects):
            data[subject] = [grades[j][i] for j in range(len(grades_matrix))]

        self.df = pd.DataFrame(data)
        return self.df

    def load_from_csv(self, filename):
        """Завантажує дані з CSV файлу"""
        try:
            self.df = pd.read_csv(filename, encoding='utf-8')
            print(f"Дані завантажено з {filename}")
            print(f"Розмір: {self.df.shape}")
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено")
            return False
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return False

    def save_to_csv(self, filename):
        """Зберігає дані у CSV файл"""
        if self.df is not None:
            self.df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Дані збережено у {filename}")
            return True
        else:
            print("Немає даних для збереження")
            return False

    def save_to_excel(self, filename):
        """Зберігає дані у Excel файл"""
        if self.df is not None:
            self.df.to_excel(filename, index=False)
            print(f"Дані збережено у {filename}")
            return True
        else:
            print("Немає даних для збереження")
            return False

    def calculate_student_averages(self):
        """Додає стовпець із середнім балом кожного студента"""
        if self.df is not None:
            self.df['Середній бал'] = self.df[self.subjects].mean(axis=1).round(2)
            return self.df[['Ім\'я', 'Прізвище', 'Середній бал']]
        return None

    def get_subject_averages(self):
        """Обчислює середній бал групи з кожного предмету"""
        if self.df is not None:
            return self.df[self.subjects].mean().round(2)
        return None

    def get_subject_stats(self):
        """Отримує статистику по предметах"""
        if self.df is not None:
            stats = self.df[self.subjects].agg(['min', 'max', 'mean', 'median', 'std']).round(2)
            return stats
        return None

    def get_top_students(self, n=3):
        """Повертає n найкращих студентів"""
        if self.df is not None:
            if 'Середній бал' not in self.df.columns:
                self.calculate_student_averages()
            return self.df.nlargest(n, 'Середній бал')[['Ім\'я', 'Прізвище', 'Середній бал']]
        return None

    def filter_by_grade(self, subject, min_grade=80):
        """Фільтрує студентів за оцінкою з предмету"""
        if self.df is not None:
            filtered = self.df[self.df[subject] >= min_grade]
            return filtered[['Ім\'я', 'Прізвище', subject]]
        return None

    def get_grade_distribution(self, subject):
        """Отримує розподіл оцінок з предмету"""
        if self.df is not None:
            return self.df[subject].value_counts().sort_index()
        return None

    def add_grade_column(self, subject, grades):
        """Додає новий стовпець з оцінками"""
        if self.df is not None and len(grades) == len(self.df):
            self.df[subject] = grades
            if subject not in self.subjects:
                self.subjects.append(subject)
            return True
        return False

    def remove_student(self, index):
        """Видаляє студента за індексом"""
        if self.df is not None and 0 <= index < len(self.df):
            self.df = self.df.drop(index).reset_index(drop=True)
            return True
        return False

    def display_table(self):
        """Виводить таблицю з даними"""
        if self.df is None:
            print("Немає даних")
            return

        print("\n" + "=" * 100)
        print(f"ГРУПА: {self.group_name}")
        print("=" * 100)

        # Підготовка даних для відображення
        display_df = self.df.copy()
        if 'Середній бал' not in display_df.columns:
            display_df['Середній бал'] = display_df[self.subjects].mean(axis=1).round(2)

        # Виведення в гарному форматі
        print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
        print("=" * 100)

    def plot_grade_distribution(self, subject):
        """Будує гістограму розподілу оцінок з предмету"""
        if self.df is not None and subject in self.df.columns:
            plt.figure(figsize=(10, 6))
            self.df[subject].plot(kind='hist', bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title(f'Розподіл оцінок з предмету {subject}')
            plt.xlabel('Оцінка')
            plt.ylabel('Кількість студентів')
            plt.grid(True, alpha=0.3)
            plt.show()
        else:
            print(f"Предмет {subject} не знайдено")

    def plot_student_comparison(self):
        """Будує порівняльну діаграму середніх балів студентів"""
        if self.df is not None:
            if 'Середній бал' not in self.df.columns:
                self.calculate_student_averages()

            plt.figure(figsize=(12, 6))
            students = self.df['Ім\'я'] + ' ' + self.df['Прізвище']
            plt.bar(students, self.df['Середній бал'], color='lightcoral')
            plt.axhline(y=self.df['Середній бал'].mean(), color='red', linestyle='--',
                        label=f'Середній по групі: {self.df["Середній бал"].mean():.2f}')
            plt.title('Середні бали студентів')
            plt.xlabel('Студент')
            plt.ylabel('Середній бал')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()


def create_demo_data():
    """Створює демонстраційні дані"""
    students = [
        {'first_name': 'Анастасія', 'last_name': 'Дишлюк',
         'grades': {'Математика': 90, 'Фізика': 85, 'Програмування': 88, 'Англійська': 92, 'Історія': 87}},
        {'first_name': 'Іван', 'last_name': 'Петренко',
         'grades': {'Математика': 78, 'Фізика': 82, 'Програмування': 80, 'Англійська': 75, 'Історія': 85}},
        {'first_name': 'Олена', 'last_name': 'Іваненко',
         'grades': {'Математика': 95, 'Фізика': 92, 'Програмування': 94, 'Англійська': 96, 'Історія': 93}},
        {'first_name': 'Петро', 'last_name': 'Коваленко',
         'grades': {'Математика': 82, 'Фізика': 79, 'Програмування': 85, 'Англійська': 88, 'Історія': 84}},
        {'first_name': 'Марія', 'last_name': 'Шевченко',
         'grades': {'Математика': 91, 'Фізика': 94, 'Програмування': 89, 'Англійська': 93, 'Історія': 90}},
        {'first_name': 'Андрій', 'last_name': 'Мельник',
         'grades': {'Математика': 76, 'Фізика': 81, 'Програмування': 79, 'Англійська': 84, 'Історія': 82}},
        {'first_name': 'Юлія', 'last_name': 'Кравчук',
         'grades': {'Математика': 94, 'Фізика': 90, 'Програмування': 92, 'Англійська': 89, 'Історія': 95}},
        {'first_name': 'Тарас', 'last_name': 'Шевченко',
         'grades': {'Математика': 88, 'Фізика': 87, 'Програмування': 86, 'Англійська': 91, 'Історія': 89}},
    ]
    return students


def main():
    """Головна функція програми"""
    print("=" * 100)
    print("РОБОТА З ТАБЛИЧНИМИ ДАНИМИ ВИКОРИСТОВУЮЧИ PANDAS")
    print("=" * 100)

    # Створення об'єкта аналізатора
    analyzer = StudentDataAnalyzer("ІПЗ-31")

    # Створення даних
    students_data = create_demo_data()
    analyzer.create_from_dicts(students_data)

    # 1. Збереження у CSV
    print("\n1. ЗБЕРЕЖЕННЯ ДАНИХ У CSV")
    analyzer.save_to_csv("students_pandas.csv")

    # 2. Обчислення середніх балів
    print("\n2. СЕРЕДНІ БАЛИ СТУДЕНТІВ")
    student_averages = analyzer.calculate_student_averages()
    print(tabulate(student_averages, headers='keys', tablefmt='simple', showindex=False))

    # 3. Середні бали по предметах
    print("\n3. СЕРЕДНІ БАЛИ ГРУПИ З ПРЕДМЕТІВ")
    subject_averages = analyzer.get_subject_averages()
    for subject, avg in subject_averages.items():
        print(f"  {subject}: {avg:.2f}")

    # 4. Детальна статистика
    print("\n4. ДЕТАЛЬНА СТАТИСТИКА ПО ПРЕДМЕТАХ")
    stats = analyzer.get_subject_stats()
    print(tabulate(stats, headers='keys', tablefmt='simple'))

    # 5. ТОП студентів
    print("\n5. ТОП-3 СТУДЕНТИ")
    top_students = analyzer.get_top_students(3)
    print(tabulate(top_students, headers='keys', tablefmt='simple', showindex=False))

    # 6. Фільтрація за оцінкою
    print("\n6. СТУДЕНТИ З ОЦІНКОЮ З ПРОГРАМУВАННЯ >= 85")
    filtered = analyzer.filter_by_grade('Програмування', 85)
    print(tabulate(filtered, headers='keys', tablefmt='simple', showindex=False))

    # 7. Розподіл оцінок
    print("\n7. РОЗПОДІЛ ОЦІНОК З МАТЕМАТИКИ")
    distribution = analyzer.get_grade_distribution('Математика')
    for grade, count in distribution.items():
        print(f"  Оцінка {grade}: {count} студентів")

    # 8. Виведення повної таблиці
    print("\n8. ПОВНА ТАБЛИЦЯ ДАНИХ")
    analyzer.display_table()

    # 9. Додавання нового стовпця
    print("\n9. ДОДАВАННЯ НОВОГО ПРЕДМЕТУ")
    new_grades = [95, 88, 97, 91, 94, 85, 98, 90]
    analyzer.add_grade_column('Філософія', new_grades)
    print("Додано предмет 'Філософія'")
    analyzer.display_table()

    # 10. Експорт у різні формати
    print("\n10. ЕКСПОРТ У РІЗНІ ФОРМАТИ")
    analyzer.save_to_excel("students_pandas.xlsx")
    analyzer.save_to_csv("students_pandas_final.csv")

    # 11. Групування та агрегація
    print("\n11. ГРУПУВАННЯ ТА АГРЕГАЦІЯ")
    # Додамо умовну категорію "Відмінники"
    analyzer.df['Відмінник'] = analyzer.df['Середній бал'] >= 90
    grouped = analyzer.df.groupby('Відмінник')[analyzer.subjects].mean().round(2)
    print("Середні бали за групами (відмінники / не відмінники):")
    print(tabulate(grouped, headers='keys', tablefmt='simple'))

    # 12. Кореляція між предметами
    print("\n12. КОРЕЛЯЦІЯ МІЖ ПРЕДМЕТАМИ")
    correlation = analyzer.df[analyzer.subjects].corr().round(2)
    print("Матриця кореляції:")
    print(tabulate(correlation, headers='keys', tablefmt='simple'))

    # Побудова графіків (за бажанням)
    plot_choice = input("\nПобудувати графіки? (так/ні): ").lower()
    if plot_choice in ['так', 'т', 'yes', 'y']:
        analyzer.plot_grade_distribution('Програмування')
        analyzer.plot_student_comparison()


if __name__ == "__main__":
    main()

    # Додаткова демонстрація: завантаження з файлу
    print("\n" + "=" * 100)
    print("ДЕМОНСТРАЦІЯ ЗАВАНТАЖЕННЯ З CSV")
    print("=" * 100)

    new_analyzer = StudentDataAnalyzer("ІПЗ-31 (з файлу)")
    if new_analyzer.load_from_csv("students_pandas_final.csv"):
        new_analyzer.display_table()