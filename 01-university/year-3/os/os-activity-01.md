---
title: OS Activity 01 — Introduction to Threads
tags:
  - university
  - os
  - individual
  - threads
status: active
created: 2026-09-11
due: TBA
subject: os
---

# OS Activity 01 — Introduction to Threads

## Assignment

Run and summarize understanding of threads from four programs.

- `Program1.cs` — create simple threads
- `Program2.cs` — resource sharing between threads
- `Program3.cs` — putting a thread to sleep
- `Program4.cs` — joining a thread

## Files

`~/Documents/University/Year-3/OS/Activity01/`

---

## Summary

A thread is the smallest unit of execution within a program. When a program starts, it runs on a single thread called the main thread. It is possible to create additional threads that run concurrently, meaning the operating system switches between them rapidly to give the appearance of parallel execution. This report summarizes the behavior observed across four programs, each demonstrating a different aspect of thread management in C\#.

### Program 1 — Creating Simple Threads

Program 1 creates two threads, each printing its own counter from 0 to 9999. When both threads are started with `th1.Start()` and `th2.Start()`, they run concurrently rather than one after the other. The output on screen shows lines from Thread 1 and Thread 2 appearing mixed together, because the operating system schedules both threads and switches between them without a fixed order. This demonstrates that threads do not execute in the order they were created, and the programmer cannot predict which thread will print next at any given moment.

### Program 2 — Sharing Resources Between Threads

Program 2 introduces a shared variable called `resource`, which all three execution contexts, including the main thread, Thread 1, and Thread 2, can read at the same time. The program prints the value of `resource` from each context. Since the variable is declared as `static`, it belongs to the class rather than any individual thread, which means all threads share the same copy. This characteristic creates both prospects and difficulties, as sharing data allows threads to communicate, but without proper control it can lead to misunderstandings and conflicts in the data when multiple threads try to modify it at the same time.

### Program 3 — Putting a Thread to Sleep

Program 3 demonstrates `Thread.Sleep(1000)`, which pauses the main thread for 1000 milliseconds before reading the shared variable. During that pause, `th1` runs and changes `resource` from 10000 to 55555. When the main thread wakes up and prints the value, it sees 55555 rather than the original value. This behavior shows that `Thread.Sleep` is a way to give other threads time to finish their work, although it is an imprecise method because the programmer must guess how long is long enough. The result depends entirely on whether the sleeping thread wakes up after the other thread has completed its assignment.

### Program 4 — Joining a Thread

Program 4 uses `th1.Join()`, which forces the main thread to wait until `th1` has completely finished before continuing. Thread 1 increments `resource` by 1 a total of 8555 times, starting from 1000. Without `Join`, the main thread might print `resource` before Thread 1 is done, giving an incorrect intermediate value. With `Join`, the main thread is guaranteed to print the final value of 9555 every time the program runs. This is a more reliable method for synchronization compared to `Thread.Sleep`, because the main thread resumes exactly when the work is complete rather than after an arbitrary time period.

---

## Key Takeaways

Threads allow a program to perform multiple tasks at the same time, but this concurrency introduces misunderstandings and conflicts when threads share data without coordination. Program 1 shows that thread scheduling is non-deterministic. Program 2 shows that static variables are visible to all threads simultaneously. Program 3 shows that `Sleep` can create a window for another thread to complete work, but this relies on timing assumptions that may not always hold. Program 4 shows that `Join` is the correct way to wait for a thread to finish, as it removes any dependence on guessing how long a thread will take. Everything together, starting from creating a thread to synchronizing it with Join, represents the fundamental lifecycle that all multi-threaded programs must manage carefully.
