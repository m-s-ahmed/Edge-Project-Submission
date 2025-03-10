import tkinter as tk
from tkinter import ttk, messagebox

class Restaurant:
    def __init__(self, root):
        self.menu = {}  # Store menu items and prices
        self.order = {}  # Store customer orders
        self.root = root
        self.root.title("Restaurant Management System")

        # Menu Management
        self.menu_frame = ttk.LabelFrame(root, text="Menu Management")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.menu_frame, text="Item Name:").grid(row=0, column=0)
        self.item_entry = ttk.Entry(self.menu_frame)
        self.item_entry.grid(row=0, column=1)
        
        ttk.Label(self.menu_frame, text="Price:").grid(row=1, column=0)
        self.price_entry = ttk.Entry(self.menu_frame)
        self.price_entry.grid(row=1, column=1)
        
        self.add_button = ttk.Button(self.menu_frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.menu_listbox = tk.Listbox(self.menu_frame, width=40, height=5)
        self.menu_listbox.grid(row=3, column=0, columnspan=2)
        
        # Order Management
        self.order_frame = ttk.LabelFrame(root, text="Take Order")
        self.order_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.order_frame, text="Item Name:").grid(row=0, column=0)
        self.order_item_entry = ttk.Entry(self.order_frame)
        self.order_item_entry.grid(row=0, column=1)
        
        ttk.Label(self.order_frame, text="Quantity:").grid(row=1, column=0)
        self.quantity_entry = ttk.Entry(self.order_frame)
        self.quantity_entry.grid(row=1, column=1)
        
        self.order_button = ttk.Button(self.order_frame, text="Add to Order", command=self.add_to_order)
        self.order_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.order_listbox = tk.Listbox(self.order_frame, width=40, height=5)
        self.order_listbox.grid(row=3, column=0, columnspan=2)
        
        # Bill Calculation
        self.bill_button = ttk.Button(root, text="Calculate Bill", command=self.calculate_bill)
        self.bill_button.grid(row=2, column=0, pady=10)
    
    def add_item(self):
        item_name = self.item_entry.get().strip().title()
        try:
            price = float(self.price_entry.get())
            if item_name and price > 0:
                self.menu[item_name] = price
                self.menu_listbox.insert(tk.END, f"{item_name}: ${price:.2f}")
                self.item_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Input Error", "Please enter a valid item name and price.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a numeric value for price.")
    
    def add_to_order(self):
        item_name = self.order_item_entry.get().strip().title()
        try:
            quantity = int(self.quantity_entry.get())
            if item_name in self.menu and quantity > 0:
                if item_name in self.order:
                    self.order[item_name] += quantity
                else:
                    self.order[item_name] = quantity
                self.order_listbox.insert(tk.END, f"{item_name} x {quantity}")
                self.order_item_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Input Error", "Item not found or invalid quantity.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a numeric value for quantity.")
    
    def calculate_bill(self):
        if not self.order:
            messagebox.showinfo("Order Status", "No items in the order.")
            return
        
        subtotal = sum(self.menu[item] * qty for item, qty in self.order.items())
        tax = subtotal * 0.05
        service_charge = subtotal * 0.10
        total = subtotal + tax + service_charge
        
        bill_summary = "\n".join([f"{item} x {qty} = ${self.menu[item] * qty:.2f}" for item, qty in self.order.items()])
        bill_summary += f"\n\nSubtotal: ${subtotal:.2f}\nTax (5%): ${tax:.2f}\nService Charge (10%): ${service_charge:.2f}\nTotal: ${total:.2f}"
        messagebox.showinfo("Bill Summary", bill_summary)
        self.order.clear()
        self.order_listbox.delete(0, tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Restaurant(root)
    root.mainloop()
