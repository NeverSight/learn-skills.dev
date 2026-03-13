---
name: testing-clojure-cljs
description: "Set up and write tests for Clojure and ClojureScript projects using cljs.test, cljs-init-tests, and shadow-cljs"
---

# Skill: Testing Clojure ClojureScript

## Goal
Set up and write tests for Clojure and ClojureScript projects using cljs.test, cljs-init-tests, and shadow-cljs workflow.

## Use This Skill When
- Testing Clojure or ClojureScript code
- Setting up test infrastructure for CLJS projects
- Using shadow-cljs for compilation
- The user asks to "add Clojure tests" or "set up cljs.test"

## Do Not Use This Skill When
- Testing TypeScript/JavaScript code (use testing-typescript-vitest)
- Project uses a different Clojure test framework (midje, test.check)

## ClojureScript Test Setup

### shadow-cljs Configuration

```clojure
;; shadow-cljs.edn
{:source-paths ["src" "test"]
 :dependencies [[cider/cider-nrepl "0.28.5"]
                [cider/orchard "0.11.0"]]

 :builds {:test {:target :browser-test
                 :output-to "target/test/test.js"
                 :tests {:matches #".*-test$"}
                 :devtools {:http-port 8080
                            :http-resource-root "target/test"}}
          
          :node-test {:target :node-test
                      :output-to "target/test/node-test.js"
                      :tests {:matches #".*-test$"}}}}
```

### package.json Scripts

```json
{
  "scripts": {
    "test:cljs": "shadow-cljs compile node-test && node target/test/node-test.js",
    "test:browser": "shadow-cljs compile test && npx http-server target/test -p 8080",
    "test:watch": "shadow-cljs watch test"
  }
}
```

## Basic cljs.test Syntax

```clojure
(ns my-project.core-test
  (:require [cljs.test :refer [deftest is testing are]]
            [my-project.core :as core]))

(deftest add-test
  (testing "addition"
    (is (= (core/add 2 3) 5))
    (is (= (core/add -1 1) 0))
    (is (= (core/add 0 0) 0))))

(deftest subtract-test
  (testing "subtraction"
    (is (= (core/subtract 5 3) 2))
    (is (= (core/subtract 3 5) -2))))

(deftest multiply-test
  (testing "multiplication"
    (are [x y] (= (core/multiply x y) (* x y))
         2 3
         -1 5
         0 10)))
```

## Test Assertions

```clojure
(deftest assertion-examples
  (testing "basic assertions"
    (is true)
    (is (= 1 1))
    (is (not false)))
  
  (testing "collection assertions"
    (is (empty? []))
    (is (seq [1 2 3]))
    (is (contains? {:a 1} :a))
    (is (contains? [1 2 3] 0)))
  
  (testing "exception handling"
    (is (thrown? js/Error
           (throw (js/Error. "test")))))
  
  (testing "approx assertions for floats"
    (is (== 0.3 (+ 0.1 0.2)))))
```

## Testing Async Code

```clojure
(ns my-project.async-test
  (:require [cljs.test :refer [deftest is testing async]]
            [my-project.async :as async]))

(deftest async-test
  (async done
    (async/timeout 100
      (is true))
    (done)))
  
(deftest promise-test
  (async done
    (-> (async/load-data)
        (.then (fn [data]
                 (is (= (:status data) 200))
                 (done)))
        (.catch (fn [err]
                  (is false "Should not error")
                  (done))))))
```

## cljs-init-tests Macro

The `cljs-init-tests` provides convenient initialization for tests:

```clojure
(ns my-project.init-test
  (:require [cljs-init-tests.core :refer [init-tests deftest-test]]
            [my-project.math :as math]
            [cljs.test :refer [deftest is testing]]))

;; Initialize test infrastructure
(init-tests)

;; Test definitions work normally
(deftest math-tests
  (testing "basic math operations"
    (is (= (math/add 2 3) 5))
    (is (= (math/subtract 5 3) 2))))
```

## Setup and Fixtures

```clojure
(ns my-project.fixtures-test
  (:require [cljs.test :refer [deftest use-fixtures testing]]
            [my-project.db :as db]))

;; Define fixtures
(defn setup-db [f]
  (db/reset!)
  (f)
  (db/cleanup!))

(defn with-logging [f]
  (println "Starting test")
  (f)
  (println "Finished test"))

;; Use fixtures
(use-fixtures :once setup-db)
(use-fixtures :each with-logging)

(deftest database-test
  (testing "database operations"
    (is (some? (db/connect)))
    (is (db/insert {:name "test"}))))
```

## Testing CLJS-Specific Features

```clojure
(ns my-project.cljs-specific-test
  (:require [cljs.test :refer [deftest is testing]]
            [cljs.core :as c]))

(deftest atom-test
  (let [counter (atom 0)]
    (swap! counter inc)
    (is (= @counter 1))
    (swap! counter inc)
    (is (= @counter 2))))

(deftest reagent-test
  (let [component (fn []
                    [:div "Hello"])]
    (is (fn? component))))
  
(deftest protocol-test
  (let [record (->Record. :field)]
    (is (= (:field record) :field))))
```

## Shadow-cljs Test Compilation

### Test Build Output

```bash
# Compile for Node.js
shadow-cljs compile node-test

# Compile for browser
shadow-cljs compile test

# Watch and test
shadow-cljs watch test
```

### CI/CD Integration

```bash
#!/bin/bash
# run-cljs-tests.sh

set -e

# Install dependencies
yarn install

# Compile tests
shadow-cljs compile node-test

# Run tests
node target/test/node-test.js

# Check exit code
if [ $? -eq 0 ]; then
  echo "Tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi
```

## Organization

```
src/
└── my_project/
    ├── core.cljs
    └── core_test.cljs  # Test in same namespace

test/
└── my_project/
    ├── integration_test.cljs
    └── e2e_test.cljs
```

## Best Practices

### 1. Test Naming
```clojure
;; GOOD - descriptive test names
(deftest add-two-positive-numbers-returns-sum)
(deftest handle-empty-input-gracefully)

;; BAD - vague names
(deftest test-add)
(deftest test-stuff)
```

### 2. Test Organization
```clojure
(deftest arithmetic-tests
  (testing "addition"
    (is (= (+ 2 3) 5))
    (is (= (+ 0 0) 0)))
  
  (testing "subtraction"
    (is (= (- 5 3) 2))))
```

### 3. Property-Based Testing
```clojure
;; With test.check
(deftest sort-is-idempotent
  (let [gen (gen/vector gen/int)]
    (is (forall [v gen]
           (= (sort v) (sort (sort v)))))))
```

## Running Tests

| Command | Purpose |
|---------|---------|
| `shadow-cljs compile test` | Compile for browser |
| `shadow-cljs compile node-test` | Compile for Node.js |
| `shadow-cljs watch test` | Watch and test |
| `shadow-cljs test` | Run tests via CLI |

## Output
- shadow-cljs.edn configuration
- Test namespace setup with cljs.test
- Example test files for CLJS
- Fixtures and setup patterns
- CI/CD test script

## References
- cljs.test: https://cljs.github.io/api/cljs.test/
- shadow-cljs: https://shadow-cljs.github.io/docs/
- cljs-init-tests: https://github.com/Olical/cljs-init-tests
- test.check: https://github.com/clojure/test.check

## Suggested Next Skills
Check the [Skill Graph](../skill_graph.json) for the full workflow.

- **[testing-typescript-vitest](../testing-typescript-vitest/SKILL.md)**
