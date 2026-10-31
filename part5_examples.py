"""here are five runtime examples. they build ASTs up until function parsing has been added."""
from expression_nodes import NumberNode, VariableNode, BinaryOpNode, FunctionCallNode
from statement_nodes import (
    AssignmentNode, PrintNode, BlockNode, IfNode,
    FunctionDefinitionNode, ReturnNode, ExpressionStatementNode,
)


def examples():
    return [
        ("Parameters and return", [
            FunctionDefinitionNode("add", ["a", "b"], BlockNode([
                ReturnNode(BinaryOpNode(VariableNode("a"), "+", VariableNode("b"))),
            ])),
            AssignmentNode("result", FunctionCallNode("add", [NumberNode(10), NumberNode(20)]), True),
            PrintNode(VariableNode("result")),
        ], "30\n"),
        ("Local shadowing", [
            AssignmentNode("x", NumberNode(10), True),
            FunctionDefinitionNode("test", [], BlockNode([
                AssignmentNode("x", NumberNode(20), True),
                PrintNode(VariableNode("x")),
            ])),
            ExpressionStatementNode(FunctionCallNode("test", [])),
            PrintNode(VariableNode("x")),
        ], "20\n10\n"),
        ("New locals on every call", [
            FunctionDefinitionNode("increment", ["n"], BlockNode([
                AssignmentNode("local", BinaryOpNode(VariableNode("n"), "+", NumberNode(1)), True),
                ReturnNode(VariableNode("local")),
            ])),
            PrintNode(FunctionCallNode("increment", [NumberNode(4)])),
            PrintNode(FunctionCallNode("increment", [NumberNode(9)])),
        ], "5\n10\n"),
        ("Return from a nested block", [
            FunctionDefinitionNode("choose", ["n"], BlockNode([
                IfNode(BinaryOpNode(VariableNode("n"), ">", NumberNode(0)), BlockNode([
                    ReturnNode(NumberNode(1)),
                ])),
                ReturnNode(NumberNode(0)),
                PrintNode(NumberNode(999)),
            ])),
            PrintNode(FunctionCallNode("choose", [NumberNode(3)])),
            PrintNode(FunctionCallNode("choose", [NumberNode(0)])),
        ], "1\n0\n"),
        ("Based on definition scope, not caller scope", [
            AssignmentNode("x", NumberNode(10), True),
            FunctionDefinitionNode("read", [], BlockNode([ReturnNode(VariableNode("x"))])),
            FunctionDefinitionNode("caller", [], BlockNode([
                AssignmentNode("x", NumberNode(99), True),
                ReturnNode(FunctionCallNode("read", [])),
            ])),
            PrintNode(FunctionCallNode("caller", [])),
        ], "10\n"),
    ]
