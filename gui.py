import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from encryption import (
    hash_master_password,
    verify_master_password,
    encrypt_password,
    decrypt_password
)
from db import insert_user, get_user_by_username
import platform
import mysql.connector

current_username = None


# --- MySQL DB Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",
    database="password_vault"
)
cursor = db.cursor()


# --- Styles and Theme Setup ---
style = ttk.Style()
style = ttk.Style()

# Force 'clam' theme because 'alt' breaks TEntry styling on Mac
if platform.system() == "Darwin":
    style.theme_use('clam')
else:
    style.theme_use('clam')


BG_COLOR = "#121212"
FG_COLOR = "#eeeeee"
BTN_BG = "#2978b5"
BTN_HOVER_BG = "#1c5d99"
SUCCESS_COLOR = "#4caf50"
ERROR_COLOR = "#f44336"

style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Arial', 12))
style.configure('TEntry', 
    background=BG_COLOR,
    fieldbackground=BG_COLOR,
    foreground=FG_COLOR,
    borderwidth=0,
    relief="flat",
    font=('Arial', 11)
)

style.configure('TButton', background="#333", foreground='white', font=('Arial', 11, 'bold'), padding=6)
style.map('TButton',
          background=[('active', "#1c5d99")],
          foreground=[('active', 'white')])

# --- Main Window ---
window = tk.Tk()
window.title("🔐 Password Vault Login")
window.geometry("400x320")
window.config(bg=BG_COLOR)
window.resizable(True, True)

def toggle_fullscreen(event=None):
    is_fullscreen = window.attributes("-fullscreen")
    window.attributes("-fullscreen", not is_fullscreen)

def toggle_login_password():
        if password_entry.cget('show') == '':
            password_entry.config(show='*')
        else:
            password_entry.config(show='')
    

window.bind("<F11>", toggle_fullscreen)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

# --- UI Elements ---
title_label = tk.Label(window, text="🔐 Password Vault", font=("Arial", 16, "bold"), background=BG_COLOR, foreground=FG_COLOR)
title_label.pack(pady=15)

username_label = tk.Label(window, text="Username:", background=BG_COLOR, foreground=FG_COLOR)
username_label.pack(pady=(5,0))
username_entry = tk.Entry(window, width=30, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
username_entry.pack()

password_label = tk.Label(window, text="Master Password:", background=BG_COLOR, foreground=FG_COLOR)
password_label.pack(pady=(10,0))
password_entry = tk.Entry(window, width=30, show="*", bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
password_entry.pack()
show_pwd_var = tk.BooleanVar()
show_pwd_check = tk.Checkbutton(window, text="Show Password", variable=show_pwd_var,command=toggle_login_password,bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR)
show_pwd_check.pack()


msg_label = tk.Label(window, text="", font=("Arial", 10, "bold"), background=BG_COLOR, foreground=FG_COLOR)
msg_label.pack(pady=10)



# --- Vault Window ---
def open_vault_window(user_id):
    vault = tk.Toplevel(window)
    vault.title("🔐 Your Vault")
    vault.geometry("520x580")
    vault.config(bg=BG_COLOR)
    vault.resizable(True, True)

    # Vault fullscreen toggle (optional)
    vault.bind("<F11>", lambda e: vault.attributes("-fullscreen", not vault.attributes("-fullscreen")))
    vault.bind("<Escape>", lambda e: vault.attributes("-fullscreen", False))

    tk.Label(vault, text="Website:", background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_website = tk.Entry(vault, width=35, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
    entry_website.grid(row=0, column=1, pady=10, sticky="w")

    tk.Label(vault, text="Username:", background=BG_COLOR, foreground=FG_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_username = tk.Entry(vault, width=35, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
    entry_username.grid(row=1, column=1, pady=10, sticky="w")

    tk.Label(vault, text="Password:", background=BG_COLOR, foreground=FG_COLOR).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_password = tk.Entry(vault, width=35, show="*", bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
    entry_password.grid(row=2, column=1, pady=10, sticky="w")

    def prompt_master_password(action_callback):
        def verify():
            entered_pwd = master_pwd_entry.get()
            user_data = get_user_by_username(current_username)
            if user_data and verify_master_password(entered_pwd, user_data[2].encode()):
                popup.destroy()
                action_callback()
            else:
                error_label.config(text="❌ Incorrect master password!", fg=ERROR_COLOR)
        popup = tk.Toplevel(window)
        popup.title("Verify Master Password")
        popup.configure(bg=BG_COLOR)
        popup.geometry("320x150")
        popup.grab_set()
        tk.Label(popup, text="Re-enter Master Password:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        master_pwd_entry = tk.Entry(popup, show="*", width=30, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
        master_pwd_entry.pack()
        error_label = tk.Label(popup, text="", bg=BG_COLOR, fg=FG_COLOR, font=('Arial', 9))
        error_label.pack()
        submit_btn = tk.Button(popup, text="Submit", command=verify, bg=BTN_BG, fg='black')
        submit_btn.pack(pady=10)


    def toggle_vault_password():
        if entry_password.cget('show') == '':
            entry_password.config(show='*')
        else:
            entry_password.config(show='')
    
    show_pwd_var_vault = tk.BooleanVar()
    show_pwd_check_vault = tk.Checkbutton(vault, text="Show Password", variable=show_pwd_var_vault, command=toggle_vault_password, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR)
    show_pwd_check_vault.grid(row=3, column=1, sticky="w")


    msg_vault = tk.Label(vault, text="", font=("Arial", 10, "bold"), background=BG_COLOR, foreground=FG_COLOR)
    msg_vault.grid(row=4, column=0, columnspan=2, pady=(0,10))


    tk.Label(vault, text="Saved Credentials", font=("Arial", 14, "bold"), background=BG_COLOR, foreground=FG_COLOR).grid(row=5, column=0, columnspan=2, pady=(15,5))

    creds_listbox = tk.Listbox(vault, width=65, height=12, bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11))
    creds_listbox.grid(row=6, column=0, columnspan=2, padx=15, pady=10)

    credential_ids = []

    def load_credentials():
        creds_listbox.delete(0, tk.END)
        credential_ids.clear()
        cursor.execute("SELECT id, site_name, login_username FROM credentials WHERE user_id = %s", (user_id,))
        for cred_id, site, login_user in cursor.fetchall():
            credential_ids.append(cred_id)
            creds_listbox.insert(tk.END, f"{site} | {login_user}")

    def save_credential():
        site = entry_website.get().strip()
        uname = entry_username.get().strip()
        pwd = entry_password.get().strip()

        if not site or not uname or not pwd:
            msg_vault.config(text="❌ All fields required!", foreground=ERROR_COLOR)
            return

        encrypted = encrypt_password(pwd)

        cursor.execute(
            "INSERT INTO credentials (user_id, site_name, login_username, encrypted_password) VALUES (%s, %s, %s, %s)",
            (user_id, site, uname, encrypted)
        )
        db.commit()
        msg_vault.config(text="✅ Credential saved!", foreground=SUCCESS_COLOR)
        entry_website.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        load_credentials()

    def view_password():
        selected = creds_listbox.curselection()
        if not selected:
            msg_vault.config(text="❌ Select a credential!", foreground=ERROR_COLOR)
            return
        def do_view():
            cred_id = credential_ids[selected[0]]
            cursor.execute("SELECT encrypted_password FROM credentials WHERE id = %s", (cred_id,))
            result = cursor.fetchone()
            if result and result[0]:
                decrypted = decrypt_password(result[0])
                messagebox.showinfo("Decrypted Password", f"🔓 Password: {decrypted}")
            else:
                msg_vault.config(text="❌ No password found.", foreground=ERROR_COLOR)
        
        prompt_master_password(do_view)
        
    def delete_credential():
        selected = creds_listbox.curselection()
        if not selected:
            msg_vault.config(text="❌ Select a credential to delete!", foreground=ERROR_COLOR)
            return
        def do_delete():
            cred_id = credential_ids[selected[0]]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected credential?")
            if confirm:
                cursor.execute("DELETE FROM credentials WHERE id = %s", (cred_id,))
                db.commit()
                msg_vault.config(text="✅ Credential deleted.", foreground=SUCCESS_COLOR)
                load_credentials()
                
        prompt_master_password(do_delete)


    def edit_credential():
        selected = creds_listbox.curselection()
        if not selected:
            msg_vault.config(text="❌ Select a credential to edit!", foreground=ERROR_COLOR)
            return
        def do_edit():
            cred_id = credential_ids[selected[0]]
            cursor.execute("SELECT site_name, login_username, encrypted_password FROM credentials WHERE id = %s", (cred_id,))
            result = cursor.fetchone()
            if not result:
                msg_vault.config(text="❌ Credential not found.", foreground=ERROR_COLOR)
                return
            site, uname, enc_pwd = result
            decrypted_pwd = decrypt_password(enc_pwd)
            entry_website.delete(0, tk.END)
            entry_website.insert(0, site)
            entry_username.delete(0, tk.END)
            entry_username.insert(0, uname)
            entry_password.delete(0, tk.END)
            entry_password.insert(0, decrypted_pwd)
            
            def save_edited_credential():
                new_site = entry_website.get().strip()
                new_uname = entry_username.get().strip()
                new_pwd = entry_password.get().strip()
                if not new_site or not new_uname or not new_pwd:
                    msg_vault.config(text="❌ All fields required!", foreground=ERROR_COLOR)
                    return
                new_encrypted = encrypt_password(new_pwd)
                cursor.execute(
                    "UPDATE credentials SET site_name=%s, login_username=%s, encrypted_password=%s WHERE id=%s",
                    (new_site, new_uname, new_encrypted, cred_id)
                    )
                db.commit()
                msg_vault.config(text="✅ Credential updated!", foreground=SUCCESS_COLOR)
                load_credentials()
                save_btn.config(command=save_credential)
            
            save_btn.config(command=save_edited_credential)
        
        prompt_master_password(do_edit)



    # Buttons frame
    btn_frame = tk.Frame(vault, bg=BG_COLOR)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

    save_btn = tk.Button(btn_frame, text="Save Credential", command=save_credential)
    save_btn.grid(row=0, column=0, padx=10)

    view_btn = tk.Button(btn_frame, text="View Password", command=view_password)
    view_btn.grid(row=0, column=1, padx=10)

    edit_btn = tk.Button(btn_frame, text="Edit Credential", command=edit_credential)
    edit_btn.grid(row=0, column=2, padx=10)

    delete_btn = tk.Button(btn_frame, text="Delete Credential", command=delete_credential)
    delete_btn.grid(row=0, column=3, padx=10)

    # Logout button to close vault window only
    logout_btn = tk.Button(vault, text="Logout", command=vault.destroy)
    logout_btn.grid(row=8, column=0, columnspan=2, pady=10)
    

    load_credentials()

# --- Auth Functions ---
def register():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        msg_label.config(text="❌ Fields required.", foreground=ERROR_COLOR)
        print("[DEBUG] Registration failed: Empty username or password")
        return
    try:
        hashed = hash_master_password(password)
        insert_user(username, hashed)
        msg_label.config(text="✅ Registered!", foreground=SUCCESS_COLOR)
        print(f"[DEBUG] User registered: {username}")
    except Exception as e:
        msg_label.config(text="❌ Registration error.", foreground=ERROR_COLOR)
        import traceback
        print("[ERROR] Registration failed:")
        traceback.print_exc()  # this prints the full error stack trace



def login():
    username = username_entry.get()
    password = password_entry.get()
    try:
        user = get_user_by_username(username)
        print(f"[DEBUG] Retrieved user: {user}")
        if user and verify_master_password(password, user[2].encode()):
            msg_label.config(text="✅ Logged in!", foreground=SUCCESS_COLOR)
            open_vault_window(user[0])
            print("[DEBUG] Login success, opening vault")
        else:
            msg_label.config(text="❌ Invalid username or password!", foreground=ERROR_COLOR)
            print("[DEBUG] Login failed: Invalid credentials")
    except Exception as e:
        msg_label.config(text="❌ Login error.", foreground=ERROR_COLOR)
        print(f"[ERROR] Login failed: {e}")
    global current_username
    current_username = username  # Store logged in username



# --- Buttons ---
frame = tk.Frame(window, bg=BG_COLOR)
frame.pack(pady=1)
register_btn = tk.Button(frame, text="Register", command=register)
register_btn.grid(row=0, column=0, padx=15)
login_btn = tk.Button(frame, text="Login", command=login)
login_btn.grid(row=0, column=1, padx=15)

exit_btn = tk.Button(window, text="Exit", command=window.destroy)
exit_btn.pack(pady=10)

window.mainloop()
