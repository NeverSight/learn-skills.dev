---
name: dart-provider-architecture
description: "Riverpod Provider 架構設計規範——依賴注入、介面隔離、必接線 provider 與 wiring test 配對規則、測試可行性。Use for: (1) 設計新的 ViewModel/Notifier 類別, (2) 審查 Provider 依賴注入與 app root 接線是否正確, (3) 宣告 throw UnimplementedError 式必接線 provider 時配對 wiring test, (4) 測試中配置 ProviderScope.overrides, (5) 發現 ref.read/watch 使用錯誤或 ProviderException 啟動例外時。Use when: 程式碼涉及 Riverpod Provider、Notifier、ViewModel、DI 接線、override 設計，或 app 啟動出現 provider 錯誤畫面時。"
metadata:
  version: 2.0.0
---

# Provider Architecture Skill

Riverpod Provider 架構設計規範——確保正確的依賴注入、介面隔離、接線閉環和測試可行性。

## 核心設計原則

狀態操作必須透過介面語意化方法封裝；DI 契約必須與 wiring 驗證閉環（見「配對規則」）。ref 誤用的根源是直接操作狀態而非透過介面；DI 缺陷的根源是契約與驗證之間的迴路沒有閉合——兩者都不是單純的 API 用法問題。

### 1. 介面隔離原則

對內和對外使用不同的介面：

| 介面類型 | 暴露對象 | 範例方法 |
|---------|---------|---------|
| 對外（Widget 層） | 語意化方法 | `selectFile()`, `startImport()`, `reset()` |
| 對內（ViewModel） | 私有方法 | `_updateProgress()`, `_handleError()` |

### 2. 語意化操作原則

不直接操作狀態，而是透過有意義的方法名稱：

```dart
// 錯誤：直接操作狀態
ref.read(provider.notifier).state = newState;

// 正確：透過語意化方法
ref.read(provider.notifier).selectFile();
```

### 3. 依賴注入透過介面原則

服務透過 Provider 注入，不硬編碼實例：

```dart
// 錯誤：ViewModel 直接依賴具體實作
class MyViewModel {
  final _dataService = DataService();  // 硬編碼，無法測試替換
}

// 正確：透過 Provider 注入
class MyViewModel extends Notifier<MyState> {
  late final DataService _dataService;  // 延遲初始化

  @override
  MyState build() {
    // 在 build() 中透過 ref.read() 取得服務，測試中可 override
    _dataService = ref.read(dataServiceProvider);
    return MyState.initial();
  }
}
```

## 標準 ViewModel 模式

```dart
/// 職責：管理資料匯入流程的狀態
/// 設計原則：服務經 Provider 注入（支援測試替換）；對外只暴露語意化方法；
/// 狀態操作封裝在內部。
class DataImportViewModel extends Notifier<DataImportState> {
  late final DataService _dataService;
  late final FileService _fileService;

  @override
  DataImportState build() {
    _dataService = ref.read(dataServiceProvider);
    _fileService = ref.read(fileServiceProvider);
    return const DataImportState();
  }

  // === 對外語意化方法 ===
  Future<void> selectFile() async {
    final file = await _fileService.pickFile();
    if (file != null) {
      state = state.copyWith(selectedFile: file);
    }
  }

  Future<void> startImport() async {
    _updateProgress(0.0);
    try {
      final records = await _fileService.parse(state.selectedFile!);
      await _dataService.saveAll(records);
      _updateProgress(1.0);
    } on AppException catch (e) {
      _handleError(e);
    }
  }

  void reset() => state = const DataImportState();

  // === 對內私有方法 ===
  void _updateProgress(double progress) =>
      state = state.copyWith(progress: progress);
  void _handleError(AppException error) =>
      state = state.copyWith(error: error);
}

/// Provider 定義：使用 .new 簡化寫法，Notifier 在 build() 中自行取得依賴
final dataImportViewModelProvider =
    NotifierProvider<DataImportViewModel, DataImportState>(
  DataImportViewModel.new,
);
```

## watch / read 紀律

```dart
// 錯誤：在普通方法中使用 watch（導致不必要的重建）
void someMethod() {
  final service = ref.watch(serviceProvider);
}

// 正確：build() 內 watch 響應式資料、read 服務實例；其他方法一律 read
@override
MyState build() {
  final reactiveData = ref.watch(someDataProvider);  // OK：響應式資料
  _service = ref.read(serviceProvider);              // OK：服務實例
  return MyState(data: reactiveData);
}

void someMethod() {
  final service = ref.read(serviceProvider);  // OK：一次性讀取
}
```

## 配對規則：必接線 provider 與 wiring test 閉環

fail-fast DI 契約（未接線即拋錯）是正確設計，但契約只在有人執行該路徑時才 fail。
測試若全部自備 override，真實接線路徑就是零覆蓋——契約永不被演練，漏接要到
實機啟動才炸開，且全部畫面一起死。

**規則：每宣告一個必接線 provider（宣告端形態見下），必須同時存在兩個測試。**

### 觸發形態（宣告端）

觸發判準是**語意**不是字面：任何「未接線即拋錯的 DI 注入點」都算——`UnimplementedError` 只是慣用形態，`StateError`、`late` 未初始化、強制轉型失敗等等價寫法同樣觸發配對規則。

```dart
/// 資料層注入點。app root 須以真實實作 override，未 override 即拋錯，
/// 強制呼叫端明確接線（DI 契約）。
final repositoryProvider = Provider<Repository>((ref) {
  throw UnimplementedError('repositoryProvider must be overridden at app root');
});
```

> **形態無關性**：本規則的論證（fail-fast 契約 + 全 mock 測試 ⇒ 真實接線零覆蓋）與 DI 形態無關——GetIt 的未 register 拋錯、InheritedWidget 的 `of(context)!` 同構適用，本 skill 僅提供 Riverpod 落地形式。
> **雙路由**：wiring test 屬「綠燈後補的防護型測試」，須依 `/tdd` skill `references/phase2/rules.md` 組 4 Q12 做一次故意破壞實測；其替身邊界（本例 ffi + in-memory 屬 host 層結構替身，不涵蓋 on-device 接縫）見同檔「紅燈層級順序」節替身術語。

### 配對測試 (a)：真實接線 wiring test

用**與 main.dart 相同的實作型別**建立 override，pump 真實 app root widget，
驗證首畫面 build 不拋 ProviderException。這條測試覆蓋的是「契約可被真實實作
滿足」，不是 mock 頂替：

```dart
testWidgets('app root wiring: real overrides build without ProviderException',
    (tester) async {
  final container = ProviderContainer(
    overrides: [
      // 與 main.dart 相同的接線型別（真實 Repository 實作 + in-memory 資源）
      repositoryProvider.overrideWithValue(
        SqliteRepository(databaseFactory: databaseFactoryFfi,
                         path: inMemoryDatabasePath),
      ),
    ],
  );
  addTearDown(container.dispose);

  await tester.pumpWidget(
    UncontrolledProviderScope(container: container, child: const MyApp()),
  );
  await tester.pump();  // 真實 I/O 場景勿用 pumpAndSettle（FakeAsync 無法結算）

  expect(tester.takeException(), isNull);
});
```

### 配對測試 (b)：未 override 迴歸鎖

把 fail-fast 行為本身鎖進測試，防止契約被靜默改成回傳假實作：

```dart
test('un-overridden mandatory provider still throws', () {
  final container = ProviderContainer();
  addTearDown(container.dispose);
  expect(
    () => container.read(repositoryProvider),
    throwsA(isA<ProviderException>()),
  );
});
```

### 為什麼通用生成會漏掉這條

「通用生成」指未載入本規範的 LLM 依通用知識產生程式碼。它會把契約（拋錯 provider）和測試（mock override）**各自寫對**，
但不知道兩者之間有一條必須閉合的迴路——mock override 教學愈完整，真實接線
路徑愈沒有測試理由存在。本規則就是把這條迴路顯性化。

## 測試最佳實踐

### Provider Override 機制

在測試中透過 `ProviderScope.overrides` 注入 Mock 服務：

```dart
testWidgets('完整匯入流程', (tester) async {
  final mockFileService = MockFileService();
  mockFileService.setPickResult(tempFile);  // 語意化配置

  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        fileServiceProvider.overrideWithValue(mockFileService),
      ],
      child: const MaterialApp(home: DataImportScreen()),
    ),
  );

  await tester.tap(find.byKey(const Key('import_button')));
  await tester.pumpAndSettle();
  expect(find.text('匯入完成'), findsOneWidget);
});
```

Mock override 適用於**功能行為測試**；它不能取代配對規則的 wiring test——
兩者驗證的是不同命題（行為正確 vs 接線存在）。

### Mock 服務設計原則

Mock 服務也提供語意化配置方法：

```dart
class MockFileService implements FileService {
  File? _pickResult;
  void setPickResult(File? file) => _pickResult = file;  // 語意化配置

  @override
  Future<File?> pickFile() async => _pickResult;
}
```

## 禁止行為

| 禁止 | 修正 |
|------|------|
| 直接操作 `.state`（`notifier.state = x`） | 語意化方法（`notifier.updateX(v)`） |
| 建構函式硬編碼服務實例 | `late final` + `build()` 內 `ref.read()` |
| 非 build 方法中 `ref.watch()` | build 內 watch、其他一律 read |
| 宣告拋錯式必接線 provider 而無配對測試 | 補 wiring test (a) + 迴歸鎖 (b) |
| wiring test 用 mock 頂替真實實作型別 | 用與 app root 相同的實作型別 + in-memory 資源 |

## 檢查清單

### ViewModel 設計

- [ ] 服務以 `late final` 宣告、在 `build()` 中 `ref.read()` 取得？
- [ ] 對外方法都是語意化的（動詞開頭）？狀態操作封裝在私有方法？
- [ ] Provider 定義使用 `.new` 簡化寫法、不在建構函式傳依賴？

### 接線閉環（配對規則）

- [ ] 每個 `throw UnimplementedError` 式 provider 都有真實接線 wiring test？
- [ ] wiring test 用與 main.dart 相同的實作型別（非 mock）？
- [ ] 未 override 拋錯行為有迴歸鎖測試？
- [ ] 真實 I/O 的 wiring test 用 `pump()` 而非 `pumpAndSettle()`？

### 測試設計

- [ ] 功能測試使用 `ProviderScope.overrides` 注入 Mock？
- [ ] Mock 服務提供語意化配置方法？
- [ ] 透過 UI 互動驗證行為（而非檢查內部狀態）？

## 本 skill 維護約束（反漂移）

前版（1.0.0）因內容綁定單一專案而被移除。維護本檔時：

- 禁止引用任何專案的檔案路徑作「參考範例」——範例一律以自足程式碼呈現
- 禁止引用專案層級 error-pattern / ticket 編號；需引用教訓時，將教訓以通用化敘述內嵌本檔
- 範例命名使用通用領域詞（DataImport、Repository），不用專案業務詞
- 新增內容前自問：替換專案名稱後此段是否仍成立？否則不屬於本 skill

---

版本紀錄在同目錄的 `CHANGELOG.md`。
