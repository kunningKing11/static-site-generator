from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextType, TextNode, text_node_to_html_node


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in textnodes]
    return children


def quote_to_html_node(items):
    quote_text = "\n".join(
        item[2:] if item.startswith("> ") else item[1:]
        for item in items
    )
    return ParentNode("blockquote", text_to_children(quote_text))


def ul_to_html_node(items):
    li_nodes = []
    for item in items:
        item = item[2:]
        children = text_to_children(item)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def ol_to_html_node(items):
    li_nodes = []
    for item in items:
        item = item.split(". ", maxsplit=1)[1]
        children = text_to_children(item)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)


def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            block_nodes.append(ParentNode("p", text_to_children(block)))
        elif block_type == BlockType.HEADING:
            if block.startswith("# "):
                levels = 1
            elif block.startswith("## "):
                levels = 2
            elif block.startswith("### "):
                levels = 3
            elif block.startswith("#### "):
                levels = 4
            elif block.startswith("##### "):
                levels = 5
            else:  # block starts with "###### "
                levels = 6

            block_nodes.append(ParentNode(f"h{levels}", text_to_children(block[(levels + 1):])))  # strip the leading # characters and the following space
        elif block_type == BlockType.CODE:
            block = block[4:-3]  # strip "```\n" from the start of the block and "```" from the end
            block_nodes.append(
                    ParentNode(
                        "pre",
                        [
                            ParentNode(
                                "code",
                                [
                                    text_node_to_html_node(TextNode(block, TextType.TEXT))
                                    ]
                                )
                            ]
                        )
                    )
        else:  # block_type is either BlockType.QUOTE, BlockType.ULIST, or BlockType.OLIST
            items = block.split("\n")
            if block_type == BlockType.QUOTE:
                block_nodes.append(quote_to_html_node(items))
            elif block_type == BlockType.ULIST:
                block_nodes.append(ul_to_html_node(items))
            else:  # block_type == BlockType.OLIST
                block_nodes.append(ol_to_html_node(items))
    root_node = ParentNode("div", block_nodes)
    return root_node

