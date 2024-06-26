```python
# test script
for i in range(1, 10):
    print(i)
```

![AST](https://g.gravizo.com/svg?digraph+astgraph+%7b%0a++++++++++node+%5bfontsize%3d12%2c+fontname%3d%22Courier%22%2c+height%3d.1%5d%3b%0a++++++++++%23+ranksep%3d.3%3b%0a++++++++++%23+edge+%5barrowsize%3d.5%5d%0a%0a++node0+%5blabel%3d%22Program%22%5d%0a++node1+%5blabel%3d%22For%22%5d%0a++node2+%5blabel%3d%22i%22%5d%0a++node1+-%3e+node2%0a++node3+%5blabel%3d%22range(1%2c10)%22%5d%0a++node1+-%3e+node3%0a++node4+%5blabel%3d%22Block%22%5d%0a++node5+%5blabel%3d%22print(i)%22%5d%0a++node4+-%3e+node5%0a++node1+-%3e+node4%0a++node0+-%3e+node1%0a%7d)

```python
for (var i = 0; i < 10; i = i + 1):
    print(i)
```

![AST](https://g.gravizo.com/svg?digraph+astgraph+%7b%0a++++++++++node+%5bfontsize%3d12%2c+fontname%3d%22Courier%22%2c+height%3d.1%5d%3b%0a++++++++++%23+ranksep%3d.3%3b%0a++++++++++%23+edge+%5barrowsize%3d.5%5d%0a%0a++node0+%5blabel%3d%22Program%22%5d%0a++node1+%5blabel%3d%22For%22%5d%0a++node2+%5blabel%3d%22Var+i%22%5d%0a++node3+%5blabel%3d%220%22%5d%0a++node2+-%3e+node3%0a++node1+-%3e+node2%0a++node4+%5blabel%3d%22Compare%0a%3c%22%5d%0a++node5+%5blabel%3d%22i%22%5d%0a++node4+-%3e+node5%0a++node6+%5blabel%3d%2210%22%5d%0a++node4+-%3e+node6%0a++node1+-%3e+node4%0a++node7+%5blabel%3d%22Assign%0ai%22%5d%0a++node8+%5blabel%3d%22%2b%22%5d%0a++node9+%5blabel%3d%22i%22%5d%0a++node8+-%3e+node9%0a++node10+%5blabel%3d%221%22%5d%0a++node8+-%3e+node10%0a++node7+-%3e+node8%0a++node1+-%3e+node7%0a++node11+%5blabel%3d%22Block%22%5d%0a++node12+%5blabel%3d%22print(i)%22%5d%0a++node11+-%3e+node12%0a++node1+-%3e+node11%0a++node0+-%3e+node1%0a%7d)
