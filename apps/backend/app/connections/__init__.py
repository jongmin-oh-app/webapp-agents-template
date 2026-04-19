from supabase import create_client, Client

from app.config import get_config


def get_supabase() -> Client:
    cfg = get_config()
    return create_client(cfg["supabase_url"], cfg["supabase_service_role_key"])
