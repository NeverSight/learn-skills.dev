---
name: how-to-do-bitwise-operations-in-dart
description: Explore Dart's bitwise operations for both integers and booleans, including AND, OR (inclusive & exclusive), NAND, NOR, and XNOR, with practical code examples.
metadata:
  url: https://rodydavis.com/posts/dart/bitwise
  last_modified: Tue, 03 Feb 2026 20:04:33 GMT
---

# How to do Bitwise operations in Dart


In Dart it is possible to do [Bitwise Operations](https://en.wikipedia.org/wiki/Bitwise_operation#:~:text=In%20computer%20programming%2C%20a%20bitwise,directly%20supported%20by%20the%20processor.) with **int** and **bool** types.

## AND 

Checks if the left and right side are both true. [Learn more](https://www.ibm.com/docs/en/xl-c-and-cpp-aix/16.1?topic=expressions-bitwise-operator).

```
// int
print(0 & 1); // 0
print(1 & 0); // 0
print(1 & 1); // 1
print(0 & 0); // 0

// bool
print(false & true); // false
print(true & false); // false
print(true & true); // true
print(false & false); // false
```

## OR 

### Inclusive 

Checks if either the left or right side are true. [Learn more](https://www.ibm.com/docs/en/xl-c-and-cpp-aix/16.1?topic=be-logical-operator).

```
// int
print(0 | 1); // 1
print(1 | 0); // 1
print(1 | 1); // 1
print(0 | 0); // 0

// bool
print(false | true); // true
print(true | false); // true
print(true | true); // true
print(false | false); // false
```

### Exclusive 

Checks if both the left or right side are true but not both. [Learn more](https://www.ibm.com/docs/en/xl-c-and-cpp-aix/16.1?topic=expressions-bitwise-exclusive-operator).

```
// int
print(0 ^ 1); // 1
print(1 ^ 0); // 1
print(1 ^ 1); // 0
print(0 ^ 0); // 0

// bool
print(false ^ true); // true
print(true ^ false); // true
print(true ^ true); // false
print(false ^ false); // false
```

## NAND 

Negated AND operation.

```
// int
print(~(0 & 1) & 1); // 1
print(~(1 & 0) & 1); // 1
print(~(1 & 1) & 1); // 0
print(~(0 & 0) & 1); // 1

// bool
print(!(false & true)); // true
print(!(true & false)); // true
print(!(true & true)); // false
print(!(false & false)); // true
```

## NOR 

Negated inclusive OR operation.

```
// int
print(~(0 | 1) & 1); // 0
print(~(1 | 0) & 1); // 0
print(~(1 | 1) & 1); // 0
print(~(0 | 0) & 1); // 1

// bool
print(!(false | true)); // false
print(!(true | false)); // false
print(!(true | true)); // false
print(!(false | false)); // true
```

## XNOR 

Negated exclusive OR operation.

```
// int
print(~(0 ^ 1) & 1); // 0
print(~(1 ^ 0) & 1); // 0
print(~(1 ^ 1) & 1); // 1
print(~(0 ^ 0) & 1); // 1

// bool
print(!(false ^ true)); // false
print(!(true ^ false)); // false
print(!(true ^ true)); // true
print(!(false ^ false)); // true
```