# Programming Assignment 2: Deques and Randomized Queues

## [specification](http://coursera.cs.princeton.edu/algs4/assignments/queues.html)

## [checklist](http://coursera.cs.princeton.edu/algs4/checklists/queues.html)

## Deques 双向队列
数据结构采用双向链表
```java
public class Deque<Item> implements Iterable<Item> {
  private int N;         //size 
  private Node front ;
  private Node near;
  private class Node {
    Item item;
    Node first;
    Node next;
 }
```

### 注意事项
取出item的时候注意避免对象游离（即需要将Node中对item的引用置null）


## RandomizedQueue 随机队列
数据结构采用可变长数组
