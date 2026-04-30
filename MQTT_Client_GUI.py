import tkinter as tk
from tkinter import filedialog, messagebox
from paho.mqtt import client as mqtt
from Heart_predictor import predict_heart
from datetime import datetime
import hashlib

# ---------------- GLOBAL VARIABLES ---------------- #
save_to_file = False
file_path = ""

# ---------------- MQTT FUNCTIONS ---------------- #

def publish_msg():
    ip = ip_entry.get()
    topic = topic_entry.get()
    msg = f"{gender_entry.get()},{age_entry.get()},{smoker_entry.get()},{cigs_entry.get()},{bpmeds_entry.get()},{stroke_entry.get()},{hyp_entry.get()},{diabetes_entry.get()},{chol_entry.get()},{sysbp_entry.get()},{diabp_entry.get()},{bmi_entry.get()},{heartrate_entry.get()},{glucose_entry.get()}"
    hash_value = hashlib.sha256(msg.encode()).hexdigest()
    final_message = msg + "|" + hash_value
    if not ip or not topic or not msg:
        messagebox.showerror("Error", "Please fill all required fields")
        return

    client = mqtt.Client()
    client.connect(ip, 1883)
    client.loop_start()
    client.publish(topic, final_message)

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    output_box.insert(tk.END, f"[{current_time}] Sent: {msg}\n")
    output_box.see(tk.END)

    status_label.config(text="✔ Message Sent", fg="#2e7d32")

def on_message(client, userdata, message):

    received = message.payload.decode()

    try:
        data_string, received_hash = received.split("|")
    except:
        data_string = received
        received_hash = ""

    # ---------- HASH CHECK ----------
    calculated_hash = hashlib.sha256(data_string.encode()).hexdigest()

    if calculated_hash == received_hash:
        auth_status = "Authentic Data"
    else:
        auth_status = "⚠ Not Authentic Data"

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    # ---------- AI PREDICTION ----------
    try:
        values = data_string.split(",")

        result = predict_heart(
            values[0],
            float(values[1]),
            values[2],
            float(values[3]),
            values[4],
            values[5],
            values[6],
            values[7],
            float(values[8]),
            float(values[9]),
            float(values[10]),
            float(values[11]),
            float(values[12]),
            float(values[13])
        )
    except:
        result = "Prediction Error (Invalid Input)"

    # ---------- DISPLAY ----------
    output_box.insert(tk.END, f"[{current_time}] Received: {data_string}\n")
    output_box.insert(tk.END, f"Prediction: {result}\n")
    output_box.insert(tk.END, f"Data Status: {auth_status}\n\n")

    output_box.see(tk.END)

    # ---------- SAVE ----------
    if save_to_file and file_path:
        with open(file_path, "a") as file:
            file.write(f"[{current_time}] Received: {data_string}\n")
            file.write(f"Prediction: {result}\n")
            file.write(f"Data Status: {auth_status}\n\n")

def subscribe_msg():
    ip = ip_entry.get()
    topic = topic_entry.get()

    if not ip or not topic:
        messagebox.showerror("Error", "Enter Broker IP and Topic")
        return

    client = mqtt.Client()
    client.connect(ip, 1883)
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_start()

    status_label.config(text="✔ Subscribed", fg="#1565c0")

# ---------------- FILE HANDLING ---------------- #

def toggle_file_saving():
    global save_to_file
    save_to_file = file_var.get()

def choose_file():
    global file_path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("Log Files", "*.log"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# ---------------- GUI DESIGN ---------------- #

root = tk.Tk()
root.title("MQTT Client GUI")
root.geometry("600x900")
root.configure(bg="#f4f6f8")

FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")

# ---------- HEADER ---------- #
header = tk.Label(
    root,
    text="MQTT Messaging Application",
    bg="#1e88e5",
    fg="white",
    font=("Segoe UI", 16, "bold"),
    pady=15
)
header.pack(fill="x")


# ---------- SCROLLABLE FRAME ---------- #

canvas = tk.Canvas(root, bg="#f4f6f8")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#f4f6f8")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

main_frame = scrollable_frame

def labeled_entry(parent, text):
    tk.Label(parent, text=text, bg="#f4f6f8", font=FONT_LABEL).pack(anchor="w")
    entry = tk.Entry(parent, font=FONT_ENTRY, width=45)
    entry.pack(pady=5)
    return entry

ip_entry = labeled_entry(main_frame, "Broker IP")
topic_entry = labeled_entry(main_frame, "Topic")

# ---------- FILE OPTIONS ---------- #
file_var = tk.BooleanVar()
tk.Checkbutton(
    main_frame,
    text="Save received messages to file",
    variable=file_var,
    command=toggle_file_saving,
    bg="#f4f6f8",
    font=FONT_LABEL
).pack(anchor="w", pady=10)

tk.Label(main_frame, text="File Location", bg="#f4f6f8", font=FONT_LABEL).pack(anchor="w")
file_entry = tk.Entry(main_frame, font=FONT_ENTRY, width=45)
file_entry.pack(pady=5)

tk.Button(
    main_frame,
    text="Browse",
    command=choose_file,
    bg="#e0e0e0",
    font=FONT_BTN,
    relief="flat",
    padx=10
).pack(pady=5)

# ---------- PATIENT DATA INPUT ---------- #

tk.Label(main_frame, text="Patient Data Input", bg="#f4f6f8", font=FONT_LABEL).pack(anchor="w", pady=10)

gender_entry = labeled_entry(main_frame, "Gender (male/female)")
age_entry = labeled_entry(main_frame, "Age")

smoker_entry = labeled_entry(main_frame, "Current Smoker (yes/no)")
cigs_entry = labeled_entry(main_frame, "Cigs Per Day")

bpmeds_entry = labeled_entry(main_frame, "BP Medicines (yes/no)")
stroke_entry = labeled_entry(main_frame, "Prevalent Stroke (yes/no)")
hyp_entry = labeled_entry(main_frame, "Hypertension (yes/no)")
diabetes_entry = labeled_entry(main_frame, "Diabetes (yes/no)")

chol_entry = labeled_entry(main_frame, "Total Cholesterol")
sysbp_entry = labeled_entry(main_frame, "Systolic BP")
diabp_entry = labeled_entry(main_frame, "Diastolic BP")

bmi_entry = labeled_entry(main_frame, "BMI")
heartrate_entry = labeled_entry(main_frame, "Heart Rate")
glucose_entry = labeled_entry(main_frame, "Glucose")

# ---------- BUTTONS ---------- #
btn_frame = tk.Frame(main_frame, bg="#f4f6f8")
btn_frame.pack(pady=15)

tk.Button(
    btn_frame,
    text="Subscribe",
    command=subscribe_msg,
    bg="#1e88e5",
    fg="white",
    font=FONT_BTN,
    padx=20,
    pady=8,
    relief="flat"
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="Publish",
    command=publish_msg,
    bg="#43a047",
    fg="white",
    font=FONT_BTN,
    padx=20,
    pady=8,
    relief="flat"
).grid(row=0, column=1, padx=10)

# ---------- OUTPUT ---------- #
tk.Label(main_frame, text="Received Messages", bg="#f4f6f8", font=FONT_LABEL).pack(anchor="w")

output_box = tk.Text(
    main_frame,
    height=10,
    font=("Consolas", 10),
    bd=1,
    relief="solid"
)
output_box.pack(fill="x", pady=5)

status_label = tk.Label(main_frame, text="", bg="#f4f6f8", font=FONT_LABEL)
status_label.pack(pady=5)

root.mainloop()
