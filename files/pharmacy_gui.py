import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ✅ Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="snehitha",
        database="pharmacy_db"
    )

# ✅ Login Function
def login():
    username = entry_user.get()
    password = entry_pass.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))

    if cursor.fetchone():
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Credentials")

    conn.close()

# ✅ Open Dashboard
def open_dashboard():
    global dash
    dash = tk.Tk()
    dash.title("Pharmacy Management System")
    dash.geometry("600x400")

    ttk.Label(dash, text="Pharmacy Management", font=("Arial", 16)).pack(pady=10)

    ttk.Button(dash, text="Manage Medicines", command=manage_medicines).pack(pady=5)
    ttk.Button(dash, text="Exit", command=dash.quit).pack(pady=5)

    dash.mainloop()

# ✅ Manage Medicines Window
def manage_medicines():
    global med_name, med_qty, med_price, med_supplier, medicine_table

    med_win = tk.Toplevel()
    med_win.title("Medicine Management")
    med_win.geometry("700x500")

    ttk.Label(med_win, text="Manage Medicines", font=("Arial", 14)).pack(pady=10)

    # Input Fields
    ttk.Label(med_win, text="Name:").pack()
    med_name = ttk.Entry(med_win)
    med_name.pack()

    ttk.Label(med_win, text="Quantity:").pack()
    med_qty = ttk.Entry(med_win)
    med_qty.pack()

    ttk.Label(med_win, text="Price:").pack()
    med_price = ttk.Entry(med_win)
    med_price.pack()

    ttk.Label(med_win, text="Supplier:").pack()
    med_supplier = ttk.Entry(med_win)
    med_supplier.pack()

    # Buttons
    ttk.Button(med_win, text="Add Medicine", command=add_medicine).pack(pady=5)
    ttk.Button(med_win, text="Update Medicine", command=update_medicine).pack(pady=5)
    ttk.Button(med_win, text="Delete Medicine", command=delete_medicine).pack(pady=5)
    ttk.Button(med_win, text="Refresh", command=view_medicines).pack(pady=5)

    # Medicine Table
    cols = ("ID", "Name", "Quantity", "Price", "Supplier")
    medicine_table = ttk.Treeview(med_win, columns=cols, show="headings")
    for col in cols:
        medicine_table.heading(col, text=col)
    medicine_table.pack(fill="both", expand=True)

    view_medicines()

# ✅ Add Medicine
def add_medicine():
    name = med_name.get()
    qty = med_qty.get()
    price = med_price.get()
    supplier = med_supplier.get()

    if not name or not qty or not price or not supplier:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    try:
        qty = int(qty)
        price = float(price)  # ✅ Ensure price is a valid decimal
    except ValueError:
        messagebox.showwarning("Warning", "Quantity must be an integer and Price must be a number!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicines (name, quantity, price, supplier) VALUES (%s, %s, %s, %s)",
        (name, qty, price, supplier)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Medicine Added Successfully!")
    view_medicines()

# ✅ View Medicines
def view_medicines():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    conn.close()

    # Clear existing table data
    for item in medicine_table.get_children():
        medicine_table.delete(item)

    # Insert new data
    for row in rows:
        medicine_table.insert("", "end", values=row)

# ✅ Update Medicine
def update_medicine():
    selected = medicine_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a medicine to update!")
        return

    item = medicine_table.item(selected[0])
    med_id = item["values"][0]

    name = med_name.get()
    qty = med_qty.get()
    price = med_price.get()
    supplier = med_supplier.get()

    if not name or not qty or not price or not supplier:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    try:
        qty = int(qty)
        price = float(price)  # ✅ Ensure price is a valid decimal
    except ValueError:
        messagebox.showwarning("Warning", "Quantity must be an integer and Price must be a number!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medicines SET name=%s, quantity=%s, price=%s, supplier=%s WHERE id=%s",
        (name, qty, price, supplier, med_id)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Medicine Updated Successfully!")
    view_medicines()

# ✅ Delete Medicine
def delete_medicine():
    selected_item = medicine_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a medicine to delete!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get selected row ID
    item = medicine_table.item(selected_item)
    med_id = item["values"][0]  # ID is the first column
    
    # Delete selected medicine
    cursor.execute("DELETE FROM medicines WHERE id = %s", (med_id,))
    conn.commit()

    # ✅ Reset ID ordering
    cursor.execute("SET @new_id = 0;")
    cursor.execute("UPDATE medicines SET id = (@new_id := @new_id + 1);")
    cursor.execute("ALTER TABLE medicines AUTO_INCREMENT = 1;")

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Medicine deleted successfully!")
    view_medicines()

# ✅ Login Window
root = tk.Tk()
root.title("Pharmacy Login")
root.geometry("300x200")

ttk.Label(root, text="Username:").pack()
entry_user = ttk.Entry(root)
entry_user.pack()

ttk.Label(root, text="Password:").pack()
entry_pass = ttk.Entry(root, show="*")
entry_pass.pack()

ttk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
