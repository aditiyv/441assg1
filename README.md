# 🚀 TCP Palindrome Checker

A **client-server application** that checks whether a given string is a **palindrome** or if it can be rearranged into one. It utilizes **Python socket programming** to enable TCP communication between a client and a server. 

The project supports:
- **Simple Palindrome Check**: Determines if a string is a palindrome while ignoring spaces, punctuation, and case.
- **Complex Palindrome Check**: Verifies if a string can be rearranged into a palindrome and calculates the **minimum swaps** required.
- **Concurrency Support**: Handles multiple clients simultaneously using **multithreading**.
- **Secure Data Transmission**: Implements **XOR-based encryption** for message security.

This project is designed to **enhance understanding of networking, concurrency, and algorithm design** through practical implementation.
## 📌 Table of Contents
- Compiling and Running Server and Client
- Example Inputs and Outputs
- Assumptions and Limitations

## 🚀 Compiling and Running Server and Client
Before running the project, make sure you have Python 3 installed. You can check by running:

```bash
python --version
```

To run the server, use the command:

```bash
python3 Palindrome_Starter_Server1.py
```

To run the client, use the command:

```bash
python3 Palindrome_Starter_Client1.py
```

## 🎯 Example Inputs and Outputs

Example 1 - Simple Palindrome Check (Valid Palindrome)

```bash
Client input: "racecar" (Choice 1)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Is palindrome: True"
```

Example 2 - Simple Palindrome Check (Non-Palindrome)

```bash
Client input: "hello" (Choice 1)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Is palindrome: False"
```

Example 3 - Complex Check (Can Rearrange to Palindrome)

```bash
Client input: "aabb" (Choice 2)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Can form a palindrome: True, Complexity score: 1"
```

Example 4 - Complex Check (Cannot Rearrange to Palindrome)

```bash
Client input: "abcde" (Choice 2)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Can form a palindrome: False, Complexity score: -1"
```

Example 5 - Edge Case (Empty String)

```bash
Client input: "" (Choice 1)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Is palindrome: True"  # Empty string is considered a palindrome
```

Example 6 - Complex Check (Odd-Length Palindrome)

```bash
Client input: "radar" (Choice 2)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Can form a palindrome: True, Complexity score: 0"  # Already a palindrome
```

Example 7 - Complex Check (Minimum Swaps Calculation)

```bash
Client input: "abba" (Choice 2)
Encrypted Transmission: <Encrypted data sent to server>
Server response: "Can form a palindrome: True, Complexity score: 0"  # No swaps needed
```

## ✨ Assumptions and Limitations
- ✅ Assumptions: 
    - The input may contain spaces, punctuation, and mixed case, which should be ignored in palindrome checks.
    - The server assumes that all input strings are ASCII-based.
    - The minimum number of swaps needed to form a palindrome is used as the complexity score.
    - The client retries up to 3 times if the server does not respond within 5 seconds.

- 🚀 Limitations:
    - Only alphanumeric characters are considered when checking for palindromes.
    - The complexity score calculation assumes an optimal solution and may not consider all possible rearrangements.
    - The encryption used (XOR cipher) is weak and should not be relied upon for real-world security.
    - The system does not handle extremely large inputs efficiently, as the palindrome checking and rearrangement calculations may become computationally expensive.
