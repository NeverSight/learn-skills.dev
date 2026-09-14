---
name: grimmory-self-hosted-library
description: Expert knowledge for setting up, configuring, and extending Grimmory — a self-hosted book library manager supporting EPUBs, PDFs, comics, Kobo sync, OPDS, and multi-user management.
triggers:
  - set up grimmory
  - self-hosted book library
  - grimmory configuration
  - grimmory docker setup
  - grimmory bookdrop
  - grimmory kobo sync
  - grimmory opds
  - grimmory metadata lookup
---

# Grimmory Self-Hosted Library Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Grimmory is a self-hosted application (successor to BookLore) for managing your entire book collection. It supports EPUBs, PDFs, MOBIs, AZW/AZW3, and comics (CBZ/CBR/CB7), with a built-in browser reader, annotations, Kobo/OPDS sync, KOReader progress sync, metadata enrichment, and multi-user support.

---

## Installation

### Requirements
- Docker and Docker Compose

### Step 1: Create `.env`

```ini
# Application
APP_USER_ID=1000
APP_GROUP_ID=1000
TZ=Etc/UTC

# Database
DATABASE_URL=jdbc:mariadb://mariadb:3306/grimmory
DB_USER=grimmory
DB_PASSWORD=${DB_PASSWORD}

# Storage: LOCAL (default) or NETWORK
DISK_TYPE=LOCAL

# MariaDB
DB_USER_ID=1000
DB_GROUP_ID=1000
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=grimmory
```

### Step 2: Create `docker-compose.yml`

```yaml
services:
  grimmory:
    image: grimmory/grimmory:latest
    # Alternative registry: ghcr.io/grimmory-tools/grimmory:latest
    container_name: grimmory
    environment:
      - USER_ID=${APP_USER_ID}
      - GROUP_ID=${APP_GROUP_ID}
      - TZ=${TZ}
      - DATABASE_URL=${DATABASE_URL}
      - DATABASE_USERNAME=${DB_USER}
      - DATABASE_PASSWORD=${DB_PASSWORD}
      - DISK_TYPE=${DISK_TYPE}
    depends_on:
      mariadb:
        condition: service_healthy
    ports:
      - "6060:6060"
    volumes:
      - ./data:/app/data
      - ./books:/books
      - ./bookdrop:/bookdrop
    healthcheck:
      test: wget -q -O - http://localhost:6060/api/v1/healthcheck
      interval: 60s
      retries: 5
      start_period: 60s
      timeout: 10s
    restart: unless-stopped

  mariadb:
    image: lscr.io/linuxserver/mariadb:11.4.5
    container_name: mariadb
    environment:
      - PUID=${DB_USER_ID}
      - PGID=${DB_GROUP_ID}
      - TZ=${TZ}
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${DB_USER}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./mariadb/config:/config
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mariadb-admin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 10
```

### Step 3: Launch

```bash
docker compose up -d

# View logs
docker compose logs -f grimmory

# Check health
curl http://localhost:6060/api/v1/healthcheck
```

Open http://localhost:6060 and create your admin account.

---

## Volume Layout

```
./data/          # App data, thumbnails, user config
./books/         # Your book files (mounted at /books)
./bookdrop/      # Drop-zone for auto-import (mounted at /bookdrop)
./mariadb/       # MariaDB data
```

---

## Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `USER_ID` | UID for the app process | `1000` |
| `GROUP_ID` | GID for the app process | `1000` |
| `TZ` | Timezone string | `Etc/UTC` |
| `DATABASE_URL` | JDBC connection string | required |
| `DATABASE_USERNAME` | DB username | required |
| `DATABASE_PASSWORD` | DB password | required |
| `DISK_TYPE` | `LOCAL` or `NETWORK` | `LOCAL` |

---

## Supported Book Formats

| Category | Formats |
|---|---|
| eBooks | EPUB, MOBI, AZW, AZW3 |
| Documents | PDF |
| Comics | CBZ, CBR, CB7 |

---

## BookDrop (Auto-Import)

Drop files into `./bookdrop/` on your host. Grimmory watches the folder, extracts metadata from Google Books and Open Library, and queues books for review.

```
./bookdrop/
  my-novel.epub        ← dropped here
  another-book.pdf     ← dropped here
```

Flow:
1. **Watch** — Grimmory monitors `/bookdrop` continuously
2. **Detect** — New files are picked up and parsed
3. **Enrich** — Metadata fetched from Google Books / Open Library
4. **Import** — Review in UI, adjust if needed, confirm import

Volume mapping required in `docker-compose.yml`:
```yaml
volumes:
  - ./bookdrop:/bookdrop
```

---

## Network Storage Mode

For NFS, SMB, or other network-mounted filesystems, set `DISK_TYPE=NETWORK`. This disables destructive UI operations (delete, move, rename) to protect shared mounts while keeping reading, metadata, and sync fully functional.

```ini
# .env
DISK_TYPE=NETWORK
```

---

## Java Backend — Key Patterns

Grimmory is a Java application (Spring Boot + MariaDB). When contributing or extending:

### Project Structure (typical Spring Boot layout)

```
src/main/java/
  com/grimmory/
    config/          # Spring configuration classes
    controller/      # REST API controllers
    service/         # Business logic
    repository/      # JPA repositories
    model/           # JPA entities
    dto/             # Data transfer objects
```

### REST API — Base Path

All endpoints are under `/api/v1/`:

```bash
# Health check
GET http://localhost:6060/api/v1/healthcheck

# Books
GET http://localhost:6060/api/v1/books
GET http://localhost:6060/api/v1/books/{id}
POST http://localhost:6060/api/v1/books
PUT http://localhost:6060/api/v1/books/{id}
DELETE http://localhost:6060/api/v1/books/{id}

# Shelves
GET http://localhost:6060/api/v1/shelves
POST http://localhost:6060/api/v1/shelves

# OPDS catalog (for compatible reader apps)
GET http://localhost:6060/opds
```

### Example: Querying the API with Java (OkHttp)

```java
import okhttp3.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class GrimmoryClient {

    private final OkHttpClient http = new OkHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();
    private final String baseUrl;
    private final String token;

    public GrimmoryClient(String baseUrl, String token) {
        this.baseUrl = baseUrl;
        this.token = token;
    }

    public String getBooks() throws Exception {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/books")
            .header("Authorization", "Bearer " + token)
            .build();

        try (Response response = http.newCall(request).execute()) {
            return response.body().string();
        }
    }
}
```

### Example: Spring Boot Controller Pattern

```java
@RestController
@RequestMapping("/api/v1/books")
@RequiredArgsConstructor
public class BookController {

    private final BookService bookService;

    @GetMapping
    public ResponseEntity<Page<BookDto>> getAllBooks(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String search) {
        return ResponseEntity.ok(bookService.findAll(page, size, search));
    }

    @GetMapping("/{id}")
    public ResponseEntity<BookDto> getBook(@PathVariable Long id) {
        return ResponseEntity.ok(bookService.findById(id));
    }

    @PostMapping
    public ResponseEntity<BookDto> createBook(@RequestBody @Valid CreateBookRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(bookService.create(request));
    }

    @PutMapping("/{id}/metadata")
    public ResponseEntity<BookDto> updateMetadata(
            @PathVariable Long id,
            @RequestBody @Valid UpdateMetadataRequest request) {
        return ResponseEntity.ok(bookService.updateMetadata(id, request));
    }
}
```

### Example: JPA Entity Pattern

```java
@Entity
@Table(name = "books")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    private String author;
    private String isbn;
    private String format;  // EPUB, PDF, CBZ, etc.

    @Column(name = "file_path")
    private String filePath;

    @Column(name = "cover_path")
    private String coverPath;

    @Column(name = "reading_progress")
    private Double readingProgress;

    @ManyToMany
    @JoinTable(
        name = "book_shelf",
        joinColumns = @JoinColumn(name = "book_id"),
        inverseJoinColumns = @JoinColumn(name = "shelf_id")
    )
    private Set<Shelf> shelves = new HashSet<>();

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;
}
```

### Example: Service with Metadata Enrichment

```java
@Service
@RequiredArgsConstructor
public class MetadataService {

    private final GoogleBooksClient googleBooksClient;
    private final OpenLibraryClient openLibraryClient;
    private final BookRepository bookRepository;

    public BookDto enrichMetadata(Long bookId) {
        Book book = bookRepository.findById(bookId)
            .orElseThrow(() -> new BookNotFoundException(bookId));

        // Try Google Books first
        Optional<BookMetadata> metadata = googleBooksClient.search(book.getTitle(), book.getAuthor());

        // Fall back to Open Library
        if (metadata.isEmpty()) {
            metadata = openLibraryClient.search(book.getIsbn());
        }

        metadata.ifPresent(m -> {
            book.setDescription(m.getDescription());
            book.setCoverUrl(m.getCoverUrl());
            book.setPublisher(m.getPublisher());
            book.setPublishedDate(m.getPublishedDate());
            bookRepository.save(book);
        });

        return BookDto.from(book);
    }
}
```

---

## OPDS Integration

Connect any OPDS-compatible reader app (Kybook, Chunky, Moon+ Reader, etc.) using:

```
http://<your-host>:6060/opds
```

Authenticate with your Grimmory username and password when prompted.

---

## Kobo / KOReader Sync

- **Kobo**: Connect via the device sync feature in Grimmory settings. The app exposes a sync endpoint compatible with Kobo's API.
- **KOReader**: Configure KOReader's sync plugin to point to your Grimmory instance URL.

---

## Multi-User & Authentication

### Local Authentication
Create users from the admin panel at http://localhost:6060. Each user has isolated shelves, reading progress, and preferences.

### OIDC Authentication
Configure via environment variables (refer to full documentation at https://grimmory.org/docs/getting-started for OIDC-specific variables such as `OIDC_ISSUER_URI`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`).

---

## Building from Source

```bash
# Clone the repository
git clone https://github.com/grimmory-tools/grimmory.git
cd grimmory

# Build with Maven
./mvnw clean package -DskipTests

# Or build Docker image locally
docker build -t grimmory:local .

# Use local build in docker-compose.yml
# Comment out 'image' and uncomment 'build: .'
```

---

## Common Docker Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View app logs
docker compose logs -f grimmory

# View DB logs
docker compose logs -f mariadb

# Restart only the app
docker compose restart grimmory

# Pull latest image and redeploy
docker compose pull && docker compose up -d

# Open a shell inside the container
docker exec -it grimmory /bin/bash

# Database shell
docker exec -it mariadb mariadb -u grimmory -p grimmory
```

---

## Troubleshooting

### Container won't start — DB connection refused
```bash
# Check MariaDB health
docker compose ps mariadb
# Should show "healthy". If not:
docker compose logs mariadb
# Ensure DATABASE_URL host matches the service name: mariadb:3306
```

### Books not appearing after BookDrop
```bash
# Verify file permissions — UID/GID must match APP_USER_ID/APP_GROUP_ID
ls -la ./bookdrop/
# Check app logs for detection events
docker compose logs -f grimmory | grep -i bookdrop
```

### Permission denied on ./books or ./data
```bash
# Set ownership to match APP_USER_ID / APP_GROUP_ID
sudo chown -R 1000:1000 ./books ./data ./bookdrop
```

### OPDS not accessible from reader app
```bash
# Confirm port 6060 is reachable from your device
curl http://<host-ip>:6060/api/v1/healthcheck
# Check firewall rules if on a remote server
```

### High memory usage
MariaDB and Grimmory together require at minimum ~512 MB RAM. For large libraries (10k+ books), allocate 1–2 GB.

### Metadata not enriching
Google Books and Open Library require outbound internet access from the container. Verify DNS and network:
```bash
docker exec -it grimmory curl -s "https://www.googleapis.com/books/v1/volumes?q=test"
```

---

## Contributing

Before opening a pull request:
1. Open an issue and get maintainer approval
2. Include screenshots/video proof and pasted test output
3. Follow backend and frontend conventions in `CONTRIBUTING.md`
4. AI-assisted code is allowed but you must run, test, and understand every line

```bash
# Run tests before submitting
./mvnw test

# Check code style
./mvnw checkstyle:check
```

---

## Links

- **GitHub**: https://github.com/grimmory-tools/grimmory
- **Docker Hub**: https://hub.docker.com/r/grimmory/grimmory
- **GHCR**: `ghcr.io/grimmory-tools/grimmory`
- **Discord**: https://discord.gg/FwqHeFWk
- **Docs**: https://grimmory.org/docs/getting-started
- **License**: AGPL-3.0
