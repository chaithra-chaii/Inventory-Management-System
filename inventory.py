import sqlite3
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

def signup():
    print("\n----- Sign Up -----")

    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")

    print("\n1.Staff:")
    print("2.Admin:")
    
    ch = input("Choose the role:")
    
    if ch == "1":
        role = "Staff"
    elif ch == "2":
        role = "Admin"
    else:
        print("Invalid")
        return

    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, email)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, email))

        conn.commit()
        print("Sign Up successful!")

    except sqlite3.IntegrityError:
        print("Username or email already exists!")

def signin():
    print("\n----- Sign In -----")

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    if user:
        print("Sign In successful!")

        if user[3] == "Admin":
            admin_menu()

        elif user[3] == "Staff":
            staff_menu()

        else:
            print("Invalid role.")

    else:
        print("Invalid username or password.")
        
def admin_menu():
    while True:
        print("\n======= ADMIN MENU =======")
        print("1. Manage Users")
        print("2. Manage Categories")
        print("3. Manage Suppliers")
        print("4. Manage Products")
        print("5. Search Products")
        print("6. Stock In")
        print("7. Stock Out")
        print("8. View Transactions")
        print("9. Low Stock Report")
        print("10. Logout")
        ch = input("Enter Your Choice:")
        
        if ch == "1":
            manage_users()
        elif ch == "2":
            manage_categories()
        elif ch == "3":
            manage_suppliers()
        elif ch == "4":
            manage_products()
        elif ch == "5":
            search_product()
        elif ch == "6":
            stock_in()
        elif ch == "7":
            stock_out()
        elif ch == "8":
            view_transactions()
        elif ch == "9":
            low_stock_report()
        elif ch == "10":
            print("Logout")
            break
        else:
            print("Invalid option.")
            
def manage_users():
   while True: 
        print("\n===== USER MANAGEMENT =====")
        print("1. Add User")
        print("2. View Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Back")
        
        ch = input("Enter Your Choice: ")
        if ch == "1":
            add_user()
        elif ch == "2":
            view_users()
        elif ch == "3":
            update_user()
        elif ch == "4":
            delete_user()
        elif ch == "5":
          break
        else:
          print("Invalid option")
          
def add_user():
    print("\n----- Add User -----")

    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")

    print("\n1. Staff")
    print("2. Admin")

    ch = input("Choose the role: ")

    if ch == "1":
        role = "Staff"
    elif ch == "2":
        role = "Admin"
    else:
        print("Invalid role!")
        return

    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, email)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, email))

        conn.commit()
        print("User added successfully!")

    except sqlite3.IntegrityError:
        print("Username or email already exists!")

def view_users():
    print("\n----- USER LIST -----")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if users:
        for user in users:
            print(
                "ID:", user[0],
                " Username:", user[1],
                " Role:", user[3],
                " Email:", user[4]
                  )
    else:
       print("No users found.")

def update_user():
    print("\n----- Update User -----")

    user_id = input("Enter User ID: ")

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        print("User not found!")
        return

    username = input("Enter new username: ")
    password = input("Enter new password: ")
    email = input("Enter new email: ")

    try:
        cursor.execute("""
            UPDATE users
            SET username = ?, password = ?, email = ?
            WHERE user_id = ?
        """, (username, password, email, user_id))

        conn.commit()
        print("User updated successfully!")

    except sqlite3.IntegrityError:
        print("Username or email already exists!")
        
def delete_user():
    print("\n----- Delete User -----")

    user_id = input("Enter User ID: ")

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        print("User not found!")
        return

    print("Username:", user[1])
    print("Role:", user[3])

    confirm = input("Are you sure you want to delete this user? (y/n): ")

    if confirm.lower() == "y":

        try:
            cursor.execute(
                "DELETE FROM users WHERE user_id = ?",
                (user_id,)
            )

            conn.commit()
            print("User deleted successfully!")

        except sqlite3.IntegrityError:
            print("Cannot delete this user because they have related transactions.")

    else:
        print("Delete cancelled.")
        
def manage_categories():
    while True:
        print("\n===== CATEGORY MANAGEMENT =====")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back")

        ch = input("Enter your choice: ")

        if ch == "1":
            add_category()
        elif ch == "2":
            view_categories()
        elif ch == "3":
            update_category()
        elif ch == "4":
            delete_category()
        elif ch == "5":
            break
        else:
            print("Invalid option.")

def add_category():
    print("\n----- Add Category -----")

    category_name = input("Enter category name: ")

    try:
        cursor.execute("""
            INSERT INTO categories (category_name)
            VALUES (?)
        """, (category_name,))

        conn.commit()
        print("Category added successfully!")

    except sqlite3.IntegrityError:
        print("Category already exists!")
        
def view_categories():
    print("\n----- CATEGORY LIST -----")

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if categories:
        for category in categories:
            print(
                "ID:", category[0],
                " Category:", category[1]
            )
    else:
        print("No categories found.")
        
def update_category():
    print("\n----- Update Category -----")

    category_id = input("Enter Category ID: ")

    cursor.execute(
        "SELECT * FROM categories WHERE category_id = ?",
        (category_id,)
    )

    category = cursor.fetchone()

    if not category:
        print("Category not found!")
        return

    category_name = input("Enter new category name: ")

    try:
        cursor.execute("""
            UPDATE categories
            SET category_name = ?
            WHERE category_id = ?
        """, (category_name, category_id))

        conn.commit()
        print("Category updated successfully!")

    except sqlite3.IntegrityError:
        print("Category already exists!")
        
def delete_category():
    print("\n----- Delete Category -----")

    category_id = input("Enter Category ID: ")

    cursor.execute(
        "SELECT * FROM categories WHERE category_id = ?",
        (category_id,)
    )

    category = cursor.fetchone()

    if not category:
        print("Category not found!")
        return

    print("Category:", category[1])

    confirm = input("Are you sure you want to delete this category? (y/n): ")

    if confirm.lower() == "y":
        try:
            cursor.execute(
                "DELETE FROM categories WHERE category_id = ?",
                (category_id,)
            )

            conn.commit()
            print("Category deleted successfully!")

        except sqlite3.IntegrityError:
            print("Cannot delete this category because it is used by a product.")

    else:
        print("Delete cancelled.")
        
def manage_suppliers():
    while True:
        print("\n===== SUPPLIER MANAGEMENT =====")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Back")

        ch = input("Enter your choice: ")

        if ch == "1":
            add_supplier()

        elif ch == "2":
            view_suppliers()

        elif ch == "3":
            break

        else:
            print("Invalid choice!")
            
def add_supplier():
    print("\n----- Add Supplier -----")

    supplier_name = input("Enter supplier name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")
    address = input("Enter address: ")

    try:
        cursor.execute("""
            INSERT INTO suppliers
            (supplier_name, phone, email, address)
            VALUES (?, ?, ?, ?)
        """, (supplier_name, phone, email, address))

        conn.commit()
        print("Supplier added successfully!")

    except sqlite3.IntegrityError:
        print("Email already exists!")
        
def view_suppliers():
    print("\n----- SUPPLIER LIST -----")

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    if suppliers:
        for supplier in suppliers:
            print(
                "ID:", supplier[0],
                " Name:", supplier[1],
                " Phone:", supplier[2],
                " Email:", supplier[3],
                " Address:", supplier[4]
            )
    else:
        print("No suppliers found.")

def manage_products():
    while True:
        print("\n===== PRODUCT MANAGEMENT =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back")

        ch = input("Enter your choice: ")
        if ch == "1":
            add_product()
        elif ch == "2":
            view_products()
        elif ch == "3":
            update_product()
        elif ch == "4":
            delete_product()
        elif ch == "5":
            break
        else:
            print("Invalid choice!")
            
def add_product():
    print("\n----- Add Product -----")

    product_name = input("Enter product name: ")
    category_id = input("Enter category ID: ")
    supplier_id = input("Enter supplier ID: ")
    price = input("Enter price: ")
    quantity = input("Enter quantity: ")

    try:
        cursor.execute("""
            INSERT INTO products
            (product_name, category_id, supplier_id, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_name,
            category_id,
            supplier_id,
            price,
            quantity
        ))

        conn.commit()
        print("Product added successfully!")

    except sqlite3.IntegrityError:
        print("Invalid!")
        
def view_products():
    print("\n----- PRODUCT LIST -----")

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if products:
        for product in products:
            print(
                "ID:", product[0],
                " Name:", product[1],
                " Category ID:", product[2],
                " Supplier ID:", product[3],
                " Price:", product[4],
                " Quantity:", product[5]
            )
    else:
        print("No products found.")

def update_product():
    print("\n----- Update Product -----")

    product_id = input("Enter Product ID: ")

    name = input("New product name: ")
    category = input("New category ID: ")
    supplier = input("New supplier ID: ")
    price = input("New price: ")
    quantity = input("New quantity: ")

    cursor.execute("""
        UPDATE products
        SET product_name=?, category_id=?, supplier_id=?,
            price=?, quantity=?
        WHERE product_id=?
    """, (name, category, supplier, price, quantity, product_id))

    conn.commit()
    print("Product updated successfully!")
    
def delete_product():
    print("\n----- Delete Product -----")

    product_id = input("Enter Product ID: ")

    cursor.execute(
        "DELETE FROM products WHERE product_id=?",
        (product_id,)
    )

    conn.commit()
    print("Product deleted successfully!")

def search_product():
    print("\n----- Search Product -----")

    name = input("Enter product name: ")

    cursor.execute(
        "SELECT * FROM products WHERE product_name= ?",
        (name,)
    )

    products = cursor.fetchall()

    for product in products:
        print(
            "ID:", product[0],
            " Name:", product[1],
            " Category:", product[2],
            " Supplier:", product[3],
            " Price:", product[4],
            " Quantity:", product[5]
        )

def stock_in():
    print("\n----- Stock In -----")

    product_id = input("Enter Product ID: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute(
        "UPDATE products SET quantity = quantity + ? WHERE product_id = ?",
        (quantity, product_id)
    )

    cursor.execute("""
        INSERT INTO stock_transactions
        (product_id, user_id, transaction_type, quantity, transaction_date)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (product_id, 1, "STOCK_IN", quantity))

    conn.commit()
    print("Stock added successfully!")

def stock_out():

    print("\n----- Stock Out -----")

    product_id = input("Enter Product ID: ")

    try:

        quantity = int(input("Enter quantity: "))

        if quantity <= 0:

            print("Quantity must be greater than 0!")
            return

    except ValueError:

        print("Please enter a valid quantity!")
        return

    cursor.execute(
        "SELECT quantity FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:

        print("Product not found!")
        return

    current_quantity = product[0]

    if current_quantity >= quantity:

        cursor.execute(
            """
            UPDATE products
            SET quantity = quantity - ?
            WHERE product_id = ?
            """,
            (quantity, product_id)
        )

        cursor.execute("""
            INSERT INTO stock_transactions
            (product_id, user_id, transaction_type,
             quantity, transaction_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (
            product_id,
            1,
            "STOCK_OUT",
            quantity
        ))

        conn.commit()

        print("Stock removed successfully!")

    else:

        print("Not enough stock!")

def view_transactions():

    print("\n----- TRANSACTION LIST -----")

    cursor.execute("SELECT * FROM stock_transactions")

    transactions = cursor.fetchall()

    if transactions:

        for transaction in transactions:

            print(
                "ID:", transaction[0],
                " Product ID:", transaction[1],
                " User ID:", transaction[2],
                " Type:", transaction[3],
                " Quantity:", transaction[4],
                " Date:", transaction[5]
            )

    else:

        print("No transactions found.")

def low_stock_report():

    print("\n----- LOW STOCK REPORT -----")

    cursor.execute("""
        SELECT * FROM products
        WHERE quantity <= 5
    """)

    products = cursor.fetchall()

    if products:

        for product in products:

            print(
                "ID:", product[0],
                " Name:", product[1],
                " Quantity:", product[5]
            )

    else:

        print("No low stock products!")

def staff_menu():
    while True: 
        print("\n===== STAFF MENU =====")
        print("1. View Products")
        print("2. Search Products")
        print("3. Stock In")
        print("4. Stock Out")
        print("5. View Transactions")
        print("6. Low Stock Report")
        print("7. Logout")
        
        ch = input("Enter your choice:")
        if ch == "1":
            view_products()
        elif ch == "2":
            search_product()
        elif ch == "3":
            stock_in()
        elif ch == "4":
            stock_out()
        elif ch == "5":
            view_transactions()
        elif ch == "6":
            low_stock_report()
        elif ch == "7":
            print("Logout")
            break
        else:
            print("Invalid option!")
    
while True:
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Sign Up")
    print("2. Sign In")
    print("3. Exit")

    ch = input("Enter your choice: ")

    if ch == "1":
        signup()

    elif ch == "2":
        signin()

    elif ch == "3":
        print("Exit!")
        break

    else:
        print("Invalid choice!")
    
conn.close()
    