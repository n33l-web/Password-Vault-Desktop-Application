from encryption import encrypt_password, decrypt_password, hash_master_password, verify_master_password
from db import insert_user, get_user_by_username, save_credential, get_credentials

def register():
    username = input("🆕 Choose a username: ")
    password = input("🔐 Choose a master password: ")
    hashed = hash_master_password(password)
    insert_user(username, hashed)

def login():
    username = input("👤 Enter your username: ")
    password = input("🔑 Enter your master password: ")
    user = get_user_by_username(username)
    
    if user and verify_master_password(password, user[2].encode()):
        print(f"\n✅ Welcome, {username}!")
        return user[0]  # return user_id
    else:
        print("❌ Invalid credentials.\n")
        return None

def add_credential(user_id):
    site = input("🌐 Site Name (e.g., Gmail): ")
    login_user = input("👥 Login Username: ")
    password = input("🔐 Password: ")
    encrypted = encrypt_password(password)
    save_credential(user_id, site, login_user, encrypted)

def view_credentials(user_id):
    creds = get_credentials(user_id)
    if not creds:
        print("📭 No credentials found.")
        return
    print("\n🔓 Saved Credentials:")
    for site, login_user, encrypted in creds:
        decrypted = decrypt_password(encrypted)
        print(f"🌐 {site} | 👥 {login_user} | 🔐 {decrypted}")

def main():
    while True:
        print("\n=== PASSWORD VAULT ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                while True:
                    print("\n--- Vault Menu ---")
                    print("1. Add Credential")
                    print("2. View Credentials")
                    print("3. Logout")
                    vault_choice = input("Choose an option: ")

                    if vault_choice == "1":
                        add_credential(user_id)
                    elif vault_choice == "2":
                        view_credentials(user_id)
                    elif vault_choice == "3":
                        print("👋 Logged out.")
                        break
                    else:
                        print("❌ Invalid choice.")
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
