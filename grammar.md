// vim: et ts=8

```
program         → declaration* EOF

declaration     → varDecl
                | funDecl
                | statement

varDecl         → "var" IDENTIFIER ( "=" expression )
funDecl         → "func" function

statement       → exprStmt
                | asignStmt
                | forStmt
                | ifStmt
                | returnStmt
                | whileStmt
                | continueStmt
                | breakStmt
                | comment
                | block

exprStmt        → expression
forStmt         → "for" IDENTIFIER "in" expression COLON block
ifStmt          → "if" expression COLON block
                ( "elif" expression COLON block )*
                ( "else" COLON block )?
returnStmt      → "return" expression?
whileStmt       → "while" expression COLON block
comment         → COMMENT
block           → INDENT declaration* DEDENT

expression      → assignment
                | array_list
                | logic_or

assignment      → IDENTIFIER ( "[" expression "]" )? "=" expression
array_list      → "[" arguments? "]"
logic_or        → logic_and ( "||" logic_and )*
logic_and       → equality ( "&&" equality )*
equality        → comparison ( ( "!=" | "==" ) comparison )*
comparison      → term ( ( ">" | ">=" | "<" | "<=" ) term )*
term            → factor ( ( "-" | "+" ) factor )*
factor          → unary ( ( "/" | "*" ) unary )*

unary           → ( "!" | "-" ) primary
primary         → atom
                | "(" expression ")"
                | "[" arguments "]"
                | primary "(" arguments? ")"
                | primary "[" expression "]"

atom            → "true" | "false" | "nil" | NUMBER | STRING | IDENTIFIER

function        → IDENTIFIER "(" parameters? ")" block
parameters      → IDENTIFIER ( "," IDENTIFIER )*
arguments       → expression ( "," expression )*
```
