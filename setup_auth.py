"""
One-time authentication setup for Google Keep MCP.

Run this once:  py setup_auth.py

It will securely ask for your Google password, log in to Keep,
save an auth token to Windows Credential Manager, and never
store your password anywhere on disk.
"""

import getpass
import keyring
import gkeepapi

SERVICE = "google-keep-mcp"
EMAIL_KEY = "email"
TOKEN_KEY = "master_token"

def main():
    print("=== Google Keep MCP - One-Time Auth Setup ===\n")

    email = input("Google email address: ").strip()
    password = getpass.getpass("Google password (hidden): ")

    print("\nLogging in to Google Keep...")
    keep = gkeepapi.Keep()

    try:
        keep.login(email, password)
    except Exception as e:
        print(f"\n❌ Login failed: {e}")
        print("\nTips:")
        print("  • Make sure your email and password are correct.")
        print("  • If Google blocked the login, visit https://accounts.google.com/")
        print("    and check for a security alert, then try again.")
        return

    # Get the master token (safe to store — it's not your password)
    master_token = keep.getMasterToken()

    # Save securely to Windows Credential Manager
    keyring.set_password(SERVICE, EMAIL_KEY, email)
    keyring.set_password(SERVICE, TOKEN_KEY, master_token)

    print(f"\n✅ Success! Auth token saved to Windows Credential Manager.")
    print("   Your password was never written to disk.")
    print("\nYou can now run the MCP server with:  py server.py")

if __name__ == "__main__":
    main()
