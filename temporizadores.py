import tkinter as tk
from tkinter import messagebox, simpledialog
from plyer import notification
import json
import os

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.remaining = duration
        self.is_running = False

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Controlador de Tiempo")
        self.timers = []
        self.load_history()

        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack()

        self.label = tk.Label(self.main_frame, text="Tiempo en segundos:")
        self.label.grid(row=0, column=0)

        self.entry = tk.Entry(self.main_frame, width=20)
        self.entry.grid(row=0, column=1)

        self.start_button = tk.Button(self.main_frame, text="Iniciar", command=self.start_timer)
        self.start_button.grid(row=1, column=0, pady=(10, 0))

        self.stop_button = tk.Button(self.main_frame, text="Detener Todos", command=self.stop_all_timers, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, pady=(10, 0))

        self.history_button = tk.Button(self.main_frame, text="Historial", command=self.show_history)
        self.history_button.grid(row=2, columnspan=2, pady=(10, 0))

        self.timer_label = tk.Label(self.main_frame, text="", font=("Helvetica", 24))
        self.timer_label.grid(row=3, columnspan=2, pady=(10, 0))

    def start_timer(self):
        try:
            duration = int(self.entry.get())
            if duration <= 0:
                raise ValueError
            timer = Timer(duration)
            timer.is_running = True
            self.timers.append(timer)
            self.timer_label.config(text=f"Temporizador: {duration} segundos")
            self.entry.delete(0, tk.END)
            self.stop_button.config(state=tk.NORMAL)
            self.update_timers()
            self.save_history()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

    def update_timers(self):
        for timer in self.timers:
            if timer.is_running:
                if timer.remaining > 0:
                    timer.remaining -= 1
                    self.timer_label.config(text=f"Temporizador: {timer.remaining} segundos")
                else:
                    timer.is_running = False
                    self.send_notification()
                    self.timer_label.config(text="¡Tiempo agotado!")
        self.master.after(1000, self.update_timers)

    def send_notification(self):
        message = simpledialog.askstring("Notificación", "Ingrese un mensaje:")
        if message:
            notification.notify(
                title="Temporizador",
                message=message,
                app_name="Controlador de Tiempo",
                timeout=10
            )
        else:
            notification.notify(
                title="Temporizador",
                message="¡El tiempo ha terminado!",
                app_name="Controlador de Tiempo",
                timeout=10
            )

    def stop_all_timers(self):
        for timer in self.timers:
            timer.is_running = False
        self.stop_button.config(state=tk.DISABLED)

    def show_history(self):
        if not self.timers:
            messagebox.showinfo("Historial", "No hay temporizadores completados.")
            return
        history_str = "\n".join(f"{i+1}. {t.duration} segundos" for i, t in enumerate(self.timers) if not t.is_running)
        messagebox.showinfo("Historial de Temporizadores", history_str)

    def load_history(self):
        if os.path.exists("historial.json"):
            with open("historial.json", "r") as file:
                data = json.load(file)
                for duration in data:
                    self.timers.append(Timer(duration))

    def save_history(self):
        with open("historial.json", "w") as file:
            json.dump([timer.duration for timer in self.timers], file)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    app = TimerApp(root)
    root.mainloop()
