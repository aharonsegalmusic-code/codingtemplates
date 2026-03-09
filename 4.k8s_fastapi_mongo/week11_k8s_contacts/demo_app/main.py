import uvicorn
from mongo_db import mongo_client # Removed 'app.' prefix for container compatibility

def main():
    # Verify connection on startup
    print(f"Connected to mongo client: {mongo_client is not None}")   
    
    # In Docker, use the 'module:attribute' string for better reloading
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
