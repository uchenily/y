```python
# test script
for i in range(1, 10):
    print(i)
```

<p align="center">
<img width="600" height="300" src="https://g.gravizo.com/source/y_mark?https://raw.githubusercontent.com/uchenily/y/main/README.md">
</p>

<details>
<summary></summary>
y_mark

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

y_mark
</details>
