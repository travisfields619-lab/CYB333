import tkinter as tk


def show_result() -> None:
    user_text = input_entry.get().strip()
    if user_text:
        result_label.config(text=f"You entered: {user_text}")
    else:
        result_label.config(text="Please enter some text.")


root = tk.Tk()
root.title("Simple Tkinter Window")
root.geometry("360x180")
root.resizable(False, False)

title_label = tk.Label(root, text="Enter text below:")
title_label.pack(pady=(20, 10))

input_entry = tk.Entry(root, width=30)
input_entry.pack(pady=5)

submit_button = tk.Button(root, text="Show Result", command=show_result)
submit_button.pack(pady=10)

result_label = tk.Label(root, text="Result will appear here.")
result_label.pack(pady=10)

root.mainloop()
