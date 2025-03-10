import tkinter as tk
from tkinter import ttk, messagebox

class Car:
    def __init__(self, brand, model, price, fuel_efficiency, color):
        self.brand = brand
        self.model = model
        self.price = price
        self.fuel_efficiency = fuel_efficiency  # in km per liter
        self.color = color

    def __str__(self):
        return f"{self.brand} {self.model} - ${self.price}, {self.fuel_efficiency} km/l, Color: {self.color}"


class CarShop:
    def __init__(self):
        self.available_cars = []

    def add_car(self, car):
        self.available_cars.append(car)

    def get_available_cars(self):
        return self.available_cars


class CarBuyer:
    def __init__(self, budget, preferred_brand=None, min_fuel_efficiency=None, preferred_color=None):
        self.budget = budget
        self.preferred_brand = preferred_brand
        self.min_fuel_efficiency = min_fuel_efficiency
        self.preferred_color = preferred_color

    def choose_car(self, car_shop):
        filtered_cars = []
        for car in car_shop.get_available_cars():
            if car.price <= self.budget:
                if self.preferred_brand and car.brand.lower() != self.preferred_brand.lower():
                    continue
                if self.min_fuel_efficiency and car.fuel_efficiency < self.min_fuel_efficiency:
                    continue
                if self.preferred_color and car.color.lower() != self.preferred_color.lower():
                    continue
                filtered_cars.append(car)

        return filtered_cars


# GUI Application
class CarSelectionApp:
    def __init__(self, root, car_shop):
        self.root = root
        self.car_shop = car_shop
        self.root.title("Car Selection System")

        # Labels and Entry Fields
        ttk.Label(root, text="Enter your budget:").grid(row=0, column=0)
        self.budget_entry = ttk.Entry(root)
        self.budget_entry.grid(row=0, column=1)

        ttk.Label(root, text="Preferred Brand:").grid(row=1, column=0)
        self.brand_entry = ttk.Entry(root)
        self.brand_entry.grid(row=1, column=1)

        ttk.Label(root, text="Minimum Fuel Efficiency (km/l):").grid(row=2, column=0)
        self.fuel_efficiency_entry = ttk.Entry(root)
        self.fuel_efficiency_entry.grid(row=2, column=1)

        ttk.Label(root, text="Preferred Color:").grid(row=3, column=0)
        self.color_entry = ttk.Entry(root)
        self.color_entry.grid(row=3, column=1)

        # Buttons
        self.search_button = ttk.Button(root, text="Search Cars", command=self.search_cars)
        self.search_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Result Display
        self.result_box = tk.Listbox(root, width=60, height=10)
        self.result_box.grid(row=5, column=0, columnspan=2)

    def search_cars(self):
        try:
            budget = int(self.budget_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid budget amount.")
            return

        preferred_brand = self.brand_entry.get().strip() or None
        min_fuel_efficiency = self.fuel_efficiency_entry.get().strip()
        min_fuel_efficiency = float(min_fuel_efficiency) if min_fuel_efficiency else None
        preferred_color = self.color_entry.get().strip() or None

        buyer = CarBuyer(budget, preferred_brand, min_fuel_efficiency, preferred_color)
        matched_cars = buyer.choose_car(self.car_shop)

        self.result_box.delete(0, tk.END)
        if matched_cars:
            for car in matched_cars:
                self.result_box.insert(tk.END, str(car))
        else:
            self.result_box.insert(tk.END, "No cars match your preferences.")


# Initialize Car Shop and Add Cars
car_shop = CarShop()
car_shop.add_car(Car("Toyota", "Corolla", 20000, 15, "Red"))
car_shop.add_car(Car("Honda", "Civic", 22000, 14, "Blue"))
car_shop.add_car(Car("Ford", "Focus", 18000, 13, "White"))
car_shop.add_car(Car("Toyota", "Camry", 25000, 12, "Black"))

# Start GUI Application
root = tk.Tk()
app = CarSelectionApp(root, car_shop)
root.mainloop()
