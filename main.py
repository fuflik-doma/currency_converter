import json
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests

# Настройки темы интерфейса
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CurrencyConverterApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Константы (ЗАМЕНИТЕ НА СВОЙ КЛЮЧ)
        self.API_KEY = "ВАШ_API_КЛЮЧ_СЮДА"
        self.HISTORY_FILE = "history.json"
        self.CURRENCIES = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "CAD"]

        # Настройка окна
        self.title("Currency Converter")
        self.geometry("500x600")
        self.resizable(False, False)

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Конвертер валют", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_title.pack(pady=20)

        # Выбор валюты "Из"
        self.label_from = ctk.CTkLabel(self, text="Из валюты:")
        self.label_from.pack(pady=2)
        self.combo_from = ctk.CTkComboBox(self, values=self.CURRENCIES)
        self.combo_from.pack(pady=5)
        self.combo_from.set("USD")

        # Выбор валюты "В"
        self.label_to = ctk.CTkLabel(self, text="В валюту:")
        self.label_to.pack(pady=2)
        self.combo_to = ctk.CTkComboBox(self, values=self.CURRENCIES)
        self.combo_to.pack(pady=5)
        self.combo_to.set("RUB")

        # Поле ввода суммы
        self.label_amount = ctk.CTkLabel(self, text="Сумма:")
        self.label_amount.pack(pady=2)
        self.entry_amount = ctk.CTkEntry(
            self, placeholder_text="Введите число..."
        )
        self.entry_amount.pack(pady=5)

        # Кнопка конвертации
        self.btn_convert = ctk.CTkButton(
            self, text="Конвертировать", command=self.convert_currency
        )
        self.btn_convert.pack(pady=15)

        # Поле вывода результата
        self.label_result = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_result.pack(pady=10)

        # Таблица истории (Список)
        self.label_history = ctk.CTkLabel(self, text="История запросов:")
        self.label_history.pack(pady=5)

        self.history_listbox = tk.Listbox(
            self,
            bg="#333333",
            fg="white",
            selectbackground="#1f538d",
            font=("Arial", 11),
        )
        self.history_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    def convert_currency(self):
        from_curr = self.combo_from.get()
        to_curr = self.combo_to.get()
        amount_str = self.entry_amount.get()

        # Валидация ввода
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Сумма должна быть положительным числом!"
            )
            return

        # Запрос к API
        url = (
            f"https://exchangerate-api.com{self.API_KEY}/pair/"
            f"{from_curr}/{to_curr}/{amount}"
        )

        try:
            response = requests.get(url)
            data = response.json()

            if data["result"] == "success":
                result = round(data["conversion_result"], 2)
                result_text = f"{amount} {from_curr} = {result} {to_curr}"

                # Вывод результата
                self.label_result.configure(text=result_text)

                # Сохранение в историю
                self.save_to_history(result_text)
            else:
                messagebox.showerror(
                    "Ошибка API", "Не удалось получить курс валют."
                )
        except Exception as e:
            messagebox.showerror(
                "Ошибка сети", "Проверьте подключение к интернету."
            )

    def save_to_history(self, record):
        # Добавляем наверх визуального списка
        self.history_listbox.insert(0, record)

        # Читаем старый файл, добавляем запись и сохраняем
        history_data = []
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history_data = json.load(f)
                except json.JSONDecodeError:
                    pass

        history_data.insert(0, record)

        with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history_data = json.load(f)
                    for record in history_data:
                        self.history_listbox.insert(tk.END, record)
                except json.JSONDecodeError:
                    pass


if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
