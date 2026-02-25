---
name: wallet-brc100-go
description: This skill should be used when the user asks to "implement BRC-100 wallet in Go", "use go-wallet-toolbox", "Go BSV wallet", "BRC-100 Go implementation", or needs guidance on building conforming wallets using Go wallet-toolbox.
---

# BRC-100 Wallet Implementation Guide (Go)

Comprehensive guide for implementing BRC-100 conforming wallets using the `go-wallet-toolbox` package.

## 🎯 Quick Reference

### Core Dependencies

```go
import (
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/wallet"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/storage"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/services"
    sdk "github.com/bsv-blockchain/go-sdk/wallet"
    "github.com/bsv-blockchain/go-sdk/primitives/ec"
    "github.com/bsv-blockchain/go-sdk/transaction"
)
```

### Installation

```bash
go get github.com/bsv-blockchain/go-wallet-toolbox
go get github.com/bsv-blockchain/go-sdk
```

---

## 📚 Table of Contents

1. [Wallet Initialization](#1-wallet-initialization)
2. [Transaction Operations](#2-transaction-operations)
3. [Key Management](#3-key-management)
4. [Storage Configuration](#4-storage-configuration)
5. [Certificate Operations](#5-certificate-operations)
6. [Error Handling](#6-error-handling)
7. [Production Patterns](#7-production-patterns)

---

## 1. Wallet Initialization

### Pattern A: Simple Wallet Setup

```go
package main

import (
    "context"
    "log"

    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/wallet"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/storage"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/services"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/defs"
    sdk "github.com/bsv-blockchain/go-sdk/wallet"
    "github.com/bsv-blockchain/go-sdk/primitives/ec"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

func createWallet() (*wallet.Wallet, error) {
    ctx := context.Background()

    // 1. Generate root key (or derive from mnemonic)
    rootKey, err := ec.NewPrivateKey()
    if err != nil {
        return nil, err
    }

    // 2. Create key deriver
    keyDeriver := sdk.NewKeyDeriver(rootKey)

    // 3. Setup SQLite storage
    db, err := gorm.Open(sqlite.Open("wallet.db"), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    storageOpts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: rootKey.PubKey().Compressed(),
        StorageName:        "main-wallet",
    }

    walletStorage, err := storage.NewStorage(storageOpts)
    if err != nil {
        return nil, err
    }

    // 4. Setup services (mainnet)
    servicesOpts := &services.Options{
        Network: defs.Mainnet,
        ArcURL:  "https://arc.taal.com",
        WocURL:  "https://api.whatsonchain.com/v1/bsv/main",
    }

    walletServices, err := services.NewServices(ctx, servicesOpts)
    if err != nil {
        return nil, err
    }

    // 5. Create wallet
    w, err := wallet.NewWallet(
        ctx,
        keyDeriver,
        walletStorage,
        wallet.WithServices(walletServices),
        wallet.WithNetwork(defs.Mainnet),
    )
    if err != nil {
        return nil, err
    }

    return w, nil
}
```

### Pattern B: Wallet with MySQL Storage

```go
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

func createMySQLWallet(ctx context.Context, rootKey *ec.PrivateKey) (*wallet.Wallet, error) {
    // MySQL DSN
    dsn := "user:password@tcp(127.0.0.1:3306)/wallet_db?charset=utf8mb4&parseTime=True&loc=Local"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    storageOpts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: rootKey.PubKey().Compressed(),
        StorageName:        "mysql-wallet",
    }

    walletStorage, err := storage.NewStorage(storageOpts)
    if err != nil {
        return nil, err
    }

    keyDeriver := sdk.NewKeyDeriver(rootKey)
    walletServices, err := services.NewServices(ctx, &services.Options{
        Network: defs.Mainnet,
        ArcURL:  "https://arc.taal.com",
    })
    if err != nil {
        return nil, err
    }

    return wallet.NewWallet(
        ctx,
        keyDeriver,
        walletStorage,
        wallet.WithServices(walletServices),
        wallet.WithNetwork(defs.Mainnet),
    )
}
```

### Pattern C: Testnet Wallet

```go
func createTestnetWallet(ctx context.Context) (*wallet.Wallet, error) {
    rootKey, _ := ec.NewPrivateKey()
    keyDeriver := sdk.NewKeyDeriver(rootKey)

    db, _ := gorm.Open(sqlite.Open("testnet.db"), &gorm.Config{})
    storageOpts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: rootKey.PubKey().Compressed(),
        StorageName:        "testnet-wallet",
    }
    walletStorage, _ := storage.NewStorage(storageOpts)

    // Testnet services
    walletServices, err := services.NewServices(ctx, &services.Options{
        Network: defs.Testnet,
        ArcURL:  "https://arc-test.taal.com",
        WocURL:  "https://api.whatsonchain.com/v1/bsv/test",
    })
    if err != nil {
        return nil, err
    }

    return wallet.NewWallet(
        ctx,
        keyDeriver,
        walletStorage,
        wallet.WithServices(walletServices),
        wallet.WithNetwork(defs.Testnet),
    )
}
```

---

## 2. Transaction Operations

### Create a Transaction

```go
import (
    "github.com/bsv-blockchain/go-sdk/script"
    sdk "github.com/bsv-blockchain/go-sdk/wallet"
)

func sendBSV(
    ctx context.Context,
    w *wallet.Wallet,
    recipientAddress string,
    satoshis uint64,
) (string, error) {
    // Build locking script from address
    lockingScript, err := script.NewP2PKHFromAddress(recipientAddress)
    if err != nil {
        return "", err
    }

    // Create action args
    args := &sdk.CreateActionArgs{
        Description: "Send BSV payment",
        Outputs: []sdk.CreateActionOutput{
            {
                LockingScript:    lockingScript.String(),
                Satoshis:         satoshis,
                OutputDescription: fmt.Sprintf("Payment to %s", recipientAddress),
                Basket:            "default",
                Tags:              []string{"payment"},
            },
        },
        Options: &sdk.CreateActionOptions{
            AcceptDelayedBroadcast: false, // Broadcast immediately
            RandomizeOutputs:       true,  // Privacy
        },
    }

    // Create action
    result, err := w.CreateAction(ctx, args)
    if err != nil {
        return "", err
    }

    if result.TxID != nil {
        return *result.TxID, nil
    }

    // Handle signing if needed
    if result.SignableTransaction != nil {
        return signAndFinalize(ctx, w, result.SignableTransaction)
    }

    return "", fmt.Errorf("unexpected result format")
}
```

### Sign a Transaction

```go
func signTransaction(
    ctx context.Context,
    w *wallet.Wallet,
    reference string,
    unlockingScripts map[uint32]sdk.UnlockingScriptSend,
) (*sdk.SignActionResult, error) {
    args := &sdk.SignActionArgs{
        Reference: reference,
        Spends:    unlockingScripts,
    }

    result, err := w.SignAction(ctx, args)
    if err != nil {
        return nil, err
    }

    return result, nil
}
```

### Check Wallet Balance

```go
func getBalance(ctx context.Context, w *wallet.Wallet) (uint64, error) {
    // Use special operation for quick balance
    args := &sdk.ListOutputsArgs{
        Basket: "00000000000000000000000000000000", // Special basket for balance
    }

    result, err := w.ListOutputs(ctx, args)
    if err != nil {
        return 0, err
    }

    return uint64(result.TotalOutputs), nil
}

// Get detailed balance with UTXOs
func getDetailedBalance(ctx context.Context, w *wallet.Wallet) (*sdk.ListOutputsResult, error) {
    args := &sdk.ListOutputsArgs{
        Basket:    "default",
        Spendable: to.Ptr(true),
        Limit:     to.Ptr(uint32(100)),
        Offset:    to.Ptr(uint32(0)),
    }

    result, err := w.ListOutputs(ctx, args)
    if err != nil {
        return nil, err
    }

    log.Printf("Found %d spendable outputs", len(result.Outputs))
    for _, output := range result.Outputs {
        log.Printf("  %s: %d satoshis", output.Outpoint, output.Satoshis)
    }

    return result, nil
}
```

### List Transaction History

```go
func listTransactions(ctx context.Context, w *wallet.Wallet) (*sdk.ListActionsResult, error) {
    args := &sdk.ListActionsArgs{
        Labels:         []string{},
        LabelQueryMode: to.Ptr(sdk.LabelQueryModeAny),
        Limit:          to.Ptr(uint32(50)),
        Offset:         to.Ptr(uint32(0)),
    }

    result, err := w.ListActions(ctx, args)
    if err != nil {
        return nil, err
    }

    log.Printf("Found %d actions", result.TotalActions)
    for _, action := range result.Actions {
        log.Printf("  %s: %s - %s", *action.TxID, action.Status, action.Description)
    }

    return result, nil
}
```

---

## 3. Key Management

### Get Public Key

```go
// Get identity key
func getIdentityKey(ctx context.Context, w *wallet.Wallet) (string, error) {
    args := &sdk.GetPublicKeyArgs{
        IdentityKey: to.Ptr(true),
    }

    result, err := w.GetPublicKey(ctx, args)
    if err != nil {
        return "", err
    }

    return result.PublicKey, nil
}

// Get derived key for protocol
func getDerivedKey(
    ctx context.Context,
    w *wallet.Wallet,
    protocolID sdk.ProtocolID,
    keyID string,
    counterparty string,
) (string, error) {
    args := &sdk.GetPublicKeyArgs{
        ProtocolID:   protocolID,
        KeyID:        keyID,
        Counterparty: to.Ptr(counterparty),
    }

    result, err := w.GetPublicKey(ctx, args)
    if err != nil {
        return "", err
    }

    return result.PublicKey, nil
}
```

### Encrypt/Decrypt Data

```go
import "encoding/base64"

func encryptMessage(
    ctx context.Context,
    w *wallet.Wallet,
    plaintext string,
    recipientPubKey string,
) (string, error) {
    args := &sdk.WalletEncryptArgs{
        Plaintext:    []byte(plaintext),
        ProtocolID:   sdk.ProtocolID{2, "secure-messaging"},
        KeyID:        "msg-key",
        Counterparty: to.Ptr(recipientPubKey),
    }

    result, err := w.Encrypt(ctx, args)
    if err != nil {
        return "", err
    }

    return base64.StdEncoding.EncodeToString(result.Ciphertext), nil
}

func decryptMessage(
    ctx context.Context,
    w *wallet.Wallet,
    ciphertext string,
    senderPubKey string,
) (string, error) {
    ciphertextBytes, err := base64.StdEncoding.DecodeString(ciphertext)
    if err != nil {
        return "", err
    }

    args := &sdk.WalletDecryptArgs{
        Ciphertext:   ciphertextBytes,
        ProtocolID:   sdk.ProtocolID{2, "secure-messaging"},
        KeyID:        "msg-key",
        Counterparty: to.Ptr(senderPubKey),
    }

    result, err := w.Decrypt(ctx, args)
    if err != nil {
        return "", err
    }

    return string(result.Plaintext), nil
}
```

### Create Signature

```go
func signData(ctx context.Context, w *wallet.Wallet, data string) (string, error) {
    args := &sdk.CreateSignatureArgs{
        Data:         []byte(data),
        ProtocolID:   sdk.ProtocolID{2, "document-signing"},
        KeyID:        "sig-key",
        Counterparty: to.Ptr("self"),
    }

    result, err := w.CreateSignature(ctx, args)
    if err != nil {
        return "", err
    }

    return base64.StdEncoding.EncodeToString(result.Signature), nil
}
```

---

## 4. Storage Configuration

### SQLite Storage

```go
import (
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

func setupSQLiteStorage(dbPath string, identityKey []byte) (*storage.Storage, error) {
    db, err := gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    opts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: identityKey,
        StorageName:        "sqlite-wallet",
    }

    return storage.NewStorage(opts)
}
```

### MySQL Storage

```go
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

func setupMySQLStorage(dsn string, identityKey []byte) (*storage.Storage, error) {
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    opts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: identityKey,
        StorageName:        "mysql-wallet",
    }

    return storage.NewStorage(opts)
}
```

### PostgreSQL Storage

```go
import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
)

func setupPostgresStorage(dsn string, identityKey []byte) (*storage.Storage, error) {
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    opts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: identityKey,
        StorageName:        "postgres-wallet",
    }

    return storage.NewStorage(opts)
}
```

---

## 5. Certificate Operations

### Acquire Certificate (Direct Protocol)

```go
func acquireDirectCertificate(
    ctx context.Context,
    w *wallet.Wallet,
    certType string,
    certifier string,
) (*sdk.AcquireCertificateResult, error) {
    identityKey, _ := getIdentityKey(ctx, w)

    args := &sdk.AcquireCertificateArgs{
        AcquisitionProtocol: sdk.AcquisitionProtocolDirect,
        Type:                certType,
        Certifier:           certifier,
        SerialNumber:        []byte("cert-serial-123"),
        Subject:             identityKey,
        RevocationOutpoint:  "txid.vout",
        Fields: map[string][]byte{
            "name":  []byte("Alice Smith"),
            "email": []byte("alice@example.com"),
        },
        KeyringForSubject: map[string]string{
            // Master keyring data
        },
        Signature: []byte("signature-bytes"),
    }

    return w.AcquireCertificate(ctx, args)
}
```

### Acquire Certificate (Issuance Protocol)

```go
func requestCertificateIssuance(
    ctx context.Context,
    w *wallet.Wallet,
) (*sdk.AcquireCertificateResult, error) {
    args := &sdk.AcquireCertificateArgs{
        AcquisitionProtocol: sdk.AcquisitionProtocolIssuance,
        Type:                "https://example.com/kyc-certificate",
        Certifier:           "certifier-identity-key",
        CertifierURL:        to.Ptr("https://certifier.example.com"),
        Fields: map[string]interface{}{
            "name":      "Alice Smith",
            "birthdate": "1990-01-01",
            "country":   "US",
        },
    }

    return w.AcquireCertificate(ctx, args)
}
```

### List Certificates

```go
func listCertificates(ctx context.Context, w *wallet.Wallet) (*sdk.ListCertificatesResult, error) {
    args := &sdk.ListCertificatesArgs{
        Certifiers: []string{"certifier-identity-key"},
        Types:      []string{"https://example.com/user-certificate"},
        Limit:      to.Ptr(uint32(50)),
        Offset:     to.Ptr(uint32(0)),
    }

    result, err := w.ListCertificates(ctx, args)
    if err != nil {
        return nil, err
    }

    log.Printf("Found %d certificates", result.TotalCertificates)
    for _, cert := range result.Certificates {
        log.Printf("  Type: %s, Certifier: %s", cert.Type, cert.Certifier)
    }

    return result, nil
}
```

### Prove Certificate

```go
func proveCertificate(
    ctx context.Context,
    w *wallet.Wallet,
    certificateID string,
) (*sdk.ProveCertificateResult, error) {
    args := &sdk.ProveCertificateArgs{
        CertificateID:   certificateID,
        FieldsToReveal:  []string{"name", "email"},
        Verifier:        "verifier-identity-key",
        Privileged:      to.Ptr(false),
    }

    return w.ProveCertificate(ctx, args)
}
```

---

## 6. Error Handling

### Standard Error Handling

```go
import (
    "errors"
    "github.com/bsv-blockchain/go-wallet-toolbox/pkg/defs"
)

func handleWalletError(err error) {
    if err == nil {
        return
    }

    // Check for specific error types
    var invalidParamErr *defs.ErrInvalidParameter
    if errors.As(err, &invalidParamErr) {
        log.Printf("Invalid parameter: %s - %s", invalidParamErr.Parameter, invalidParamErr.Message)
        return
    }

    var internalErr *defs.ErrInternal
    if errors.As(err, &internalErr) {
        log.Printf("Internal error: %s", internalErr.Message)
        return
    }

    // Generic error
    log.Printf("Wallet error: %v", err)
}
```

### Transaction Error Handling

```go
func sendWithErrorHandling(
    ctx context.Context,
    w *wallet.Wallet,
    recipient string,
    satoshis uint64,
) (string, error) {
    txid, err := sendBSV(ctx, w, recipient, satoshis)
    if err != nil {
        handleWalletError(err)

        // Check if it's a review actions error
        if strings.Contains(err.Error(), "review") {
            log.Printf("Transaction requires review")
            // Handle review flow
        }

        return "", err
    }

    log.Printf("Transaction sent: %s", txid)
    return txid, nil
}
```

---

## 7. Production Patterns

### Wallet Manager Pattern

```go
type WalletManager struct {
    wallet  *wallet.Wallet
    storage *storage.Storage
    mu      sync.RWMutex
}

func NewWalletManager(ctx context.Context, rootKey *ec.PrivateKey) (*WalletManager, error) {
    db, err := gorm.Open(sqlite.Open("wallet.db"), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    storageOpts := &storage.Options{
        Db:                 db,
        StorageIdentityKey: rootKey.PubKey().Compressed(),
        StorageName:        "managed-wallet",
    }

    walletStorage, err := storage.NewStorage(storageOpts)
    if err != nil {
        return nil, err
    }

    keyDeriver := sdk.NewKeyDeriver(rootKey)
    walletServices, err := services.NewServices(ctx, &services.Options{
        Network: defs.Mainnet,
        ArcURL:  "https://arc.taal.com",
    })
    if err != nil {
        return nil, err
    }

    w, err := wallet.NewWallet(
        ctx,
        keyDeriver,
        walletStorage,
        wallet.WithServices(walletServices),
        wallet.WithNetwork(defs.Mainnet),
    )
    if err != nil {
        return nil, err
    }

    return &WalletManager{
        wallet:  w,
        storage: walletStorage,
    }, nil
}

func (wm *WalletManager) GetWallet() *wallet.Wallet {
    wm.mu.RLock()
    defer wm.mu.RUnlock()
    return wm.wallet
}

func (wm *WalletManager) Close() error {
    wm.mu.Lock()
    defer wm.mu.Unlock()

    // Cleanup resources
    return nil
}
```

### Retry Pattern

```go
func sendWithRetry(
    ctx context.Context,
    w *wallet.Wallet,
    recipient string,
    satoshis uint64,
    maxRetries int,
) (string, error) {
    var lastErr error

    for attempt := 1; attempt <= maxRetries; attempt++ {
        txid, err := sendBSV(ctx, w, recipient, satoshis)
        if err == nil {
            return txid, nil
        }

        lastErr = err
        log.Printf("Attempt %d failed: %v", attempt, err)

        if attempt < maxRetries {
            time.Sleep(time.Second * time.Duration(attempt))
        }
    }

    return "", fmt.Errorf("all %d retries failed: %w", maxRetries, lastErr)
}
```

### Background Monitor Pattern

```go
import "github.com/bsv-blockchain/go-wallet-toolbox/pkg/monitor"

func setupMonitor(
    ctx context.Context,
    walletStorage *storage.Storage,
    walletServices *services.WalletServices,
) (*monitor.Monitor, error) {
    opts := &monitor.Options{
        Storage:  walletStorage,
        Services: walletServices,
        Network:  defs.Mainnet,
    }

    m, err := monitor.NewMonitor(ctx, opts)
    if err != nil {
        return nil, err
    }

    // Start monitoring in background
    go func() {
        if err := m.Start(ctx); err != nil {
            log.Printf("Monitor error: %v", err)
        }
    }()

    return m, nil
}
```

---

## 🔗 Additional Resources

- **BRC-100 Specification**: https://bsv.brc.dev/wallet/0100
- **Go Wallet Toolbox**: https://github.com/bsv-blockchain/go-wallet-toolbox
- **Go SDK**: https://github.com/bsv-blockchain/go-sdk
- **Examples**: https://github.com/bsv-blockchain/go-wallet-toolbox/tree/master/examples
- **Storage Server**: https://github.com/bsv-blockchain/go-wallet-toolbox/blob/master/docs/storage_server.md

---

## 📝 Common Patterns Summary

| Task | Function | Key Args |
|------|----------|----------|
| Send BSV | `CreateAction()` | `Outputs`, `Options` |
| Check balance | `ListOutputs()` | Special basket |
| List UTXOs | `ListOutputs()` | `Basket`, `Spendable` |
| Get history | `ListActions()` | `Labels`, `Limit` |
| Get pubkey | `GetPublicKey()` | `ProtocolID`, `KeyID` |
| Encrypt data | `Encrypt()` | `Plaintext`, `Counterparty` |
| Get certificate | `AcquireCertificate()` | `Type`, `Certifier` |

---

**Remember**: Always use context for cancellation, handle errors explicitly, and follow Go best practices for concurrent wallet access!
