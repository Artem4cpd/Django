import tkinter as tk
from tkinter import messagebox
import secrets
import string


def generate():
    try:
        length = int(entry_length.get())
        if length < 4:
            messagebox.showwarning("Ошибка", "Минимум 4 символа!")
            return

        # Набор символов: буквы (верхний/нижний регистр) + цифры + спецсимволы
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(chars) for _ in range(length))

        entry_pass.delete(0, tk.END)
        entry_pass.insert(0, password)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число!")


def copy_to_clipboard():
    password = entry_pass.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Готово", "Пароль скопирован в буфер обмена!")
    else:
        messagebox.showwarning("Внимание", "Сначала создайте пароль")


# Создание окна
root = tk.Tk()
root.title("GenPass v1.1")
root.geometry("350x250")
root.resizable(False, False)

# Интерфейс
tk.Label(root, text="Длина пароля:", font=("Arial", 10)).pack(pady=5)
entry_length = tk.Entry(root, justify='center', width=10)
entry_length.insert(0, "16")
entry_length.pack()

# Кнопка генерации
btn_gen = tk.Button(root, text="Сгенерировать", command=generate,
                    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_gen.pack(pady=10, ipadx=10)

# Поле с паролем
entry_pass = tk.Entry(root, font=("Courier New", 12), justify='center', width=30)
entry_pass.pack(pady=5, padx=20)

# Кнопка копирования
btn_copy = tk.Button(root, text="Копировать в буфер", command=copy_to_clipboard,
                     bg="#2196F3", fg="white")
btn_copy.pack(pady=10)

root.mainloop()