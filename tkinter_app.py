import tkinter as tk


def on_submit():
    user_input = entry.get().strip()
    if user_input:
        result_label.config(text=f"You entered: {user_input}")
    else:
        result_label.config(text="Please enter some text.")


# Main window
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("400x200")
root.resizable(False, False)

# Input label
input_label = tk.Label(root, text="Enter text:", font=("Arial", 12))
input_label.pack(pady=(20, 5))

# Input box
entry = tk.Entry(root, width=35, font=("Arial", 12))
entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=on_submit)
submit_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
result_label.pack(pady=5)

root.mainloop()
