import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

res = supabase.table("projects").select("id, problem_statement").execute()
for proj in res.data:
    if proj["id"] in ["089f65bf-6dd5-4f87-a0a8-436f45b60734", "28fa63d2-0a84-4e26-8795-83173b1dd22c"]:
        print("ID:", proj["id"])
        print("PROBLEM STATEMENT:", repr(proj["problem_statement"]))
