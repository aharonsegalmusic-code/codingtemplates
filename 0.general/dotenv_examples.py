from dotenv import dotenv_values, load_dotenv
import os

# =========================================================
# SETUP: Let's create a fake .env file to demo with
# =========================================================
with open(".env.demo", "w") as f:
    f.write("MONGO_URI=mongodb://localhost:27017/mydb\n")
    f.write("SECRET_KEY=super_secret_123\n")
    f.write("DEBUG=true\n")
    f.write("PORT=8080\n")

print("=" * 60)
print("  DOTENV CHEAT SHEET — LEARN BY SEEING")
print("=" * 60)

# =========================================================
# 1. dotenv_values() — returns a plain dict
# =========================================================
print("\n📦 METHOD 1: dotenv_values('.env.demo')")
print("-" * 40)

config = dotenv_values(".env.demo")

print(f"  type(config)        → {type(config).__name__}")
print(f"  config               → {dict(config)}")
print(f"  config['MONGO_URI']  → {config['MONGO_URI']}")
print(f"  config.get('DEBUG')  → {config.get('DEBUG')}")
print(f"  config.get('NOPE')   → {config.get('NOPE')}")
print(f"  config.get('NOPE', 'fallback') → {config.get('NOPE', 'fallback')}")

# =========================================================
# 2. load_dotenv() — loads into os.environ
# =========================================================
print("\n\n🌍 METHOD 2: load_dotenv('.env.demo')")
print("-" * 40)

# First show that os.environ does NOT have our vars yet
print(f"  BEFORE load_dotenv:")
print(f"    os.getenv('MONGO_URI')  → {os.getenv('MONGO_URI')}")
print(f"    os.getenv('SECRET_KEY') → {os.getenv('SECRET_KEY')}")

load_dotenv(".env.demo")

print(f"  AFTER load_dotenv:")
print(f"    os.getenv('MONGO_URI')  → {os.getenv('MONGO_URI')}")
print(f"    os.getenv('SECRET_KEY') → {os.getenv('SECRET_KEY')}")
print(f"    os.environ['PORT']      → {os.environ['PORT']}")
print(f"    os.getenv('NOPE')       → {os.getenv('NOPE')}")
print(f"    os.getenv('NOPE', '?')  → {os.getenv('NOPE', '?')}")

# =========================================================
# 3. Difference: dict['key'] vs dict.get('key')
# =========================================================
print("\n\n⚠️  METHOD 3: ['key'] vs .get('key')")
print("-" * 40)
print(f"  config['MONGO_URI']       → {config['MONGO_URI']}  (works!)")
print(f"  config.get('MONGO_URI')   → {config.get('MONGO_URI')}  (works!)")
print(f"  config.get('MISSING')     → {config.get('MISSING')}  (returns None)")
try:
    _ = config['MISSING']
except KeyError as e:
    print(f"  config['MISSING']         → 💥 KeyError: {e}")

# =========================================================
# 4. os.environ['key'] vs os.getenv('key')
# =========================================================
print("\n\n⚠️  METHOD 4: os.environ['key'] vs os.getenv('key')")
print("-" * 40)
print(f"  os.environ['PORT']        → {os.environ['PORT']}  (works!)")
print(f"  os.getenv('PORT')         → {os.getenv('PORT')}  (works!)")
print(f"  os.getenv('MISSING')      → {os.getenv('MISSING')}  (returns None)")
try:
    _ = os.environ['MISSING']
except KeyError as e:
    print(f"  os.environ['MISSING']     → 💥 KeyError: {e}")

# =========================================================
# 5. Switching environments
# =========================================================
print("\n\n🔄 METHOD 5: Switching environments")
print("-" * 40)

# Create a second env file
with open(".env.prod", "w") as f:
    f.write("MONGO_URI=mongodb://prod-server:27017/realdb\n")
    f.write("DEBUG=false\n")

PRODUCTION = False
ENV_PATH = ".env.prod" if PRODUCTION else ".env.demo"
config = dotenv_values(ENV_PATH)
print(f"  PRODUCTION = {PRODUCTION}")
print(f"  ENV_PATH   = {ENV_PATH}")
print(f"  MONGO_URI  = {config['MONGO_URI']}")
print(f"  DEBUG      = {config['DEBUG']}")

PRODUCTION = True
ENV_PATH = ".env.prod" if PRODUCTION else ".env.demo"
config = dotenv_values(ENV_PATH)
print(f"\n  PRODUCTION = {PRODUCTION}")
print(f"  ENV_PATH   = {ENV_PATH}")
print(f"  MONGO_URI  = {config['MONGO_URI']}")
print(f"  DEBUG      = {config['DEBUG']}")

# =========================================================
# 6. Merging env files
# =========================================================
print("\n\n🔗 METHOD 6: Merging .env files")
print("-" * 40)

defaults = dotenv_values(".env.demo")
overrides = dotenv_values(".env.prod")
merged = {**defaults, **overrides}

print(f"  defaults  → {dict(defaults)}")
print(f"  overrides → {dict(overrides)}")
print(f"  merged    → {merged}")
print(f"  (PORT came from defaults, DEBUG was overridden by prod)")

# =========================================================
# SUMMARY
# =========================================================
print("\n\n" + "=" * 60)
print("  QUICK REFERENCE")
print("=" * 60)
print("""
  dotenv_values(path)  → returns dict, doesn't touch os.environ
  load_dotenv(path)    → loads into os.environ

  dict['KEY']          → value or 💥 KeyError
  dict.get('KEY')      → value or None
  dict.get('KEY','x')  → value or 'x'

  os.environ['KEY']    → value or 💥 KeyError
  os.getenv('KEY')     → value or None
  os.getenv('KEY','x') → value or 'x'
""")

# Cleanup
os.remove(".env.demo")
os.remove(".env.prod")