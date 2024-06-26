```python
# test script
for i in range(1, 10):
    print(i)
```

<p align="center">
<img width="600" height="300" src='https://g.gravizo.com/svg?
digraph astgraph {
          node [fontsize=12, fontname="Courier", height=.1];
          # ranksep=.3;
          # edge [arrowsize=.5]

  node0 [label="Program"]
  node1 [label="For"]
  node2 [label="i"]
  node1 -> node2
  node3 [label="range(1,10)"]
  node1 -> node3
  node4 [label="Block"]
  node5 [label="print(i)"]
  node4 -> node5
  node1 -> node4
  node0 -> node1
}
'/>
</p>

```python
for (var i = 0; i < 10; i = i + 1):
    print(i)
```

<p align="center">
<img width="600" height="300" src='https://g.gravizo.com/svg?
digraph astgraph {
          node [fontsize=12, fontname="Courier", height=.1];
          # ranksep=.3;
          # edge [arrowsize=.5]

  node0 [label="Program"]
  node1 [label="For"]
  node2 [label="Var i"]
  node3 [label="0"]
  node2 -> node3
  node1 -> node2
  node4 [label="Compare
<"]
  node5 [label="i"]
  node4 -> node5
  node6 [label="10"]
  node4 -> node6
  node1 -> node4
  node7 [label="Assign
i"]
  node8 [label="+"]
  node9 [label="i"]
  node8 -> node9
  node10 [label="1"]
  node8 -> node10
  node7 -> node8
  node1 -> node7
  node11 [label="Block"]
  node12 [label="print(i)"]
  node11 -> node12
  node1 -> node11
  node0 -> node1
}
'/>
</p>
