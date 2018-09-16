container实现对集合的操作

## List双向链表
`Element`是列表元素, 有指向前后元素的指针(next,prev)和一个指向当前列表的指针(list)
``` go
// Element is an element of a linked list.
type Element struct {
	// Next and previous pointers in the doubly-linked list of elements.
	// To simplify the implementation, internally a list l is implemented
	// as a ring, such that &l.root is both the next element of the last
	// list element (l.Back()) and the previous element of the first list
	// element (l.Front()).
	next, prev *Element

	// The list to which this element belongs.
	list *List

	// The value stored with this element.
	Value interface{}
}
```
+ Next()返回Element在列表中后个元素
+ Prev()返回Element在列表中前个元素

List双向链表结构, root是链表的当前元素指针, len是链表长度
``` go
// List represents a doubly linked list.
// The zero value for List is an empty list ready to use.
type List struct {
	root Element // sentinel list element, only &root, root.prev, and root.next are used
	len  int     // current list length excluding (this) sentinel element
}
```
+ Init()初始化链表
