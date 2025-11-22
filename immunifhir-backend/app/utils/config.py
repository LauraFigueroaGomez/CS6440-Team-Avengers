import os
import httpx
from supabase import create_client, ClientOptions
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

http_client = httpx.Client(http2=False, timeout=10.0)

options = ClientOptions(
    http_client=http_client,
    postgrest_client_timeout=10,
    storage_client_timeout=10,
    schema="public"
)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
