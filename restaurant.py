import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random 

# ========================= ITEM MENU AND PRICES =========================
FOOD_MENU = {
    "Tandoori Roti (₹25/pc)": 25,
    "Dal Makhni (₹120)": 120,
    "Paneer Paratha (₹120/pc)": 120,
    "Panner Raseela (₹270)": 270,
    "Veg Biryani (₹120)": 120,
}

# --- GLOBAL VARIABLE FOR BILL TRACKING (DOES NOT DEPEND ON TKINTER) ---
current_bill_no = "N/A" 
# --- customer_name_var and customer_phone_var must be moved below root = tk.Tk() ---


# ========================= CORE CALCULATION FUNCTION =========================

def calculate_total():
    """Calculates the total bill based on the quantity of all food items and updates customer info."""
    global current_bill_no
    final_total = 0
    
    # Input validation for Customer Info
    if customer_name_var.get() == "" or customer_phone_var.get() == "":
        messagebox.showerror("Error", "Customer Name and Phone Number are required.")
        return

    # 1. Gather data and calculate total
    for item in FOOD_MENU.keys():
        qty_var = item_vars.get(item + "_qty")
        
        try:
            quantity = int(qty_var.get()) if qty_var.get() else 0
            
            if quantity < 0:
                 messagebox.showerror("Error", "Quantity cannot be negative.")
                 return
            
            if quantity > 0:
                price = FOOD_MENU[item]
                item_cost = price * quantity
                final_total += item_cost
                
        except ValueError:
            messagebox.showerror("Error", f"Invalid quantity for '{item}'. Please enter a number.")
            return

    # Check if anything was ordered
    if final_total == 0:
        messagebox.showwarning("Warning", "Please order at least one item.")
        return
        
    # 2. Generate and store Bill Number and Date
    if current_bill_no == "N/A":
        current_bill_no = f"INV-{random.randint(10000, 99999)}" 

    current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    # 3. Update the Header Labels
    bill_no_label.config(text=f"Bill No: {current_bill_no}")
    date_label.config(text=f"Date: {current_date}")

    # 4. Update the 'Total Cost' field in the GUI
    total_cost_entry.config(state='normal') 
    total_cost_entry.delete(0, 'end')
    total_cost_entry.insert(0, f"₹{final_total:.2f}")
    total_cost_entry.config(state='readonly')
    
    messagebox.showinfo("Success", f"Bill calculated for {customer_name_var.get()}. Total: ₹{final_total:.2f}")

def reset_fields():
    """Resets all quantity fields, the total cost, and customer info to default."""
    global current_bill_no
    
    # 1. Reset all quantity entry fields to "0"
    for var in item_vars.values():
        if isinstance(var, tk.StringVar):
            var.set("0")
    
    # 2. Reset the total cost field
    total_cost_entry.config(state='normal')
    total_cost_entry.delete(0, 'end')
    total_cost_entry.insert(0, "₹0.00")
    total_cost_entry.config(state='readonly')
    
    # 3. Reset Bill Number and Customer Info
    current_bill_no = "N/A"
    bill_no_label.config(text="Bill No: N/A")
    date_label.config(text="Date: N/A")
    customer_name_var.set("") # This relies on the StringVar being initialized later
    customer_phone_var.set("") # This relies on the StringVar being initialized later
    
    messagebox.showinfo("Reset Complete", "System is ready for a new order.")

def exit_app():
    """Exits the application."""
    if messagebox.askyesno("Exit Application", "Are you sure you want to close the application?"):
        root.destroy()

# ========================= GUI SETUP =========================

root = tk.Tk()
root.title("Restaurant Bill Calculator")
root.geometry("450x650") 
root.resizable(False, False)
root.configure(bg="#F5F5F5") 

# --- MOVED TKINTER-DEPENDENT VARIABLES HERE (FIXING THE ERROR) ---
# Global declarations for the variables must occur *after* root = tk.Tk()
customer_name_var = tk.StringVar(value="")
customer_phone_var = tk.StringVar(value="")
# --- End of fix ---


# --- Global Dictionary to hold Menu Entry variables ---
item_vars = {}

# --- 1. Title Frame ---
title_frame = tk.Frame(root, bg="#6A1B9A", height=60)
title_frame.pack(side=tk.TOP, fill=tk.X)
tk.Label(title_frame, text="RESTAURANT BILL CALCULATOR", font=('Arial', 18, 'bold'), fg="white", bg="#6A1B9A").pack(pady=10)

# --- 1.5. Header Info Frame (Bill No. & Date) ---
header_info_frame = tk.Frame(root, bg="#EAEAEA")
header_info_frame.pack(side=tk.TOP, fill=tk.X)

global bill_no_label
bill_no_label = tk.Label(header_info_frame, text="Bill No: N/A", font=('Arial', 10, 'bold'), fg="#6A1B9A", bg="#EAEAEA")
bill_no_label.pack(side=tk.LEFT, padx=20, pady=5)

global date_label
date_label = tk.Label(header_info_frame, text="Date: N/A", font=('Arial', 10, 'bold'), fg="#6A1B9A", bg="#EAEAEA")
date_label.pack(side=tk.RIGHT, padx=20, pady=5)


# --- 2. Customer Info Frame ---
cust_frame = tk.LabelFrame(root, text="Customer Details", font=('Arial', 12, 'bold'), padx=15, pady=10, bg="#ffffff", fg="#6A1B9A")
cust_frame.pack(pady=10, padx=20, fill='x')

tk.Label(cust_frame, text="Name:", font=('Arial', 11), bg="#ffffff").grid(row=0, column=0, pady=5, padx=5, sticky="w")
tk.Entry(cust_frame, textvariable=customer_name_var, font=('Arial', 11), width=20, bd=2, relief=tk.RIDGE).grid(row=0, column=1, pady=5, padx=5)

tk.Label(cust_frame, text="Phone:", font=('Arial', 11), bg="#ffffff").grid(row=1, column=0, pady=5, padx=5, sticky="w")
tk.Entry(cust_frame, textvariable=customer_phone_var, font=('Arial', 11), width=20, bd=2, relief=tk.RIDGE).grid(row=1, column=1, pady=5, padx=5)


# --- 3. Menu and Quantity Frame ---
menu_frame = tk.LabelFrame(root, text="Menu & Quantity", font=('Arial', 12, 'bold'), padx=15, pady=10, bg="#ffffff", fg="#6A1B9A")
menu_frame.pack(pady=10, padx=20, fill='x')

current_row = 0
for item, price in FOOD_MENU.items():
    
    # 1. Quantity Variable (Default is 0)
    qty_var = tk.StringVar(value="0")
    item_vars[item + "_qty"] = qty_var

    # 2. Item Label
    tk.Label(menu_frame, text=item, font=('Arial', 11), bg="#ffffff", anchor="w").grid(row=current_row, column=0, pady=8, padx=10, sticky="w")
    
    # 3. Quantity Entry
    qty_entry = tk.Entry(menu_frame, textvariable=qty_var, font=('Arial', 11), width=10, justify='center', bd=2, relief=tk.RIDGE)
    qty_entry.grid(row=current_row, column=1, pady=8, padx=10)
    
    current_row += 1

# --- 4. Total Display Frame ---
total_frame = tk.Frame(root, bg="#EAEAEA")
total_frame.pack(pady=10, fill='x', padx=20)

tk.Label(total_frame, text="Total Cost:", font=('Arial', 14, 'bold'), bg="#EAEAEA", fg="#333333").pack(side=tk.LEFT, padx=10)

total_cost_entry = tk.Entry(total_frame, font=('Arial', 14, 'bold'), width=15, state='readonly', justify='right', fg="#004D40", bd=4, relief=tk.SUNKEN)
total_cost_entry.insert(0, "₹0.00")
total_cost_entry.pack(side=tk.RIGHT, padx=10)


# --- 5. Action Buttons (Bottom) ---
button_frame = tk.Frame(root, bg="#F5F5F5")
button_frame.pack(pady=15)

tk.Button(button_frame, text="CALCULATE TOTAL", font=('Arial', 11, 'bold'), bg="#4CAF50", fg="white", command=calculate_total, width=18).pack(side=tk.LEFT, padx=8)
tk.Button(button_frame, text="RESET", font=('Arial', 11, 'bold'), bg="#FF9800", fg="white", command=reset_fields, width=10).pack(side=tk.LEFT, padx=8)
tk.Button(button_frame, text="EXIT", font=('Arial', 11, 'bold'), bg="#F44336", fg="white", command=exit_app, width=10).pack(side=tk.LEFT, padx=8)

root.mainloop()