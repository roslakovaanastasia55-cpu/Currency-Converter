import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class CurrencyConventerApp:
    def __init__(self, root):
        self.root = root
        self.root.tittle("CurrencyConventer")
        self.root.geometry("600×500")

        # Выбор валюты "из"
        ttk.Label(root, text="From:").grid(row=0, column=0, padx=10, pady=10)
        self.from_currency = ttk.Combobox(root, values=[])
        self.from_currency.grid(row=0, column=1, padx=10, pady=10)

        # Выбор валюты "в"
        ttk.Label(root, text="To:").grid(row=1, column=0, padx=10, pady=10)
        self.to_currency = ttk.Combobox(root, values=[])
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)

        # Поле ввода суммы
        ttk.Label(root, text=Amount:").grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=3, column=0, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_btn = ttk.Button(root, text="Convert, command=self.convert_currency")
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=("From", "To", "Amount", "Result"), show="headings")
        self.history_tree.heading("From", text="From")
        self.history_tree.heading("To", text="To")
        self.history_tree.heading("Amount", text="Amount")
        self.history_tree.heading("Result". text="Result")
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Загрузка валют при запуске
        self.load_currencies()
        # Обновление таблицы истории
        self.update_history_table()
    
    def load_currencies(self):
        """"Загрузка списка валют из API""""
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = responce.json()
            currencies = list(data['rates'].keys())
            self.from_currency['values'] = currencies
            self.to_currency['values'] = currencies
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load currencies: {e}")

    def get_exchange_rate(self, from_curr, to_curr):
        """Получение курса обмена"""
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_curr}")
            data = responce.json()
            return data['rates'][to_curr]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get exchange rate: {e}")
            return None

    def save_history(self, history):
        with open("history.json", "w") as f:
            json.dump(history, f, indent=4)

    def load_history(self):
        try:
            with open("history.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        history = self.load_history()
        for record in history:
            self.history_tree.insert("", "end", values=(
                record["from"],
                record["to"],
                record["amount"],
                record["result"]
            ))

    def validate_input(self, amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be a positive number")
                return None
            return amount
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return None

    def convert_currency(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        amount_str = self.amount.entry.get()

        amount = self.validate_input(amount_str)
        if amount is None:
            return

        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return

        result = amount × rate

        history = self.load_history()
        history.append({
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": round(result, 2)
        })
        self.save_history(history)
        self.update_history_table()

        messagebox.showinfo("Result", F"{amount} {from_curr} = {round(result, 2 )} {to_curr}")

# Запуск приложения
if __name__ == "__main":
    root = tk.Tk()
    app = CurrencyConventerApp(root)
    root.mainloop()
