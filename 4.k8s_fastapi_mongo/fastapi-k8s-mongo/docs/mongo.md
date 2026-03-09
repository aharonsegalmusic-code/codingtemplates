# MongoDB 

### 1.2 Start MongoDB Server

```bash
sudo systemctl start mongod
sudo systemctl enable mongod   # optional: start on boot
```

### 1.3 Access Mongo Shell

```bash
mongo
```

### 1.4 Check MongoDB Version

```bash
mongo --version
```

### 1.5 Stop MongoDB Server

```bash
sudo systemctl stop mongod
```

---

## 2. MongoDB in Docker

### 2.1 Pull MongoDB Image

```bash
docker pull mongo:latest
```

### 2.2 Run MongoDB Container

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest
```

### 2.3 Check Running Containers

```bash
docker ps
```

### 2.4 View Logs

```bash
docker logs mongodb
```

### 2.5 Access Mongo Shell inside Container

```bash
docker exec -it mongodb mongo
```

### 2.6 Stop Container

```bash
docker stop mongodb
```

### 2.7 Remove Container

```bash
docker rm mongodb
```

### 2.8 Connect Compass to Docker MongoDB

* Host: `localhost`
* Port: `27017`
* Authentication: leave empty (unless you set credentials)

---

## 3. Basic MongoDB Commands (both local and Docker)

```js
// Show databases
show dbs

// Create/use database
use myDatabase

// Create collection and insert document
db.myCollection.insertOne({ name: 'John', age: 30 })

// View documents
db.myCollection.find()
```

This guide covers installation,
