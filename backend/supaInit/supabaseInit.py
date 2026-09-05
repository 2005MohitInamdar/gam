import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("PUBLIC_SUPABASE_PUBLISHABLE_KEY", "")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabaseb environment variables. Check your .env file.")

supabaseClient: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
