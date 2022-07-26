```
struct Node:
    value
    next

func (Node) get_value():
    return self.value

func (Node) get_next():
    return self.next

node1 = Node(value=1, next=nil)
node2 = Node(value=1, next=nil)
node1.next = node2
```

```
interface Reader:
    read()

interface Writer:
    write()

interface ReadWriter:
    Reader
    Writer
```
